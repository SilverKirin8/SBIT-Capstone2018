import boto3
import re
import getpass

MAX_DCS=8
MIN_DCS=2
MAX_VOLUME_SIZE=1500
MIN_VOLUME_SIZE=1

SECTION_SEPARATOR = '#'*60

networkStackName = 'CapstoneNetworkStack'
adStackName = 'CapstoneADStack'
fsStackName = 'CapstoneFSStack'

#Should change these in the future to let user define all of this, skipping for now to save time
fs1NetBIOSName = 'FS1'
fs2NetBIOSName = 'FS2'

'''
DON'T FORGET TO UPDATE CLOUDFORMATION TEMPLATE LOCATIONS
(Either replace references to or instantiate following vars)
'''
vpcTemplateUrl = 'https://s3.us-east-2.amazonaws.com/cf-templates-65d2poexw312-us-east-2/2018022aO1-NetworkStackForCapstone.yaml7ruxj7sxky9'
adTemplateUrl = 'https://s3.us-east-2.amazonaws.com/cf-templates-65d2poexw312-us-east-2/2018029g87-ADStackForCapstone.yaml003x5k82ixi5v'
fsTemplateUrl = 'https://s3.us-east-2.amazonaws.com/cf-templates-65d2poexw312-us-east-2/2018029XbM-FSStackForCapstone.yamlpsrseqqsm4h'

#EC2 object allows connection and manipulation of AWS EC2 resource types
ec2 = boto3.resource('ec2')
#CloudFormation client allows creation of AWS resources in a stack by using CloudFormation templates
cloudFormationClient = boto3.client('cloudformation')
#ssmClient allows remote command execution against EC2 instances
ssmClient = boto3.client('ssm')

def main():
    #Welcome message
    print(SECTION_SEPARATOR)
    print('Welcome to SBIT: The Small Business IT automation suite!')
    print('Please enter the following information and we\'ll get started.\n\n')

    #Gather data from user
    userDomainName = getDomainName('Enter your Domain Name (Ex. "example.com"): ')
    userDomainNetBIOSName = getNetBiosName('Enter the NetBIOS name of the domain (Ex. "EXAMPLE"): ')
    userKeyPair = getKeyPairName('Enter the name of the Key Pair (used when accessing instances): ')
    userNumDcs = getNumDcs('How many Domain Controllers? [Leave blank to use default of 2]: ')
    userNumFileServers = getNumFileServers('How many File Servers? [Leave blank to use default of 2]: ')
    userVolumeSize = getVolumeSize('How much storage would you like (in GiBs) on file servers?: ')
    userDcInstanceType = getInstanceType('Enter the instance type to use for Domain Controllers [Default: t2.micro]: ')
    userFsInstanceType = getInstanceType('Enter the instance type to use for File Servers [Default: t2.micro]: ')
    userExchangeInstanceType = getInstanceType('Enter the instance type to use for Exchange servers [Default: t2.micro]: ')
    userMiscInstanceType = getInstanceType('Enter the instance type to use for all other servers (VPN, 802.1x Security, Certificate Authority) [Default: t2.micro]: ')
    userDomainAdminUsername = getUsername('Enter a username for the domain administrator account (separate account from the default "Administrator" account): ')
    userDomainAdminPassword = getPassword('Enter a password for the domain administrator account: ')
    userRestoreModePassword = getPassword('Enter a password for Active Directory Restore Mode: ')

    #Build VPC and other networking resources
#    buildNetworkStack()

	#Build Active Directory and Domain Controllers
#    buildADStack(networkStackName, userDomainName, userDomainNetBIOSName, userDomainAdminUsername, userDomainAdminPassword, userRestoreModePassword, userDcInstanceType, userKeyPair)
	
	#Build File Servers and configure a Namespace and Replication
    buildFSStack(networkStackName, adStackName, userDomainName, userDomainNetBIOSName, userDomainAdminUsername, userDomainAdminPassword, userFsInstanceType, userVolumeSize, userKeyPair)
    #Build instances...

