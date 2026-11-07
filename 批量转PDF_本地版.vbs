Option Explicit
On Error Resume Next
' Local batch Word -> PDF. No network, no upload.
' Double-click to run. Output goes to a PDF\ subfolder beside each Word file.
' Set SKIP_EXISTING = False to re-convert everything.
Const wdExportFormatPDF = 17
Dim SKIP_EXISTING : SKIP_EXISTING = True
Dim fso, base, logPath, logF, app, progs, prog, oDoc
Dim doneCnt, skipCnt, errCnt
doneCnt = 0 : skipCnt = 0 : errCnt = 0

Set fso = CreateObject("Scripting.FileSystemObject")
base = fso.GetParentFolderName(WScript.ScriptFullName)
logPath = base & "\convert_log.txt"
Set logF = fso.CreateTextFile(logPath, True, True)

LogMsg "START " & Now
LogMsg "BASE  " & base

Set app = Nothing
progs = Array("Word.Application", "KWPS.Application")
For Each prog In progs
    Err.Clear
    Set app = CreateObject(prog)
    If Err.Number = 0 And Not app Is Nothing Then
        LogMsg "COM   " & prog
        Exit For
    End If
    Set app = Nothing
Next
If app Is Nothing Then
    LogMsg "FATAL No Word/WPS COM available on this machine."
    logF.Close
    WScript.Echo "No Word/WPS COM available. See convert_log.txt"
    WScript.Quit 1
End If
app.Visible = False
app.DisplayAlerts = 0

If fso.FolderExists(base & "\question-bank") Then
    WalkFolder fso.GetFolder(base & "\question-bank")
Else
    LogMsg "FATAL question-bank folder not found"
End If

app.Quit
LogMsg "DONE converted=" & doneCnt & " skipped=" & skipCnt & " errors=" & errCnt
logF.Close
WScript.Echo "Done. converted=" & doneCnt & " skipped=" & skipCnt & " errors=" & errCnt & " (see convert_log.txt)"

Sub WalkFolder(fldr)
    Dim f, sf, ext, stem, pdfDir, outPath, srcDir
    For Each f In fldr.Files
        ext = LCase(fso.GetExtensionName(f.Name))
        If (ext = "doc" Or ext = "docx" Or ext = "docm") And Left(f.Name, 1) <> "~" Then
            srcDir = fso.GetParentFolderName(f.Path)
            stem = fso.GetBaseName(f.Name)
            If SKIP_EXISTING And fso.FileExists(srcDir & "\" & stem & ".pdf") Then
                skipCnt = skipCnt + 1
                LogMsg "SKIP  " & f.Path
            Else
                pdfDir = srcDir & "\PDF"
                If Not fso.FolderExists(pdfDir) Then fso.CreateFolder pdfDir
                outPath = pdfDir & "\" & stem & ".pdf"
                Err.Clear
                Set oDoc = app.Documents.Open(f.Path, False, True)
                If Err.Number <> 0 Or oDoc Is Nothing Then
                    errCnt = errCnt + 1
                    LogMsg "ERROR open " & f.Path & " : " & Err.Description
                Else
                    Err.Clear
                    oDoc.ExportAsFixedFormat outPath, wdExportFormatPDF
                    If Err.Number <> 0 Then
                        errCnt = errCnt + 1
                        LogMsg "ERROR export " & f.Path & " : " & Err.Description
                    Else
                        doneCnt = doneCnt + 1
                        LogMsg "OK    " & outPath
                    End If
                    oDoc.Close 0
                End If
                Set oDoc = Nothing
            End If
        End If
    Next
    For Each sf In fldr.SubFolders
        WalkFolder sf
    Next
End Sub

Sub LogMsg(t)
    logF.WriteLine t
End Sub
