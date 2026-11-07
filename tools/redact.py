# -*- coding: utf-8 -*-
"""
本地仓库脱敏工具（只读基线，只写本地输出目录）

用法:
    python redact.py --src <只读基线仓库> --dst <输出仓库> \
                     --rules <真实值规则.json> --review <报告输出目录>

设计约束:
- 不连接、不修改任何远程；输出仓库不配置 remote。
- 真实个人标识保存在外部 rules JSON 中，不进入任何 Git 仓库。
- 脚本本身不含真实姓名，可安全随仓库交付。
- 输出仓库使用全新 git init + 单一提交，历史中不存在含隐私的旧对象。
"""
import os
import re
import json
import shutil
import zipfile
import subprocess
import argparse
import csv
from collections import Counter

changes = []
stats = Counter()


def log(rel, kind, detail):
    changes.append((rel, kind, detail))
    stats[kind] += 1


def make_mask(s, enc, mask_char="×"):
    """生成与 s 按 enc 编码后等长的掩码字节，保证 OLE / PDF 结构不被破坏。"""
    out = bytearray()
    for ch in s:
        if ord(ch) > 127:
            out += mask_char.encode(enc)
        else:
            out += (mask_char.encode("utf-16-le") if enc == "utf-16-le" else b"x")
    return bytes(out)


def replace_bytes(data, strings):
    """在二进制中按 UTF-8 / UTF-16LE / GBK 做等长替换。"""
    n = 0
    for s in strings:
        for enc in ("utf-8", "utf-16-le", "gbk"):
            try:
                needle = s.encode(enc)
            except UnicodeEncodeError:
                continue
            if not needle or needle not in data:
                continue
            m = make_mask(s, enc)
            if len(m) != len(needle):
                continue
            n += data.count(needle)
            data = data.replace(needle, m)
    return data, n


def clear_xml_tags(data, tags):
    s = data.decode("utf-8", "ignore")
    for tag in tags:
        pat = r"<%s(?:\s[^>]*)?>.*?</%s>" % (re.escape(tag), re.escape(tag))
        s = re.sub(pat, "<%s></%s>" % (tag, tag), s, flags=re.S)
    return s.encode("utf-8")


def replace_xml_text(data, strings, mask):
    s = data.decode("utf-8", "ignore")
    n = 0
    for x in strings:
        if x in s:
            n += s.count(x)
            s = s.replace(x, mask)
    return s.encode("utf-8"), n


def clean_office(path, rel, rules):
    """清理 docx / pptx：core.xml、app.xml、custom.xml 及正文中的个人标识。"""
    with zipfile.ZipFile(path, "r") as zin:
        items = [(info, zin.read(info.filename)) for info in zin.infolist()]

    has_custom = any(i.filename.endswith("docProps/custom.xml") for i, _ in items)
    out = []
    meta_cleared = False
    for info, data in items:
        name = info.filename
        if name.endswith("docProps/custom.xml"):
            log(rel, "office_custom_removed", "删除 docProps/custom.xml 来源标记")
            continue
        if has_custom and name == "[Content_Types].xml":
            data = re.sub(rb'<Override[^>]*PartName="/?docProps/custom\.xml"[^>]*/>', b"", data)
        if has_custom and name == "_rels/.rels":
            data = re.sub(rb'<Relationship[^>]*Target="[^"]*docProps/custom\.xml"[^>]*/>', b"", data)
        if name.endswith("docProps/core.xml"):
            data = clear_xml_tags(data, rules["office_meta_tags"])
            meta_cleared = True
        elif name.endswith("docProps/app.xml"):
            data = clear_xml_tags(data, rules["office_app_tags"])
            meta_cleared = True
        elif name.endswith(".xml") and (name.startswith("word/") or name.startswith("ppt/")):
            data, n = replace_xml_text(data, rules["content_strings"], rules["mask"])
            if n:
                log(rel, "office_body_masked", "%s: %d 处" % (name, n))
        elif name.endswith(".bin"):
            data, n = replace_bytes(data, rules["binary_strings"])
            if n:
                log(rel, "office_binary_masked", "%s: %d 处" % (name, n))
        out.append((info, data))

    if meta_cleared:
        log(rel, "office_meta_cleared", "清空 core.xml / app.xml 作者与来源字段")
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w") as zout:
        for info, data in out:
            zout.writestr(info, data)
    os.replace(tmp, path)


def clean_pdf(path, rel, rules):
    """清空 PDF Info 字典与 XMP 元数据。

    必须完整重写：增量保存只追加新字典，旧的 /Author(...) 会物理残留，
    可被取证工具直接读出。
    """
    import pymupdf
    doc = pymupdf.open(path)
    doc.set_metadata({})
    try:
        doc.del_xml_metadata()
    except Exception:
        pass
    info = doc.xref_get_key(-1, "Info")
    if info[0] == "xref":
        try:
            xref = int(info[1].split()[0])
            for k in ("Creator", "Producer", "Author", "Title", "Subject",
                      "Keywords", "CreationDate", "ModDate", "Trapped"):
                try:
                    doc.xref_set_key(xref, k, "null")
                except Exception:
                    pass
        except Exception:
            pass
    tmp = path + ".clean.pdf"
    try:
        doc.save(tmp, garbage=4, deflate=True, clean=True)
        doc.close()
        os.replace(tmp, path)
        log(rel, "pdf_rewritten", "完整重写，物理删除旧 Info / XMP 对象")
    except Exception as e:
        doc.close()
        log(rel, "ERROR_pdf", "完整重写失败: %s" % str(e)[:100])
        try:
            d = pymupdf.open(path)
            d.set_metadata({})
            try:
                d.del_xml_metadata()
            except Exception:
                pass
            d.saveIncr()
            d.close()
        except Exception:
            pass
    data = open(path, "rb").read()
    data2, n = replace_bytes(data, rules["binary_strings"])
    if n:
        open(path, "wb").write(data2)
        log(rel, "pdf_bytes_masked", "等长替换 %d 处" % n)


