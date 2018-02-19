param(
     [string]
     [Parameter(Mandatory=$true,Position=0)]
     $DomainDNSName,

     [string]
     [Parameter(Position=1)]
     $OrganizationalUnit='AWS OU'
)

# Translate the domain name into LDAP format
$DomainName = $DomainDNSName -replace '\.',',DC='
$DomainName = 'DC=' + $DomainName

# Create global groups to hold user accounts
New-ADGroup -Name 'Admins' -SamAccountName 'Admins' -GroupCategory Security -GroupScope Global -DisplayName 'Admins' -Path "OU=$OrganizationalUnit,$DomainName"
Add-ADGroupMember -Identity 'Admins' -Members 'Domain Admins','Administrator'

New-ADGroup -Name 'Executives' -SamAccountName 'Executives' -GroupCategory Security -GroupScope Global -DisplayName 'Executives' -Path "OU=$OrganizationalUnit,$DomainName"  

New-ADGroup -Name 'Managers' -SamAccountName 'Managers' -GroupCategory Security -GroupScope Global -DisplayName 'Managers' -Path "OU=$OrganizationalUnit,$DomainName"  

New-ADGroup -Name 'All Employees' -SamAccountName 'AllEmployees' -GroupCategory Security -GroupScope Global -DisplayName 'All Employees' -Path "OU=$OrganizationalUnit,$DomainName" 
Add-ADGroupMember -Identity  'AllEmployees' -Members 'Admins','Executives','Managers'  


# Create domain local groups to assign permissions
New-ADGroup -Name 'Admins-FullControl' -SamAccountName 'Admins-FullControl' -GroupCategory Security -GroupScope DomainLocal -DisplayName 'Admins-FullControl' -Path "OU=$OrganizationalUnit,$DomainName"  
Add-ADGroupMember -Identity  'Admins-FullControl' -Members 'Admins'  

New-ADGroup -Name 'Admins-FullAccess' -SamAccountName 'Admins-FullAccess' -GroupCategory Security -GroupScope DomainLocal -DisplayName 'Admins-FullAccess' -Path "OU=$OrganizationalUnit,$DomainName" 
Add-ADGroupMember -Identity 'Admins-FullAccess' -Members 'Admins'  

New-ADGroup -Name 'Admins-Modify' -SamAccountName 'Admins-Modify' -GroupCategory Security -GroupScope DomainLocal -DisplayName 'Admins-Modify' -Path "OU=$OrganizationalUnit,$DomainName" 
Add-ADGroupMember -Identity 'Admins-Modify' -Members 'Admins'  

New-ADGroup -Name 'All Employees-Read' -SamAccountName 'AllEmployees-Read' -GroupCategory Security -GroupScope DomainLocal -DisplayName 'All Employees-Read' -Path "OU=$OrganizationalUnit,$DomainName" 
Add-ADGroupMember -Identity 'AllEmployees-Read' -Members 'AllEmployees'  

New-ADGroup -Name 'All Employees-Modify' -SamAccountName 'AllEmployees-Modify' -GroupCategory Security -GroupScope DomainLocal -DisplayName 'All Employees-Modify' -Path "OU=$OrganizationalUnit,$DomainName" 
Add-ADGroupMember -Identity 'AllEmployees-Modify' -Members 'AllEmployees'  

New-ADGroup -Name 'All Employees-Change' -SamAccountName 'AllEmployees-Change' -GroupCategory Security -GroupScope DomainLocal -DisplayName 'All Employees-Change' -Path "OU=$OrganizationalUnit,$DomainName" 
Add-ADGroupMember -Identity 'AllEmployees-Change' -Members 'AllEmployees'  

New-ADGroup -Name 'Executives-Modify' -SamAccountName 'Executives-Modify' -GroupCategory Security -GroupScope DomainLocal -DisplayName 'Executives-Modify' -Path "OU=$OrganizationalUnit,$DomainName" 
Add-ADGroupMember -Identity 'Executives-Modify' -Members 'Executives'  

New-ADGroup -Name 'Managers-Modify' -SamAccountName 'Managers-Modify' -GroupCategory Security -GroupScope DomainLocal -DisplayName 'Managers-Modify' -Path "OU=$OrganizationalUnit,$DomainName" 
Add-ADGroupMember -Identity 'Managers-Modify' -Members 'Managers'  