import boto3
import datetime

region = 'ap-south-1'
client = boto3.client('ec2', region_name=region)
sns_client = boto3.client('sns', region_name=region)

# response = client.describe_instances(region, account)
response = client.describe_tags(
    Filters=[{
        'Name': 'tag:TagName',
        'Values': ['TestInstance'],
    }],
)

# Listing the instances which have the specified tag
ec2_instance_list = []
for tag in response['Tags']:
    ec2_instance_list.append(tag["ResourceId"])
   

# Getting the details of the instances
ec2_instance = client.describe_instances(InstanceIds=ec2_instance_list)


# Checking if the instance launch time is 3 days old
today_date = datetime.datetime.now()
today_date = today_date.strftime("%Y-%m-%d").split("-")
today_date = [int(i) for i in today_date]

list_terminated_instances = []

for instance in ec2_instance["Reservations"][0]["Instances"]:
    instance_launchTime = instance["LaunchTime"]
    instance_date = instance_launchTime.strftime("%Y-%m-%d").split("-")
    instance_date = [int(i) for i in instance_date]

    year = today_date[0] - instance_date[0]
    month = today_date[1] - instance_date[1]
    day = today_date[2] - instance_date[2]

    if year > 0 or month > 0 or day >= 0:
        list_terminated_instances.append(instance["InstanceId"])

# Terminating the 3 days older CIR images if any
if len(list_terminated_instances):
    instance_termination = client.terminate_instances(InstanceIds=list_terminated_instances)
    for i in instance_termination["TerminatingInstances"]:
        print("\n", i["InstanceId"], " ----- ", i["CurrentState"]["Name"])

# Emailing the terminated instance detais
sns_arn = "<SNS ARN>"
subject = "Terminated CIR instances"
message = "The below instances are 3 days older, created for testing purpose. Hence, they are terminated. Please find the instance id's below :- \n\n\n\n"

for instance in list_terminated_instances:
    message += instance + "\n"

sns_response = sns_client.publish(
    TopicArn=sns_arn,
    Subject=subject,
    Message=message,
)