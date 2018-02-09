# Create a session connected to the Exchange Management Shell
$session = New-PSSession -ConfigurationName Microsoft.Exchange -ConnectionUri http://exch1.ki7hds.com/Powershell/ -Authentication Kerberos -Credential $userCredential

# Import the session
Import-PSSession $session

# Enable all users in the AWS OU
Get-User -OrganizationalUnit "AWS OU" | Enable-Mailbox -Database "DB1"

# Create and apply a new Email Address Policy
New-EmailAddressPolicy -Name 'Primary Address Policy' -IncludedRecipients AllRecipients -EnabledEmailAddressTemplates "SMTP:%1g%s@ki7hds.com" -Priority 1 -Confirm:$false
# Apply the new policy
Update-EmailAddressPolicy -Identity 'Primary Address Policy' -Confirm:$false







