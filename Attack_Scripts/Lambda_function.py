import json
import boto3

THRESHOLD = 5 # Number of failed attempts to trigger an alert

def lambda_handler(event, context):
    data = json.loads(event['awslogs']['data'])
    log_events = data['logEvents']

    ip_count = {}

    for log_event in log_events:
        message = log_event['message']
        fields = message.split()
        
        # Assuming the default VPC Flow Logs format
        source_ip = fields[3]
        destination_port = fields[6]
        action = fields[13]

        if destination_port == '22' and action == 'REJECT':
            ip_count[source_ip] = ip_count.get(source_ip, 0) + 1

    for ip, count in ip_count.items():
        if count > THRESHOLD:
            send_alert(ip, count)

def send_alert(ip, count):
    sns_client = boto3.client('sns')
    topic_arn = 'arn:aws:sns:us-west-2:429364903933:BruteForce'

    message = f"Suspicious SSH activity detected from IP {ip}. {count} failed attempts within the time window."
    subject = "SSH Brute Force Alert"

    sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=subject
    )

    print(f"Alert sent for IP {ip} with {count} failed attempts.")
