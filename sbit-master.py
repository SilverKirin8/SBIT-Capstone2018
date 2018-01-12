import boto3
import re
import getpass

'''
Admin Passwords
'''
MAX_DCS=8
MIN_DCS=2
MAX_VOLUME_SIZE=1500
MIN_VOLUME_SIZE=10

ec2 = boto3.resource('ec2') #EC2 object allows connection and manipulation of AWS EC2 resource types

#Prompt for and validate the Domain Name
def getDomainName():
    validDomain = False
    #Loop until the user enters a valid domain
    while(not validDomain):
        userDomain = input('Domain Name: ')
        #The domain can include upper and lowercase letters, numbers, and
        #dashes (-), as long as the dashes are not the first or last 
        #character. Ex. "-example.com" = invalid, "ex-ample.com" = valid.
        regex = re.compile('^[A-Za-z0-9]([A-Za-z0-9-]*\.)+[A-Za-z0-9]+$')
        if(regex.match(userDomain)):
            validDomain = True
        else:
            print('Invalid domain. Please enter a valid domain. Domain names must contain only upper and lowercase letters and numbers. Hyphens or dashes (-) are allowed only if they are NOT the first or last character.')
    return userDomain

#Prompt for the name of the Key Pair to use for accessing instances
def getKeyPairName():
    #Compile a list of all available Key Pair Names
    keyPairs = ec2.key_pairs.all()
    validPairNames = []
    for pair in keyPairs:
        validPairNames.append(pair.name)

    validKeyPairName = False
    #Prompt for and validate Key Pair Name
    while(not validKeyPairName):
        userKeyPairName = input('Key Pair: ')
        if(not userKeyPairName in validPairNames):
            print('Please, enter the name of the key pair you created in AWS.')
        else:
            validKeyPairName = True
    return userKeyPairName

#Prompt for the number of Domain Controllers
#Users must enter a number between 2 and 8, the default is 2
def getNumDcs():
    validNum = False
    #Loop until the user enters a number between 2 and 8, inclusive
    while(not validNum):
        userNumDcs = input('How many Domain Controllers? [Leave blank to use default of 2]: ')
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
def getNumFileServers():
    validNum = False
    #Loop until the user enters a number between 2 and 4, inclusive
    while(not validNum):
        userNumFileServers = input('How many File Servers? [Leave blank to use default of 2]: ')
        #Ensure the user enters a number between 2 and 4, or leaves the input blank
        regex = re.compile('(^$)|^[2-4]$')
        if(not regex.match(userNumFileServers)):
            print('Please, enter a number between 2 and 4.')
        else:
            validNum = True
    #Return the default if the user enters nothing
    if(userNumDcs == ''):
        return MIN_DCS
    else:
        return int(userNumFileServers)

#Prompt for and validate the size of drives to be added to file servers
def getVolumeSize():
    validSize = False
    #Loop until a valid volume size is entered
    while(not validSize):
        userVolumeSize = input('How much storage would you like (in GiBs) on file servers?: ')
        #Validate that the number entered is positive and between MAX_VOLUME_SIZE and MIN_VOLUME_SIZE
        try:
            if(int(userVolumeSize) > MAX_VOLUME_SIZE or int(userVolumeSize) < MIN_VOLUME_SIZE):
                raise ValueError
            else:
                validSize = True
        except ValueError:
            print('Invalid input. Please enter a number between %d and %d.' % (MIN_VOLUME_SIZE,MAX_VOLUME_SIZE))
    return int(userVolumeSize)

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

print(getPassword('Enter a password for the domain administrator account (separate account from the default "Administrator" account): '))
