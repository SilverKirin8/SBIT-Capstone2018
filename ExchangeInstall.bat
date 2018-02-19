powershell.exe -Command "c:\cfn\scripts\Mount-Exchange.ps1"
timeout /t 30 /nobreak
powershell.exe -Command Start-Process powershell.exe '-NoProfile -Command "c:\cfn\scripts\Prepare-ActiveDirectory.ps1"' -Verb RunAs
timeout /t 420 /nobreak
powershell.exe -Command Start-Process powershell.exe '-NoProfile -Command "c:\cfn\scripts\Install-Exchange.ps1"' -Verb RunAs
timeout /t 3900 /nobreak
powershell.exe -Command Start-Process powershell.exe '-NoProfile -Command "Dismount-DiskImage -ImagePath c:\cfn\downloads\ExchangeServer2016-x64-cu8.iso"' -Verb RunAs