def clean_text(path, rel, rules):
    raw = open(path, "rb").read()
    enc = "utf-8"
    try:
        s = raw.decode("utf-8")
    except UnicodeDecodeError:
        enc = "gbk"
        s = raw.decode("gbk", "ignore")
    n = 0
    for x in rules["content_strings"]:
        if x in s:
            n += s.count(x)
            s = s.replace(x, rules["mask"])
    if n:
        open(path, "wb").write(s.encode(enc))
        log(rel, "text_masked", "%s: %d 处" % (enc, n))


def clean_binary(path, rel, rules):
    """旧 .doc / 伪 .docx（OLE）：等长字节替换，不破坏复合文档结构。"""
    data = open(path, "rb").read()
    data2, n = replace_bytes(data, rules["binary_strings"])
    if n:
        open(path, "wb").write(data2)
        log(rel, "ole_masked", "等长替换 %d 处" % n)


def clean_image(path, rel):
    from PIL import Image
    im = Image.open(path)
    if im.getexif():
        im.save(path, "JPEG", quality=95)
        log(rel, "exif_cleared", "清空 EXIF")


def rename_sensitive(root, rules):
    entries = []
    for r, ds, fs in os.walk(root):
        if ".git" in r.split(os.sep):
            continue
        for name in ds + fs:
            entries.append(os.path.join(r, name))
    entries.sort(key=lambda p: p.count(os.sep), reverse=True)
    filename_from = rules.get("filename_mask_from", "xxxxxx")
    for p in entries:
        base = os.path.basename(p)
        new = base.replace(filename_from, rules["mask"])
        for x in rules["content_strings"]:
            if x in new:
                new = new.replace(x, rules["mask"])
        if new != base:
            os.rename(p, os.path.join(os.path.dirname(p), new))
            log(os.path.relpath(p, root), "renamed", "-> " + new)


def init_git(root):
    def run(*args):
        return subprocess.run(["git", "-C", root] + list(args), capture_output=True, text=True)
    run("init", "-b", "main")
    run("config", "user.name", "TZU Question Bank")
    run("config", "user.email", "noreply@invalid")
    run("add", "-A")
    r = run("commit", "-m", "chore: 清理个人隐私信息与文档来源元数据")
    if r.returncode != 0:
        print("GIT COMMIT ERROR:", r.stdout, r.stderr)
    # 明确不设置任何 remote
    print("remotes:", repr(run("remote", "-v").stdout.strip()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="只读基线仓库（不会被修改）")
    ap.add_argument("--dst", required=True, help="输出仓库目录（全新生成）")
    ap.add_argument("--rules", required=True, help="真实值规则 JSON，不入库")
    ap.add_argument("--review", required=True, help="报告输出目录，不入库")
    args = ap.parse_args()
    src, dst, review = os.path.abspath(args.src), os.path.abspath(args.dst), os.path.abspath(args.review)
    rules = json.load(open(args.rules, encoding="utf-8"))

    assert os.path.isdir(src) and os.path.exists(os.path.join(src, ".git")), "基线仓库不存在"
    assert os.path.basename(dst) == "tzu-question-bank-redacted", "输出目录名不符，拒绝执行"
    assert src != dst, "src 与 dst 不能相同"
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".git", "*.tmp", "~$*"))
    print("copied baseline ->", dst)

    files = [os.path.join(r, f) for r, ds, fs in os.walk(dst) for f in fs]
    print("files to process:", len(files))
    changes.clear()
    stats.clear()

    for path in files:
        rel = os.path.relpath(path, dst)
        ext = os.path.splitext(path)[1].lower()
        head = open(path, "rb").read(2)
        if ext in (".docx", ".pptx", ".docm") and head == b"PK":
            try:
                clean_office(path, rel, rules)
            except Exception as e:
                log(rel, "ERROR_office", str(e)[:120])
        elif ext == ".pdf":
            try:
                clean_pdf(path, rel, rules)
            except Exception as e:
                log(rel, "ERROR_pdf", str(e)[:120])
        elif ext in (".md", ".txt", ".vbs", ".gitignore"):
            clean_text(path, rel, rules)
        elif ext in (".doc", ".docx", ".docm"):
            clean_binary(path, rel, rules)
        elif ext in (".jpg", ".jpeg", ".png"):
            try:
                clean_image(path, rel)
            except Exception as e:
                log(rel, "ERROR_image", str(e)[:120])

    rename_sensitive(dst, rules)
    init_git(dst)

    os.makedirs(review, exist_ok=True)
    with open(os.path.join(review, "redaction_changes_v2.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["相对路径", "处理类型", "说明"])
        w.writerows(changes)
    with open(os.path.join(review, "redaction_stats_v2.json"), "w", encoding="utf-8") as f:
        json.dump(dict(stats), f, ensure_ascii=False, indent=2)
    print("\n=== STATS ===")
    for k, v in stats.most_common():
        print("%-28s %d" % (k, v))
    print("total change records:", len(changes))


if __name__ == "__main__":
    main()
