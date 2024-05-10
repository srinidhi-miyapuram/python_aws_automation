import boto3
client = boto3.client('ec2')
sns_client = boto3.client('sns')

instance_id = []
res = client.describe_instances()
for response in res['Reservations']:
    for instance in response['Instances']:
        print(f"Instance id is {instance['InstanceId']} and its state is {instance['State']['Name']}")
        instance_id.append(instance['InstanceId'])

sns_client.publish(
    TopicArn = 'arn',
    Subject = 'EC2 Instances in ap-south-1 region',
    Message = str(instance_id)
)

