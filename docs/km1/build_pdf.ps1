# Generuje diagramy (SVG) i dokumentacje KM1 w PDF.
# Uruchomienie:  powershell -ExecutionPolicy Bypass -File docs\km1\build_pdf.ps1
$ErrorActionPreference = "Stop"
$dir  = $PSScriptRoot
$html = Join-Path $dir "dokumentacja_km1.html"
$pdf  = Join-Path $dir "dokumentacja_km1.pdf"

python (Join-Path $dir "diagrams\generate.py")

$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edge)) { $edge = "C:\Program Files\Google\Chrome\Application\chrome.exe" }
$profile = Join-Path $env:TEMP "km1-pdf-profile"

if (Test-Path $pdf) { Remove-Item $pdf }
$url = "file:///" + $html.Replace('\', '/')
$args = @("--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--user-data-dir=`"$profile`"",
          "--print-to-pdf=`"$pdf`"", "`"$url`"")
Start-Process -FilePath $edge -ArgumentList $args -Wait -WindowStyle Hidden

if (Test-Path $pdf) { "PDF: $pdf" } else { throw "Nie udalo sie wygenerowac PDF" }
