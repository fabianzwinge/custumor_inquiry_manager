import boto3
from botocore.exceptions import ClientError
import os
import json

def send_templated_email(to_address: str, template_name: str, template_data: dict):
    """
    Sends a templated email using AWS SES.

    :param to_address: The recipient's email address.
    :param template_name: The name of the SES template.
    :param template_data: A dictionary of data to pass to the template.
    :return: The message ID if the email was sent successfully, else None.
    """
    SENDER = os.getenv("SENDER_EMAIL")

    if not SENDER:
        print("ERROR: SENDER_EMAIL environment variable not set. Cannot send email.")
        return None

    client = boto3.client('ses', region_name="us-east-1")

    try:
        response = client.send_templated_email(
            Source=SENDER,
            Destination={'ToAddresses': [to_address]},
            Template=template_name,
            TemplateData=json.dumps(template_data)
        )
    except ClientError as e:
        print(f"Email sending failed: {e.response['Error']['Message']}")
        return None
    else:
        print(f"Email sent! Template: {template_name}, Message ID: {response['MessageId']}")
        return response['MessageId']

def send_confirmation_email(to_address: str, name: str, inquiry_id: int, inquiry_text: str):
    return send_templated_email(
        to_address=to_address,
        template_name="InquiryConfirmationTemplate",
        template_data={
            "name": name,
            "inquiry_id": str(inquiry_id),
            "inquiry_text": inquiry_text
        }
    )

def send_response_email(to_address: str, inquiry_id: int, response_text: str, inquiry_text: str):
    return send_templated_email(
        to_address=to_address,
        template_name="InquiryResponseTemplate",
        template_data={
            "inquiry_id": str(inquiry_id),
            "response_text": response_text,
            "inquiry_text": inquiry_text
        }
    )