#Build VPC and other networking resources
def buildNetworkStack():
    #vpcStackWaiter can be called to halt script execution until the specified stack is finished executing/building
    vpcStackWaiter = cloudFormationClient.get_waiter('stack_create_complete')
    
    #Print estimated time to completion
    print('\n' + SECTION_SEPARATOR)
    print('Building AWS Networking...')
    print('Estimated time to completion: ~2-5 min.')
    
    vpcStackResponse = cloudFormationClient.create_stack(
        StackName = networkStackName,
        TemplateURL = vpcTemplateUrl,
    )
    vpcStackWaiter.wait(StackName=vpcStackResponse['StackId'])

    print('AWS Networking... Build Complete!')

#Build first two Domain Controllers in AD domain
def buildADStack(networkStackName, userDomainName, userDomainNetBIOSName, userDomainAdminUsername, userDomainAdminPassword, userRestoreModePassword, userDcInstanceType, userKeyPair):
	#adStackWaiter can be called to halt script execution until the specified stack is finished building
	adStackWaiter = cloudFormationClient.get_waiter('stack_create_complete')
	
	#Print estimated time to completion
	print('\n' + SECTION_SEPARATOR)
	print('Building Active Directory...')
	print('Estimated time to completion: ~30 min.')
	
	adStackResponse = cloudFormationClient.create_stack(
		StackName = adStackName,
		TemplateURL = adTemplateUrl,
		Parameters=[
			{
				'ParameterKey' : 'NetworkStackName',
				'ParameterValue' : networkStackName
			},
			{
				'ParameterKey' : 'DomainDNSName',
				'ParameterValue' : userDomainName
			},
			{
				'ParameterKey' : 'DomainNetBIOSName',
				'ParameterValue' : userDomainNetBIOSName
			},
			{
				'ParameterKey' : 'DomainAdminUser',
				'ParameterValue' : userDomainAdminUsername
			},
			{
				'ParameterKey' : 'DomainAdminPassword',
				'ParameterValue' : userDomainAdminPassword
			},
			{
				'ParameterKey' : 'RestoreModePassword',
				'ParameterValue' : userRestoreModePassword
			},
			{
				'ParameterKey' : 'DCInstanceType',
				'ParameterValue' : userDcInstanceType
			},
			{
				'ParameterKey' : 'KeyPair',
				'ParameterValue' : userKeyPair
			},
		],
	)
	adStackWaiter.wait(StackName=adStackResponse['StackId'])
	print('Active Directory... Build Complete!')

