powershell.exe -Command Start-Process powershell.exe '-NoProfile -Command "c:\cfn\scripts\Configure-Fsrm.ps1"' -Verb RunAs
timeout /t 120 /nobreak
powershell.exe -Command Start-Process powershell.exe '-NoProfile -Command "c:\cfn\scripts\Configure-Dfs.ps1"' -Verb RunAs