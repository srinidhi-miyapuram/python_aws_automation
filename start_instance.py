import boto3
client = boto3.client('ec2')
conn = boto3.resource('ec2')
instnaces = conn.instances.filter()
for instance in instnaces:
    if instance.state['Name'] == 'stopped':
        client.start_instances(InstanceIds = [instance.id])
        print(f"The {instance.id} is started")