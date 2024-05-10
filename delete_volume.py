import boto3
client = boto3.client('ec2')

rclient = boto3.resource('ec2')
volumes = rclient.volumes.all()
volumes = rclient.volumes.filter(Filters = [{
    'Name': 'status',
    'Values': ['available']
}])
for vol in volumes:
    client.delete_volume(VolumeId = vol.id)
    print(f"The {vol.id} is deleted")