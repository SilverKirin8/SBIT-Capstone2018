import boto3
import re

'''
# DCs
# FSs
Instance Types
Drive Sizes
Admin Passwords
'''
MAX_DCS=8
MIN_DCS=2

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
        regex = re.compile('[A-Za-z0-9]([A-Za-z0-9-]*\.)+[A-Za-z0-9]+')
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
        regex = re.compile('(^$)|[2-8]')
        if(not regex.match(userNumDcs)):
            print('Please, enter a number between 2 and 8.')
        else:
            validNum = True
    if(userNumDcs == ''):
        return MIN_DCS
    else:
        return int(userNumDcs)


print(getKeyPairName())
