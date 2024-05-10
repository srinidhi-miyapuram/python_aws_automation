
# Listing out the unused Elastic Ip's

import boto3

client = boto3.client('ec2')

response = client.describe_addresses()

unused_eip = []

for i in response['Addresses']:
    ip_addr = i['PublicIp']
    try:
        allocation = i['AssociationId']
    except:
        unused_eip.append(ip_addr)

print(unused_eip)