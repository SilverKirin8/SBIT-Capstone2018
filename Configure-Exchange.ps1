# Create a session connected to the Exchange Management Shell
$session = New-PSSession -ConfigurationName Microsoft.Exchange -ConnectionUri http://exch1.ki7hds.com/Powershell/ -Authentication Kerberos -Credential

# Import the session
Import-PSSession $session

# Enable all users in the AWS OU
Get-User -OrganizationalUnit "AWS OU" | Enable-Mailbox -Database "DB1"








