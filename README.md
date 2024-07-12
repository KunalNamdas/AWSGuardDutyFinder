# GuardDuty Alert System

This AWS Lambda function integrates with Amazon GuardDuty and Amazon SNS to monitor and notify about security findings. The function is triggered by an EventBridge rule to check for GuardDuty findings at regular intervals and send notifications via SNS.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Step 1: Create an SNS Topic](#step-1-create-an-sns-topic)
  - [Step 2: Enable GuardDuty](#step-2-enable-guardduty)
  - [Step 3: Create an IAM Role for Lambda](#step-3-create-an-iam-role-for-lambda)
  - [Step 4: Create the Lambda Function](#step-4-create-the-lambda-function)
  - [Step 5: Create an EventBridge Rule](#step-5-create-an-eventbridge-rule)
  - [Step 6: Test Your Setup](#step-6-test-your-setup)
- [Lambda Function Code](#lambda-function-code)

## Prerequisites

- AWS account with necessary permissions.
- Basic understanding of AWS services: Lambda, GuardDuty, SNS, EventBridge, IAM.

## Setup Instructions

### Step 1: Create an SNS Topic

1. Sign in to the AWS Management Console and open the Amazon SNS console.
2. Click on "Topics" in the left navigation pane.
3. Click the "Create topic" button.
4. Choose the type of topic (Standard or FIFO) and enter the necessary details (name, display name, etc.).
5. Click "Create topic".
6. Copy the ARN of the newly created topic.

### Step 2: Enable GuardDuty

1. Sign in to the AWS Management Console and open the GuardDuty console.
2. Enable GuardDuty if it is not already enabled:
   - Click on "Get started" if this is your first time using GuardDuty.
   - Follow the prompts to enable GuardDuty in your AWS account.
3. Get the Detector ID:
   - In the GuardDuty console, navigate to the "Detectors" section.
   - Note down the Detector ID.

### Step 3: Create an IAM Role for Lambda

1. Sign in to the AWS Management Console and open the IAM console.
2. Create a Role:
   - Click on "Roles" in the left navigation pane.
   - Click the "Create role" button.
   - Choose "Lambda" as the trusted entity.
   - Click "Next: Permissions".
   - Attach the necessary policies to allow Lambda to interact with GuardDuty and SNS:
     - `AmazonGuardDutyReadOnlyAccess`
     - `AmazonSNSFullAccess`
   - Click "Next: Tags" (optional).
   - Click "Next: Review".
   - Enter a role name (e.g., `LambdaGuardDutySNSRole`).
   - Click "Create role".

### Step 4: Create the Lambda Function

1. Sign in to the AWS Management Console and open the Lambda console.
2. Create a Function:
   - Click the "Create function" button.
   - Choose "Author from scratch".
   - Enter the function name (e.g., `GuardDutyAlertFunction`).
   - Choose Python as the runtime.
   - Under "Permissions", choose "Use an existing role" and select the role you created in Step 3.
   - Click "Create function".
3. Add the Code:
   - Replace the default code with your Lambda function code:
   - Replace `'YOUR_DETECTOR_ID'` with your actual GuardDuty Detector ID.
   - Replace `'YOUR_SNS_TOPIC_ARN'` with your SNS Topic ARN.
   - Click "Deploy" to save your function.

### Step 5: Create an EventBridge Rule

1. Sign in to the AWS Management Console and open the EventBridge console.
2. Create a Rule:
   - Click on "Rules" in the left navigation pane.
   - Click the "Create rule" button.
   - Enter a name for your rule (e.g., `GuardDutyCheckRule`) and a description.
   - For the Rule type, choose "Event Source".
   - Under "Event source", choose "Event pattern".
   - In the "Build event pattern" section, select the "AWS services" event source, and choose "GuardDuty" as the event source.
   - Set up the event pattern to match GuardDuty findings. You can use the default pattern or customize it based on your needs.
3. Add a Target:
   - Click "Next".
   - Under "Target types", choose "AWS service".
   - In the "Select a target" dropdown, choose "Lambda function".
   - Select your Lambda function from the dropdown (e.g., `GuardDutyAlertFunction`).
   - Click "Next".
4. Review and Create:
   - Review your settings.
   - Click "Create rule".

### Step 6: Test Your Setup

1. Generate GuardDuty Findings:
   - You can simulate findings in GuardDuty or wait for actual findings to occur.
2. Check SNS Notifications:
   - Verify that SNS notifications are received when GuardDuty detects findings.
3. Monitor Lambda Execution:
   - Use CloudWatch Logs to monitor the execution of your Lambda function and troubleshoot any issues.

## Lambda Function Code

```python
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
```

## Thank You for Using

You're welcome! Here's a thank-you message you can use:
"Thank you for using AWSGuardDutyFinder! If you have any feedback or questions, feel free to reach out. Happy monitoring!"