#Build first two File Servers in AD Domain
def buildFSStack(networkStackName, adStackName, userDomainName, userDomainNetBIOSName, userDomainAdminUsername, userDomainAdminPassword, userFsInstanceType, userVolumeSize, userKeyPair):
    #fsStackWaiter can be called to halt script execution until the specified stack is finished building
    fsStackWaiter = cloudFormationClient.get_waiter('stack_create_complete')
    
    #Print estimated time to completion
    print('\n' + SECTION_SEPARATOR)
    print('Building File Servers...')
    print('Estimated time to completion: ~10 min.')
    
    fsStackResponse = cloudFormationClient.create_stack(
        StackName = fsStackName,
        TemplateURL = fsTemplateUrl,
        Parameters=[
            {
                'ParameterKey' : 'NetworkStackName',
                'ParameterValue' : networkStackName
            },
            {
                'ParameterKey' : 'ADStackName',
                'ParameterValue' : adStackName
            },
            {
                'ParameterKey' : 'DomainDNSName',
                'ParameterValue' : userDomainName
            },
            {
                'ParameterKey' : 'DomainNetBIOSName',
                'ParameterValue' : userDomainNetBIOSName
            },
            {
                'ParameterKey' : 'DomainAdminUser',
                'ParameterValue' : userDomainAdminUsername
            },
            {
                'ParameterKey' : 'DomainAdminPassword',
                'ParameterValue' : userDomainAdminPassword
            },
            {
                'ParameterKey' : 'FSInstanceType',
                'ParameterValue' : userFsInstanceType
            },
            {
                'ParameterKey' : 'FSVolumeSize',
                'ParameterValue' : userVolumeSize
            },
            {
                'ParameterKey' : 'KeyPair',
                'ParameterValue' : userKeyPair
            },
        ],
    )
    fsStackWaiter.wait(StackName=fsStackResponse['StackId'])
    
    #Send a command to the first File Server, telling it to execute the Configure-Dfs script
    '''ssmResponse = ssmClient.send_command(
        Targets=[
            {
                'Key': 'tag:Name',
                'Values': [
                    fs1NetBIOSName,
                ]
            },
        ],
        DocumentName='AWS-RunPowerShellScript',
        TimeoutSeconds=3600,
        Comment='Execute script to configure DFS Namespace and DFS Replication.',
        Parameters={
            'commands': [
                ("Invoke-Command -Session (New-PSSession -Credential (New-Object System.Management.Automation.PSCredential('%s\%s',(ConvertTo-SecureString '%s' -AsPlainText -Force)))) -Script { c:\cfn\scripts\Configure-Dfs.ps1 -DomainName '%s' -Fs1NetBiosName '%s' -Fs2NetBiosName '%s' }" % (userDomainNetBIOSName, userDomainAdminUsername, userDomainAdminPassword, userDomainName, fs1NetBIOSName, fs2NetBIOSName)),
            ]
        }
    )'''
    
    print('File Servers... Build Complete!')

#Prompt for and validate the Domain Name
def getDomainName(message):
    validDomain = False
    #Loop until the user enters a valid domain
    while(not validDomain):
        userDomain = input(message)
        #The domain can include upper and lowercase letters, numbers, and
        #dashes (-), as long as the dashes are not the first or last 
        #character. Ex. "-example.com" = invalid, "ex-ample.com" = valid.
        regex = re.compile('^[A-Za-z0-9]([A-Za-z0-9-]*\.)+[A-Za-z0-9]+$')
        if(regex.match(userDomain)):
            validDomain = True
        else:
            print('Invalid domain. Please enter a valid domain. Domain names must contain only upper and lowercase letters and numbers. Hyphens or dashes (-) are allowed only if they are NOT the first or last character.')
    return userDomain
	
#Prompt for the NetBIOS name of the domain
def getNetBiosName(message):
    validNetBiosName = False
    #Loop until the user enters a valid NetBIOS name
    while(not validNetBiosName):
        userNetBiosName = input(message)
        #The domain NetBIOS name is typically the domain name without the root domain
        # Ex. example.com => EXAMPLE
        regex = re.compile('^[A-Za-z0-9\-]+$')
        if(regex.match(userNetBiosName) and len(userNetBiosName) >= 1 and len(userNetBiosName) <= 15):
            validNetBiosName = True
        else:
            print('Invalid name. Domain NetBIOS names are typically the domain name without the root (Ex. example.com => EXAMPLE) and computer NetBIOS names are a short name for the computer. NetBIOS names must be between 1 and 15 characters long and can have upper and lowercase letters, numbers, and hyphens (-).')
    return userNetBiosName

#Prompt for the name of the Key Pair to use for accessing instances
def getKeyPairName(message):
    #Compile a list of all available Key Pair Names
    keyPairs = ec2.key_pairs.all()
    validPairNames = []
    for pair in keyPairs:
        validPairNames.append(pair.name)

    validKeyPairName = False
    #Prompt for and validate Key Pair Name
    while(not validKeyPairName):
        userKeyPairName = input(message)
        if(not userKeyPairName in validPairNames):
            print('Please, enter the name of the key pair you created in AWS.')
        else:
            validKeyPairName = True
    return userKeyPairName

