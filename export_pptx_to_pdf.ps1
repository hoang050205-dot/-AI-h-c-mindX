$tempDir = [System.IO.Path]::GetTempPath()
$tempPptx = Join-Path $tempDir "vinamilk_temp.pptx"
$tempPdf = Join-Path $tempDir "vinamilk_temp.pdf"

$origPptx = (Resolve-Path "outputs\reports\Vinamilk_Supply_Chain_Operations_PhamMinhHoang.pptx").Path
$finalPdf = (Join-Path (Split-Path $origPptx) "Vinamilk_Supply_Chain_Operations_PhamMinhHoang.pdf")
$finalPdfV2 = (Join-Path (Split-Path $origPptx) "Vinamilk_Supply_Chain_Operations_PhamMinhHoang_v2.pdf")
$exportDir = Join-Path (Split-Path $origPptx) "slide_previews"

Write-Output "Copying to temp: $tempPptx"
Copy-Item -Path $origPptx -Destination $tempPptx -Force

Write-Output "Opening PowerPoint COM..."
$pptApp = New-Object -ComObject PowerPoint.Application

try {
    $presentation = $pptApp.Presentations.Open($tempPptx, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    
    Write-Output "Exporting to Temp PDF: $tempPdf"
    # 32 = ppSaveAsPDF
    $presentation.SaveAs($tempPdf, 32)
    
    Write-Output "Exporting slide preview images..."
    for ($i = 1; $i -le $presentation.Slides.Count; $i++) {
        $slidePng = Join-Path $exportDir "slide_$i.png"
        $presentation.Slides.Item($i).Export($slidePng, "PNG", 1920, 1080)
    }

    $presentation.Close()

    # Copy to v2 first (always succeeds even if v1 is locked by PDF viewer)
    Copy-Item -Path $tempPdf -Destination $finalPdfV2 -Force
    Write-Output "SUCCESS: Saved to $finalPdfV2"

    try {
        Copy-Item -Path $tempPdf -Destination $finalPdf -Force
        Write-Output "SUCCESS: Also overwritten $finalPdf"
    } catch {
        Write-Output "Note: Original PDF is currently opened in reader, saved as v2 PDF instead."
    }

} catch {
    Write-Output "Error: $_"
} finally {
    $pptApp.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($pptApp) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
    
    if (Test-Path $tempPptx) { Remove-Item $tempPptx -Force }
    if (Test-Path $tempPdf) { Remove-Item $tempPdf -Force }
}
