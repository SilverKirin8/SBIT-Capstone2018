import boto3
import re

'''
Domain
# DCs
# FSs
KeyName
Instance Types
Drive Sizes
'''

def getDomainName():
    validDomain = False
    userDomain = input('Domain Name: ')
    regex = re.compile('[A-Za-z0-9]([A-Za-z0-9-]*\.)+[A-Za-z0-9]+')
    if(regex.match(userDomain)):
        print(userDomain)
'''        validDomain = True
    else:
        print('

'''

getDomainName()
