# importing pandas as pd
import pandas as pd

"""

Multipurpose Internet Mail Extensions (MIME) ---> When the the email contains an attachment,
it must be sent in MIME format. 

"""
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


import boto3
from datetime import date
import re

def lambda_handler(event, context):
    # TODO implement
    region = 'ap-south-1'
    client = boto3.client('ec2', region_name = region)
    ses_client = boto3.client('ses', region_name = region)
    

    # getting today's date and time 
    
    today = date.today()
    today_day = today.day
    tmonth = today.month
    tyear = today.year
    
    # listing snapshots 

    snap_res = client.describe_snapshots(OwnerIds = ['self'])

    for snap in snap_res['Snapshots']:
        # getting snapshot created date
        snap_date = snap['StartTime']
        datetime_obj = snap_date.date() 
        snap_month = datetime_obj.month
        snap_year = datetime_obj.year
        # checking if the snapshot is 3 weeks older or not
        if snap_year < tyear or (tmonth - snap_month) >= 1:
            snap_descprition = snap['Description']
            # checking if the description of snapshot contain ami id
            result = re.search("ami-*", snap_descprition)
            # if yes then deleting the ami to proceed with the deletion of the snapshot
            if result:
                ami_id = re.split(" ami-", snap_descprition)[-1]
                ami_res = client.deregister_image(
                    ImageId="ami-"+ami_id
                    )
            # deleting the snapshot
            snap_res = client.delete_snapshot(
                SnapshotId = snap['SnapshotId']
            )
    
    # creating lists 
    snap_list_updated = []
    snap_descp = []
    snap_creation_date = []
    snap_state = []
    snap_storage = []
    snap_encryption = []
    snap_progress = []
    snap_kmsKeyId = []
    snap_volumeId = []
    snap_tags = []

    # appending the values in respective list
    for snap in snap_res['Snapshots']:
        snap_list_updated.append(snap['SnapshotId'])
        snap_descp.append(snap['Description'])
        snap_creation_date.append(snap['StartTime'])
        snap_state.append(snap['State'])
        snap_storage.append(snap['StorageTier'])
        snap_encryption.append(snap['Encrypted'])
        snap_progress.append(snap['Progress'])
        # snap_kmsKeyId.append(snap['KmsKeyId'])
        snap_volumeId.append(snap['VolumeId'])
        snap_tags.append(snap['Tags'][0]['Value'])

    # Creating the dictionary for the list of the snapshot details
    report = {
        "SnapshotId" : snap_list_updated,
        "Description" : snap_descp,
        "StartTime" : snap_creation_date,
        "State" : snap_state,
        "StorageTier" : snap_storage,
        "Encrypted" : snap_encryption,
        "Progress" : snap_progress,
        # "KmsKeyId" : snap_kmsKeyId,
        "VolumeId" : snap_volumeId,
        "Tags" : snap_tags
    }

    snap_report = pd.DataFrame(report)
    print(snap_report)

    file_name = "Snapshot_Report_" + str(today_day) + "_" + str(tmonth) + "_" + str(tyear) + ".csv"
    snap_report.to_csv(file_name)
    
    # sending email
    
    email_body = "After deleting 3 weeks older snapshotsare :- \n"
    

    # SES mail

    email_to = ["from_mail", "to_mail"]

    # # SES report

    msg = MIMEMultipart()
    msg["Subject"] = "KMS Monthly Snapshot report"
    msg["From"] = email_to[0]
    msg["To"] = email_to[0]
    msg["CC"] = email_to[1]

    body = MIMEText(email_body, "plain")
    msg.attach(body)

    part = MIMEApplication(open(file_name, 'rb').read())

    part.add_header('Content-Disposition', 'attachment', filename=file_name)
    msg.attach(part)

    # sending the mail with the csv file attached

    response = ses_client.send_raw_email(
        Source=msg['From'],
        Destinations=email_to,
        RawMessage={
            'Data': msg.as_string()
        }
    )

lambda_handler(1,1)