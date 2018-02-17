param(
    [string]
    [Parameter(Mandatory=$true)]
    $SmtpServer, #EXCH1.ki7hds.com

    [string]
    [Parameter(Mandatory=$true)]
    $AdminEmailAddress, #RMcClure@ki7hds.com

    [string]
    [Parameter(Mandatory=$true)]
    $VolumeSize, #10GB

    [string]
    [Parameter(Mandatory=$true)]
    $QuotaPath #c:\SBIT
)

Set-FsrmSetting -SmtpServer $SmtpServer -AdminEmailAddress $AdminEmailAddress

$Action = New-FsrmAction -Type Email -MailTo $AdminEmailAddress -RunLimitInterval 120 -Subject "Warning: Running Out of Disk Space on FS1!" -Body "You are about to reach the end of your available storage on FS1. You can add more storage or delete old, unused files." -Confirm:$false
$Threshold = New-FsrmQuotaThreshold -Percentage 90 -Action $Action -Confirm:$false
New-FSRMQuota -Path $QuotaPath -Size ($VolumeSize/1) -Threshold $Threshold -Description "This quota monitors the shared SBIT volume and warns when the volume has only 10% free space." -Confirm:$false





