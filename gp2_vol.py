
# checking the volumes in the account which are using gp2 

import boto3

client = boto3.client('ec2', region_name = 'ap-south-1')

sns_client = boto3.client('sns')
sns_arn = "arn"

res = client.describe_volumes()
vol_list = []

for inst in res['Volumes']:
    print(inst)
    vol_type = inst['VolumeType']
    print(vol_type)
    vol_id = inst['VolumeId']
    print(inst['VolumeType'])
    if vol_type == 'gp2':
        vol_list.append(vol_id)


print(vol_list)

# sending email

email_body = "List of GP2 volumes\n"

for vol in vol_list:
    email_body += f"{vol}" + "\n"
    print(vol)

sns_client.publish(
    TopicArn = sns_arn,
    Subject = 'Volumes in ap-south-1 region',
    Message = email_body
)

