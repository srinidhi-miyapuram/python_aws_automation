
# checking the volumes attached to instances which are using gp2

import boto3

client = boto3.client('ec2', region_name = 'ap-south-1')

sns_client = boto3.client('sns')
sns_arn = "arn"

res = client.describe_instances()
vol_list = {}

for inst in res['Reservations']:
    inst_id = inst['Instances'][0]['InstanceId']
    print(inst_id)
    vol = inst['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId']
    print(vol)
    response = client.describe_volumes(
        VolumeIds = [vol]
    )
    
    vol_type = response['Volumes'][0]['VolumeType']
    print(response['Volumes'][0]['VolumeType'])
    if vol_type == 'gp2':
        vol_list[inst_id] = vol


print(vol_list)

# sending email

email_body = "List of GP2 volumes\n"

for key in vol_list.keys():
    email_body += f"{key} = {vol_list[key]}" + "\n"
    print(key)

sns_client.publish(
    TopicArn = sns_arn,
    Subject = 'Volumes in ap-south-1 region',
    Message = email_body
)

