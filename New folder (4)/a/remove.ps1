$rootPath = "C:\Users\Desktop\Documents\Paradox Interactive\Hearts of Iron IV\mod\tfb"
$files = Get-ChildItem -Path $rootPath -Filter "*.txt" -Recurse

# UTF-8 ohne BOM Encoding erzwingen
$encoding = New-Object System.Text.UTF8Encoding($false)

foreach ($file in $files) {
    # Dateiinhalt einlesen (als String, ohne Formatierung durch PowerShell-Pipeline)
    $rawContent = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    
    # Regex, der nur den Hashtag-Kommentar-Block matcht
    # Erhält Zeilenumbrüche (\r\n oder \n) und restlichen Text exakt
    $updatedContent = $rawContent -replace '#.*', ''
    
    # Datei schreiben und sicherstellen, dass nichts null ist
    if ($null -ne $updatedContent) {
        [System.IO.File]::WriteAllText($file.FullName, $updatedContent, $encoding)
    }
}