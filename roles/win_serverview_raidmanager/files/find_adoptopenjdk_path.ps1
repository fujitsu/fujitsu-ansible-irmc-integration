# PowerShell Script to Find AdoptOpenJDK Installation Path

# NOTE: Limited to AdoptOpenJDK. (Not applicable to other OpenJDKs).

$registryBasePath = "HKLM:\SOFTWARE\Eclipse Adoptium"
$jdkKeys = Get-ChildItem -Path $registryBasePath -ErrorAction SilentlyContinue

$installationPath = $null
$latestVersion = $null

# NOTE:
#  AdoptOpenJDK's installation path is stored in the registry below:
#   "HKEY_LOCAL_MACHINE\SOFTWARE\Eclipse Adoptium\{CATEGORY}\{VERSION}\hotspot\MSI\Path"
#   "{CATEGORY}" is "JRE" or "JDK".
#   "{VERSION}" is a version (eg "8.0.422.5").

# Find the newest version of JDK or JRE installation paths
foreach ($jdkKey in $jdkKeys) {
    $jdkSubKeys = Get-ChildItem -Path $jdkKey.PSPath -ErrorAction SilentlyContinue
    foreach ($subKey in $jdkSubKeys) {
        $hotspotPath = "$($subKey.PSPath)\hotspot\MSI"
        if (Test-Path $hotspotPath) {
            $pathValue = (Get-ItemProperty -Path $hotspotPath).Path
            if ($pathValue -ne $null) {
                if ($latestVersion -eq $null -or [string]::Compare($subKey.PSChildName, $latestVersion) -gt 0) {
                    $installationPath = $pathValue
                    $latestVersion = $subKey.PSChildName
                }
            }
        }
    }
}

if ($installationPath -ne $null) {
    Write-Output $installationPath
    exit 0
} else {
    Write-Error "AdoptOpenJDK is not installed."
    exit 1
}
