param(
    [string]
    [Parameter(Mandatory=$true)]
    $DriveLetter
)

$newDisk = Get-Disk 1
$newDisk | Set-Disk -IsOffline $false
$newDisk | Initialize-Disk -PartitionStyle GPT
$newDisk | New-Partition -DriveLetter $DriveLetter -UseMaximumSize
Get-Volume -DriveLetter $DriveLetter | Format-Volume -FileSystem NTFS -NewFileSystemLabel 'SBIT File Shares'