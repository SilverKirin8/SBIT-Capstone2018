$newDisk = Get-Disk 1
$newDisk | Set-Disk -IsOffline $false
$newDisk | Initialize-Disk -PartitionStyle GPT
$newDisk | New-Partition -DriveLetter z -UseMaximumSize
Get-Volume -DriveLetter z | Format-Volume -FileSystem NTFS -NewFileSystemLabel 'SBIT File Shares'