#Prompt for the number of Domain Controllers
#Users must enter a number between 2 and 8, the default is 2
def getNumDcs(message):
    validNum = False
    #Loop until the user enters a number between 2 and 8, inclusive
    while(not validNum):
        userNumDcs = input(message)
        #Ensure the user enters a number between 2 and 8, or leaves the input blank
        regex = re.compile('(^$)|^[2-8]$')
        if(not regex.match(userNumDcs)):
            print('Please, enter a number between 2 and 8.')
        else:
            validNum = True
    #Return the default if the user enters nothing
    if(userNumDcs == ''):
        return MIN_DCS
    else:
        return int(userNumDcs)

#Prompt for the number of File Servers
#Users must enter a number between 2 and 4, the default is 2
def getNumFileServers(message):
    validNum = False
    #Loop until the user enters a number between 2 and 4, inclusive
    while(not validNum):
        userNumFileServers = input(message)
        #Ensure the user enters a number between 2 and 4, or leaves the input blank
        regex = re.compile('(^$)|^[2-4]$')
        if(not regex.match(userNumFileServers)):
            print('Please, enter a number between 2 and 4.')
        else:
            validNum = True
    #Return the default if the user enters nothing
    if(userNumFileServers == ''):
        return MIN_DCS
    else:
        return int(userNumFileServers)

#Prompt for and validate the size of drives to be added to file servers
def getVolumeSize(message):
    validSize = False
    #Loop until a valid volume size is entered
    while(not validSize):
        userVolumeSize = input(message)
        #Validate that the number entered is positive and between MAX_VOLUME_SIZE and MIN_VOLUME_SIZE
        try:
            if(int(userVolumeSize) > MAX_VOLUME_SIZE or int(userVolumeSize) < MIN_VOLUME_SIZE):
                raise ValueError
            else:
                validSize = True
        except ValueError:
            print('Invalid input. Please enter a number between %d and %d.' % (MIN_VOLUME_SIZE,MAX_VOLUME_SIZE))
    return userVolumeSize

#Prompt for and validate the instance type for instances
def getInstanceType(message):
    validTypes = ["t2.micro","t2.small","t2.medium","t2.large","t2.xlarge","t2.2xlarge","m5.large","m5.xlarge","m5.2xlarge","m5.4xlarge"]
    validType = False
    #Loop until a valid instance type is entered
    while(not validType):
        userInstanceType = input(message)
        if(userInstanceType in validTypes):
            validType = True
        else:
            print('Invalid input. Please enter one of the following instance types:')
            for instanceType in validTypes[:-2]:
                print('%s, ' % (instanceType), end='')
            print(validTypes[-1])
    return userInstanceType
	
#Prompt for usernames for AD users
def getUsername(message):
    validUsername = False
    #Loop until the user enters a valid username
    while(not validUsername):
        userName = input(message)
        #Ensure the username has no symbols
        regex = re.compile('[a-zA-Z0-9]*')
        if(len(userName) >= 3 and len(userName) <= 25 and regex.match(userName)):
            validUsername = True
        else:
            print('Invalid username. Usernames can contain upper and lowercase letters and numbers. Usernames should be between 3 and 25 characters in length.')
    return userName

#Prompt for and validate the AD admin password
def getPassword(message):
    validPassword = False
    #Loop until the user enters a password that is at least 8 characters and
    #contains at least one upper and lowercase letter, number, and symbol
    while(not validPassword):
        userPassword = getpass.getpass(message)
        #Check to see if password meets length and complexity requirements
        if(
            (len(userPassword) >= 8) and
            (re.search(r'[A-Z]', userPassword) is not None) and #Checks for Uppercase
            (re.search(r'[a-z]', userPassword) is not None) and #Checks for Lowercase
            (re.search(r'\d', userPassword) is not None) and #Checks for Numbers
            (re.search(r"[!#$%&'()*+,-./[\\\]^_`{|}~"+r'":;<=>?@]', userPassword) is not None) #Checks for Symbols
           ):
            validPassword = True
        else:
            print('Invalid password. Password should be 8 characters or more and contain an uppercase letter, lowercase letter, number, and symbol.')
    return userPassword



if __name__ == "__main__":
    main()
