import json
import boto3
from datetime import date,datetime

def lambda_handler(event, context):
    # TODO implement
    region = 'ap-south-1'
    client = boto3.client('ec2', region_name = region)
    sns_client = boto3.client('sns')
    sns_arn = "arn"
    
    # listing all the amis
    
    response = client.describe_images(
        Owners=[
            'self',
        ]
    )
    
    snap_list = {}
    ami_list = {}
    
    today = date.today()
    tmonth = today.month
    tyear = today.year
    

    for image in response['Images']:
        ami_list[image['CreationDate']] = image['ImageId']
        snap_list[image['CreationDate']] = image['BlockDeviceMappings'][0]['Ebs']['SnapshotId']
    
    # deleting the 2 or greater amis
    
    del_ami = []
    del_snap = []
    
    for key in ami_list.keys():
        cdate = key.split('T')
        clist = cdate[0].split('-')
        cmonth = int(clist[1])
        cyear = int(clist[0])
        if cyear < tyear or (tmonth - cmonth) >= 0:
            result = client.deregister_image(
                ImageId=ami_list[key]
            )
            res = client.delete_snapshot(
                SnapshotId = snap_list[key]
            )
            del_snap.append(snap_list[key])
            del_ami.append(ami_list[key])
            print(f"The {snap_list[key]} {ami_list[key]}is deleted")
    
    
    # sending email
    
    # email_body = "List of AMIS\n"
    
    for key in ami_list.keys():
        email_body += f"{key} = {ami_list[key]} + {snap_list[key]}" + "\n"
    
    email_body += "The deleted ami's are :- " + "\n"
    
    for image in del_ami:
        email_body += f"{image} is deleted" + "\n"

    sns_client.publish(
        TopicArn = sns_arn,
        Subject = 'AMIS in ap-south-1 region',
        Message = email_body
    )

lambda_handler(1,1)