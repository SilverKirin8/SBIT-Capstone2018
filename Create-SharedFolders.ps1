# Get the directory path and rules to add to the ACL

param(
	[String]
	$DriveLetter = 'c:'
)

function Modify-AclRules {
    <# Adds the rules specified in the parameter '-rules' to the ACL of the directory found at '-path' #>
    param(
        [String]
        [Parameter(Position=0,Mandatory=$true)]
        $path, 
        
        [Object[]]
        [Parameter(Position=1,Mandatory=$true)]
        $rules
    )
    
    # Get the ACL
    $acl = (Get-Item $path).GetAccessControl('Access');

    # Add ACEs to ACL
    Foreach($rule in $rules){ $acl.SetAccessRule($rule); }

    # Remove insecure ACEs
    $acl.Access | ForEach-Object {
        if($_.IdentityReference -like 'BUILTIN\Administrators' -or $_.IdentityReference -like 'BUILTIN\Users'){
            $acl.RemoveAccessRule($_)
        }
    }
    # Apply the ACL to the directory
    $acl | Set-Acl $path
}

<# Remove inheritance
    While inheritance is active, inherited rules CANNOT be 
    removed. Therefore, inheritance has to be removed and 
    the ACL applied before ACE rules can be removed. The 
    ACL MUST be applied before the inheritance removal 
    takes effect.
#>
function Remove-Inheritance {
    param(
        [string]
        [Parameter(Position=0,Mandatory=$True)]
        $path # The directory path to remove inheritance
    )

    $acl = (Get-Item $path).GetAccessControl('Access');
    $acl.SetAccessRuleProtection($true,$true);
    $acl | Set-Acl $path;
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

$rootSharePath = "$DriveLetter\AWSShares"

<# Create a new folder on the root of the new, second drive #>
mkdir $rootSharePath

# Remove inheritance from root folder
Remove-Inheritance $rootSharePath

# Build array of ACEs to add to the ACL
$rules = @();
$rules += New-Object System.Security.AccessControl.FileSystemAccessRule('Admins-FullControl','FullControl','None','None','Allow')
$rules += New-Object System.Security.AccessControl.FileSystemAccessRule('AllEmployees-Read','Read','None','None','Allow')

# Modify the permissions of the root folder
Modify-AclRules -path $rootSharePath -rules $rules


<# Create 'Admins' directory inside of root folder #>
$adminsPath = "$rootSharePath\Admins"
mkdir $adminsPath

# Remove inheritance from 'Admins'
Remove-Inheritance $adminsPath

#Build array of ACEs to add to ACL
$rules = @()
$rules += New-Object System.Security.AccessControl.FileSystemAccessRule('Admins-Modify','Modify','ContainerInherit,ObjectInherit','None','Allow')

# Modify permissions of 'Admins'
Modify-AclRules -path $adminsPath -rules $rules


<# Create 'Executives' directory inside of root folder #>
$execPath = "$rootSharePath\Executives"
mkdir $execPath

# Remove inheritance from 'Executives'
Remove-Inheritance $execPath

#Build array of ACEs to add to ACL
$rules = @()
$rules += New-Object System.Security.AccessControl.FileSystemAccessRule('Executives-Modify','Modify','ContainerInherit,ObjectInherit','None','Allow')

# Modify permissions of 'Executives'
Modify-AclRules -path $execPath -rules $rules


<# Create 'Managers' directory inside of root folder #>
$managerPath = "$rootSharePath\Managers"
mkdir $managerPath

# Remove inheritance from 'Managers'
Remove-Inheritance $managerPath

#Build array of ACEs to add to ACL
$rules = @()
$rules += New-Object System.Security.AccessControl.FileSystemAccessRule('Managers-Modify','Modify','ContainerInherit,ObjectInherit','None','Allow')

# Modify permissions of 'Managers'
Modify-AclRules -path $managerPath -rules $rules


<# Create 'All Employees' directory inside of root folder #>
$empsPath = "$rootSharePath\All Employees"
mkdir $empsPath

# Remove inheritance from 'All Employees'
Remove-Inheritance $empsPath

#Build array of ACEs to add to ACL
$rules = @()
$rules += New-Object System.Security.AccessControl.FileSystemAccessRule('AllEmployees-Modify','Modify','ContainerInherit,ObjectInherit','None','Allow')

# Modify permissions of 'All Employees'
Modify-AclRules -path $empsPath -rules $rules

<# Share the root folder #>
New-SMBShare –Name “AWSShares” –Path $rootSharePath `
    –FullAccess "Admins-FullAccess"  `
    -ChangeAccess "AllEmployees-Change" `
    -FolderEnumerationMode AccessBased
