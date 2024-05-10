import boto3
client = boto3.client('ec2')
vol_id = []
vol = client.create_volume(AvailabilityZone = 'ap-south-1a',
                           Size = 8,
                           VolumeType = 'gp2',
                           MultiAttachEnabled = False)
vol_id.append(vol['VolumeId'])
waiter = client.get_waiter('volume_available')
waiter.wait(VolumeIds = vol_id)
print(f"The volume created is {vol['State']} and volume id is {vol['VolumeId']}")

for volId in vol_id:
    snap = client.create_snapshot(VolumeId = volId)
    print(f"snapshot for {volId} is {snap['SnapshotId']}")