import boto3
client = boto3.client('ec2', region_name = 'ap-south-1')
ec2 = client.describe_snapshots(OwnerIds = ['self'])
for snap in ec2['Snapshots']:
    client.delete_snapshot(SnapshotId = snap['SnapshotId'])
    print(f"The {snap['SnapshotId']} is deleted")