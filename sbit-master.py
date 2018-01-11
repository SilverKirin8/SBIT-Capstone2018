import boto3
import re

'''
# DCs
# FSs
KeyName
Instance Types
Drive Sizes
'''

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
#print(getDomainName())


