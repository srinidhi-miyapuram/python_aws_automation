import boto3
client = boto3.client('ec2')
instances_list = boto3.resource('ec2')
instances_list = instances_list.instances.filter() # need to find the meaning of this line
for instance in instances_list:
    res = client.terminate_instances(InstanceIds = [instance.id])
    print(f"The {instance.id} is terminated")
