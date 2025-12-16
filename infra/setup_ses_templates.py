import boto3
from botocore.exceptions import ClientError
import os

CONFIRMATION_TEMPLATE = {
    "TemplateName": "InquiryConfirmationTemplate",
    "SubjectPart": "Confirmation of your inquiry (ID: {{inquiry_id}})",
    "HtmlPart": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
        .header { background-color: #f4f4f4; padding: 10px; text-align: center; border-radius: 8px 8px 0 0; }
        .content { padding: 20px; }
        .footer { font-size: 0.9em; text-align: center; color: #777; margin-top: 20px; }
        .inquiry-box { background-color: #f9f9f9; padding: 15px; border-radius: 5px; border: 1px solid #eee; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Your inquiry has been received</h2>
        </div>
        <div class="content">
            <p>Hello {{name}},</p>
            <p>Thank you for your message. We have received your inquiry with the ID <strong>{{inquiry_id}}</strong> and will process it as soon as possible.</p>
            <p><strong>Your original inquiry:</strong></p>
            <div class="inquiry-box">
                <p><em>{{inquiry_text}}</em></p>
            </div>
            <p>We will get back to you as soon as we have an answer for you.</p>
        </div>
        <div class="footer">
            <p>&copy; Customer Inquiry Manager</p>
        </div>
    </div>
</body>
</html>''',
    "TextPart": """Hello {{name}},

Thank you for your message. We have received your inquiry with the ID {{inquiry_id}} and will process it as soon as possible.

Your original inquiry:
{{inquiry_text}}

We will get back to you as soon as we have an answer for you.

© Customer Inquiry Manager
"""
}

RESPONSE_TEMPLATE = {
    "TemplateName": "InquiryResponseTemplate",
    "SubjectPart": "Response to your inquiry (ID: {{inquiry_id}})",
    "HtmlPart": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
        .header { background-color: #f4f4f4; padding: 10px; text-align: center; border-radius: 8px 8px 0 0; }
        .content { padding: 20px; }
        .response-box { background-color: #f9f9f9; padding: 15px; border-radius: 5px; border: 1px solid #eee; margin-bottom: 20px; }
        .inquiry-box { background-color: #f9f9f9; padding: 15px; border-radius: 5px; border: 1px solid #eee; }
        .footer { font-size: 0.9em; text-align: center; color: #777; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Response to your inquiry</h2>
        </div>
        <div class="content">
            <p>Here is the response to your inquiry with the ID <strong>{{inquiry_id}}</strong>:</p>
            <div class="response-box">
                <p>{{response_text}}</p>
            </div>
            <p><strong>Your original inquiry:</strong></p>
            <div class="inquiry-box">
                <p><em>{{inquiry_text}}</em></p>
            </div>
            <p>We hope this response was helpful.</p>
        </div>
        <div class="footer">
            <p>&copy; Customer Inquiry Manager</p>
        </div>
    </div>
</body>
</html>''',
    "TextPart": """Response to your inquiry (ID: {{inquiry_id}})

Here is the response to your inquiry:

{{response_text}}

Your original inquiry:
{{inquiry_text}}

We hope this response was helpful.

© Customer Inquiry Manager
"""
}


def create_or_update_template(ses_client, template_definition):
    """
    Creates or updates a single SES template.
    """
    template_name = template_definition["TemplateName"]
    template_content = {
        'SubjectPart': template_definition["SubjectPart"],
        'HtmlPart': template_definition["HtmlPart"],
        'TextPart': template_definition["TextPart"]
    }
    
    try:
        ses_client.update_template(
            Template={
                'TemplateName': template_name,
                **template_content
            }
        )
        print(f"Template '{template_name}' was successfully updated.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'TemplateDoesNotExistException':
            ses_client.create_template(
                Template={
                    'TemplateName': template_name,
                    **template_content
                }
            )
            print(f"Template '{template_name}' was successfully created.")
        else:
            print(f"An unexpected error occurred with '{template_name}': {e}")

def main():
    try:
        ses_client = boto3.client('ses', region_name="us-east-1")
    except Exception as e:
        print(f"Error creating SES client: {e}")
        return

    templates_to_process = [CONFIRMATION_TEMPLATE, RESPONSE_TEMPLATE]
    
    for template_def in templates_to_process:
        create_or_update_template(ses_client, template_def)

if __name__ == "__main__":
    main()
