try {
    $ppt = New-Object -ComObject PowerPoint.Application
    Write-Output "PowerPoint COM Available"
    $ppt.Quit()
} catch {
    Write-Output "PowerPoint COM Not Available"
}
