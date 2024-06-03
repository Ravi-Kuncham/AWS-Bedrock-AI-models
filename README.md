# AWS-Bedrock-AI-models
Using AI models provided by the AWS Bedrock service, I built a serverless architechture which can:
1. Genererate Code from user prompts
2. Generate Summary of meeting documents or any other document
3. Generate Images from user prompts
The serverless architechture consists of AWS Bedrock, Lambda, API gateway, S3 and Postman.
- Using Postman the prompts/documents are passed and AWS API is invoked
- AWS API then calls Lambda function related to the task (code, summary or image generation)
- AWS lambda function then uses the respective AI models from the AWS Bedrock to perform the task
- The results are then stored in the S3 bucket
