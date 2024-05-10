import boto3
client = boto3.client('ec2')
conn = boto3.resource('ec2')
instances = conn.instances.filter()
for instance in instances:
    if instance.state["Name"] == 'running':
        client.stop_instances(InstanceIds = [instance.id])
        print(f"The {instance.id} is stopped")