# Script configures a DFS Namespace and DFS Replication between two servers
# Should change params to require an array of server names to allow for scalability
    # Will skip for now in interest of time, will refactor later (if possible)
param(
    [string]
    [Parameter(Mandatory=$true)]
    $DomainName,

    [string]
    [Parameter(Mandatory=$true)]
    $Fs1NetBiosName,

    [string]
    [Parameter(Mandatory=$true)]
    $Fs2NetBiosName
)

$rGroupName = 'SBITReplicationGroup'
$rFolderName = 'SBITReplicatedFolder'
$sharedFolderPath = 'z:\AWSShares'

# Create Namespace
New-DfsnRoot -Path "\\$DomainName\AWSShares" -TargetPath "\\$Fs1NetBiosName.$DomainName\AWSShares" -Type DomainV2 ` 
-Description 'Namespace for file servers created by SBIT.' -EnableAccessBasedEnumeration $true

# Add additional server(s) to the namespace
New-DfnsRootTarget -Path "\\$DomainName\AWSShares" -TargetPath "\\$Fs2NetBiosName.$DomainName\AWSShares"

# Create Replication group, folder, and add computers to group
New-DfsReplicationGroup -DomainName $DomainName -GroupName $rGroupName | ` 
New-DfsReplicatedFolder -FolderName $rFolderName -DomainName $DomainName | ` 
Add-DfsrMember -DomainName $DomainName -ComputerName "$Fs1NetBiosName.$DomainName","$Fs2NetBiosName.$DomainName"

# Add replication connections (tells servers which members should send/receive replication data)
Add-DfsrConnection -DomainName $DomainName -GroupName $rGroupName ` 
-SourceComputerName "$Fs1NetBiosName.$DomainName" -DestinationComputerName "$Fs2NetBiosName.$DomainName"

# Set the membership and content paths to be replicated
Set-DfsrMembership -GroupName $rGroupName -FolderName $rFolderName -ComputerName "$Fs1NetBiosName.$DomainName" -ContentPath $sharedFolderPath –PrimaryMember $true
Set-DfsrMembership -GroupName $rGroupName -FolderName $rFolderName -ComputerName "$Fs2NetBiosName.$DomainName" -ContentPath $sharedFolderPath