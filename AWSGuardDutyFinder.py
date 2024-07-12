import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Initialize GuardDuty client
        guardduty = boto3.client('guardduty')
        
        # Specify DetectorId
        detector_id = 'YOUR_DETECTOR_ID'  # Replace 'YOUR_DETECTOR_ID' with your actual detector ID
        
        try:
            # Get findings
            findings = guardduty.list_findings(DetectorId=detector_id)
        except Exception as e:
            logger.error("Error getting GuardDuty findings: %s", e)
            return {
                'statusCode': 500,
                'body': 'Error getting GuardDuty findings'
            }
        
        # Check if there are findings
        if len(findings['FindingIds']) > 0:
            try:
                # Initialize SNS client
                sns = boto3.client('sns')
                
                # Publish message to SNS topic
                sns.publish(
                    TopicArn='YOUR_SNS_TOPIC_ARN',  # Replace with your SNS Topic ARN
                    Message='GuardDuty findings: {}'.format(len(findings['FindingIds']))
                )
            except Exception as e:
                logger.error("Error publishing message to SNS topic: %s", e)
                return {
                    'statusCode': 500,
                    'body': 'Error publishing message to SNS topic'
                }
        
        return {
            'statusCode': 200,
            'body': 'Processed {} findings'.format(len(findings['FindingIds']))
        }

    except Exception as e:
        logger.error("Unhandled error: %s", e)
        return {
            'statusCode': 500,
            'body': 'Internal server error'
        }
