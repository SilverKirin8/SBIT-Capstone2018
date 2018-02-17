powershell.exe -Command "c:\cfn\scripts\Mount-Exchange.ps1"
powershell.exe -Command Start-Process powershell.exe '-NoProfile -Command "c:\cfn\scripts\Prepare-ActiveDirectory.ps1"' -Verb RunAs
timeout /t 600 /nobreak
powershell.exe -Command Start-Process powershell.exe '-NoProfile -Command "c:\cfn\scripts\Install-Exchange.ps1"' -Verb RunAs