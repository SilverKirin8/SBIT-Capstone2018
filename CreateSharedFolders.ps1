<# Remove inheritance
    While inheritance is active, inherited rules CANNOT be 
    removed. Therefore, inheritance has to be removed and 
    the ACL applied before ACE rules can be removed. The 
    ACL MUST be applied before the inheritance removal 
    takes effect.
#>
$acl = (Get-Item 'c:\AWSTest').GetAccessControl('Access');
$acl.SetAccessRuleProtection($true,$true);
$acl | Set-Acl 'c:\AWSTest';

<# Remove unsecured rules #>
$acl = (Get-Item 'c:\AWSTest').GetAccessControl('Access');
# Build array of ACEs to add to the ACL
$rules = @();
$rules += New-Object System.Security.AccessControl.FileSystemAccessRule('Admins','FullControl','None','None','Allow');
$rules += New-Object System.Security.AccessControl.FileSystemAccessRule('All Employees','Read','None','None','Allow');
# Add ACEs to ACL
Foreach($rule in $rules){
    $acl.SetAccessRule($_);
}

# Remove insecure ACEs
$acl.Access | ForEach-Object {
    if($_.IdentityReference -like 'BUILTIN\Administrators' -or $_.IdentityReference -like 'BUILTIN\Users'){
        $acl.RemoveAccessRule($_)
    }
}
# Apply the ACL to the directory
$acl | Set-Acl 'c:\AWSTest'
