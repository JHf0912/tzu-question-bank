<div align="center">

# 📚 TZU Question Bank

**TZU · 计算机科学与技术专业 · 历年题库与复习资料**

_一站式汇集各学期课程试卷、复习提纲与习题答案，助你高效备考_

<br>

![School](https://img.shields.io/badge/TZU-1e88e5?style=flat-square)
![Major](https://img.shields.io/badge/专业-计算机科学与技术-43a047?style=flat-square)
![Semesters](https://img.shields.io/badge/学期-5%20个-blue?style=flat-square)
![Courses](https://img.shields.io/badge/课程-20%20门-orange?style=flat-square)
![Files](https://img.shields.io/badge/资料-420%20份-ff69b4?style=flat-square)
![Originals](https://img.shields.io/badge/可编辑原件-147%20份-9c27b0?style=flat-square)
![PRs](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square)

</div>

---

> 📌 **简介**：本仓库收集整理了 TZU 计算机科学与技术专业从大一到大三的各学期课程试题、复习资料与配套答案，按「学期 / 课程」分层组织，方便检索与取用。**每门课同时保留 PDF 与可编辑的 Word 原件**——阅读用 PDF，修改与二次整理用原件。资料持续更新中，欢迎一起完善。

---

## 📖 目录

- [✨ 项目亮点](#-项目亮点)
- [📊 数据概览](#-数据概览)
- [📦 学期构成](#-学期构成)
- [🗂️ 目录结构](#️-目录结构)
- [📚 课程一览](#-课程一览)
- [🔍 如何检索](#-如何检索)
- [✅ 检查清单](#-检查清单)
- [📄 文件说明](#-文件说明)
- [📅 更新记录](#-更新记录)
- [🚀 如何贡献](#-如何贡献)
- [⚠️ 注意事项](#️-注意事项)

---

## ✨ 项目亮点

- 🗂️ **结构清晰** — 学期 → 课程 → `pdf/` 三层直达，不用逐层翻找
- 📝 **双格式并存** — 同一份资料既有 PDF 便于阅读，也保留 `.docx` / `.doc` 原件便于修改，不用再为「想改一处却只有 PDF」发愁
- 🔄 **持续更新** — 随课程推进不断补充新学科与新资料
- 🤝 **开放共建** — 欢迎 Fork 与 Pull Request，一起把题库做大做全

---

## 📊 数据概览

| 指标 | 数量 |
|:-----|:----:|
| 🎓 已收录学期 | **5** 个（大一上 → 大三上） |
| 📘 已收录课程 | **20** 门 |
| 📎 资料文件 | **420** 份（学期内） |
| 📄 其中 PDF | **222** 份 |
| ✏️ 其中可编辑 Word 原件 | **147** 份（86 `.docx` + 61 `.doc`） |
| 🖼️ 其中说明与附件 | **51** 份（28 说明 + 18 图片 + 3 脚本 + 1 演示文稿 + 1 文本） |

> 仓库根目录另有 7 份工程文件（README、CHECKLIST、CONTRIBUTING、REDACTION、脱敏脚本等），未计入上表。

---

## 📦 学期构成

| 学期 | 课程 | PDF | 可编辑原件 | 文件合计 |
|:-----|:---:|:---:|:---:|:---:|
| 大一上 · `1-first-semester` | 4 | 18 | 16 | 38 |
| 大一下 · `1-second-semester` | 5 | 30 | 27 | 62 |
| 大二上 · `2-first-semester` | 4 | 71 | 66 | 162 |
| 大二下 · `2-second-semester` | 5 | 80 | 34 | 127 |
| 大三上 · `3-first-semester` | 2 | 23 | 4 | 31 |
| **合计** | **20** | **222** | **147** | **420** |

> 大二两学期资料量最大（数据库 45 份 PDF、算法 27 份、计算机网络 25 份），大三上目前 2 门课程，后续随课程推进补充。

---

## 🗂️ 目录结构

学期目录**直接位于仓库根**，每个学期下只放课程目录；每门课程内 `pdf/` 收 PDF，学科根放可编辑原件与课程说明。

```text
tzu-question-bank/
├── 1-first-semester/                  # 大一上（4 门）
│   ├── 高等数学（上）/
│   │   ├── pdf/                       #   PDF 资料
│   │   ├── *.docx / *.doc             #   可编辑原件
│   │   └── README.md                  #   课程说明
│   ├── 线性代数/                      #   待补充
│   ├── python/                        #   待补充
│   └── college-english-1/
├── 1-second-semester/                 # 大一下（5 门）
│   ├── 高等数学（下）/
│   ├── 离散数学/
│   ├── 大学物理/
│   ├── c/
│   └── college-english-2/
├── 2-first-semester/                  # 大二上（4 门）
│   ├── database/
│   ├── data-structures/
│   ├── 数字逻辑电路/
│   └── probability-and-statistics/
├── 2-second-semester/                 # 大二下（5 门）
│   ├── computer-organization/
│   ├── computer-networks/
│   ├── algorithm/
│   ├── java/
│   └── operating-systems/
├── 3-first-semester/                  # 大三上（2 门）
│   ├── README.md                      #   学期说明
│   ├── 数据挖掘/
│   │   ├── pdf/                       #   13 份 PDF
│   │   ├── *.docx                     #   4 份可编辑原件
│   │   ├── *.pdf                      #   8 份原始 PDF（与 pdf/ 同字节）
│   │   └── README.md
│   └── 编译原理/
│       ├── pdf/                       #   1 份 PDF
│       ├── 编译原理经典例题.pdf        #   原始副本
│       └── README.md
├── tools/                             # 脱敏脚本
├── CHECKLIST.md                       # 整理进度清单
├── CONTRIBUTING.md                    # 贡献规范
├── REDACTION.md                       # 脱敏规则说明
└── 批量转PDF_本地版.vbs                # 本地批量转换脚本
```

> 🕓 大四（`4-first-semester/`、`4-second-semester/`）目录将按同一规范陆续补充。
>
> 📌 说明：`3-first-semester` 的课程同时在学科根保留了一份原始 PDF；其余学期学科根以可编辑原件为主。

---

## 📚 课程一览

「PDF」指 `pdf/` 内的份数，「原件」指学科根的 `.docx` / `.doc` 份数。

### 🟢 大一上

| 课程 | 目录 | PDF | 原件 |
|:-----|:-----|:---:|:----:|
| 高等数学（上） | [`高等数学（上）/`](1-first-semester/高等数学（上）) | 5 | 3 |
| 线性代数 | [`线性代数/`](1-first-semester/线性代数) | — | — |
| Python | [`python/`](1-first-semester/python) | — | — |
| 大学英语 1 | [`college-english-1/`](1-first-semester/college-english-1) | 13 | 13 |

> 线性代数、Python 目前仅有课程说明，资料待补充。

### 🟢 大一下

| 课程 | 目录 | PDF | 原件 |
|:-----|:-----|:---:|:----:|
| 高等数学（下） | [`高等数学（下）/`](1-second-semester/高等数学（下）) | 3 | 3 |
| 离散数学 | [`离散数学/`](1-second-semester/离散数学) | 14 | 14 |
| 大学物理 | [`大学物理/`](1-second-semester/大学物理) | 7 | 4 |
| C 语言 | [`c/`](1-second-semester/c) | 5 | 5 |
| 大学英语 2 | [`college-english-2/`](1-second-semester/college-english-2) | 1 | 1 |

### 🔵 大二上

| 课程 | 目录 | PDF | 原件 |
|:-----|:-----|:---:|:----:|
| 数据库 | [`database/`](2-first-semester/database) | 45 | 44 |
| 数据结构 | [`data-structures/`](2-first-semester/data-structures) | 16 | 15 |
| 数字逻辑电路 | [`数字逻辑电路/`](2-first-semester/数字逻辑电路) | 2 | 1 |
| 概率论与数理统计 | [`probability-and-statistics/`](2-first-semester/probability-and-statistics) | 8 | 6 |

### 🔵 大二下

| 课程 | 目录 | PDF | 原件 |
|:-----|:-----|:---:|:----:|
| 计算机组成原理 | [`computer-organization/`](2-second-semester/computer-organization) | 4 | — |
| 计算机网络 | [`computer-networks/`](2-second-semester/computer-networks) | 25 | 14 |
| 算法设计与分析 | [`algorithm/`](2-second-semester/algorithm) | 27 | 8 |
| Java 程序设计 | [`java/`](2-second-semester/java) | 18 | 9 |
| 操作系统 | [`operating-systems/`](2-second-semester/operating-systems) | 6 | 3 |

### 🟣 大三上

| 课程 | 目录 | PDF | 原件 |
|:-----|:-----|:---:|:----:|
| 数据挖掘 | [`数据挖掘/`](3-first-semester/数据挖掘) | 21 | 4 |
| 编译原理 | [`编译原理/`](3-first-semester/编译原理) | 2 | — |

> 数据挖掘的 21 份 PDF = `pdf/` 内 13 份 + 学科根 8 份原始副本。

---

## 🔍 如何检索

1. **找资料**：进入对应学期目录（如 `2-first-semester/`）→ 选择课程
2. **阅读**：直接打开该课程 `pdf/` 内的文件
3. **修改或二次整理**：使用学科根目录下的 `.docx` / `.doc` 原件
4. **看课程范围**：先读该课程的 `README.md`，多数写有教材与考点范围

---

## ✅ 检查清单

各课程资料的整理进度——包括**脱敏**、**资料整理**、**机翻检查**——逐门课程完整跟踪，详见：

👉 **[📋 题库检查清单 CHECKLIST.md](CHECKLIST.md)**

---

## 📄 文件说明

| 位置 | 说明 |
|:-----|:-----|
| `学期/课程/pdf/` | 📑 该课程的 PDF 资料汇总 |
| `学期/课程/*.docx`、`*.doc` | ✏️ 可编辑原件，便于修改与再加工 |
| `学期/课程/*.pdf` | 📎 原始 PDF（部分学期保留，与 `pdf/` 内同名文件字节一致） |
| `学期/课程/README.md` | ℹ️ 课程说明（20 门课程均已具备） |
| `学期/README.md` | 🗓️ 学期说明（目前 `3-first-semester` 具备） |

---

## 📅 更新记录

### 2026-11-14

- 🗂️ **目录重构**：移除 `question-bank` 外层，学期目录上移至仓库根，`pdf/` 下沉到每门课程内
- 📎 **补齐示例排版**：`3-first-semester` 的学科根补回原始 PDF 副本（数据挖掘 8 份、编译原理 1 份），并新增学期 `README.md`
- ✏️ **原件归位**：86 份 `.docx` 与 61 份 `.doc` 全部落在学科根目录，与 PDF 并存
- 🔒 **脱敏**：PDF 元数据与 Word 属性清理，学科根副本与 `pdf/` 内文件逐字节一致
- 📝 **README 重写**：统计改为实测值，链接改为仓库内相对路径，补充「如何检索」「学期构成」本节

---

## 🚀 如何贡献

1. 🍴 **Fork** 本仓库
2. 📁 按「学期 / 课程」放置文件：PDF 放 `pdf/`，可编辑原件放学科根
3. 📝 补一份课程 `README.md`，说明教材与范围
4. ✅ 确认无个人隐私信息后提交（见 [REDACTION.md](REDACTION.md)）
5. 🔁 发起 **Pull Request**

详细规范见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## ⚠️ 注意事项

- 📚 本仓库所有资料**仅供学习参考**，请勿用于商业用途。
- 🔒 上传前请确保**不包含个人隐私信息**（如学号、姓名等），并清理文档元数据。
- 🙏 若资料涉及版权问题，请联系维护者删除。

---

<div align="center">

**⭐ 如果这个仓库对你有帮助，欢迎点个 Star！**

_Made with ❤️ by TZU 计算机专业同学_

</div>
