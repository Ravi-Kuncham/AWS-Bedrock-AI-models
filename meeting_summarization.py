import boto3
import botocore.config
import json
import base64
from datetime import datetime
from email import message_from_bytes


# Function to extract text from multipart data:
def extract_text_from_multipart(data):
    
    msg = message_from_bytes(data)
    
    text_content = ''
    
    if msg.is_multipart():
        
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                text_content = text_content + part.get_payload(decode=True).decode('utf-8') + "\n"
    
    else:
        
        if msg.get_content_type() == "text/plain":
            text_content = msg.get_payload(decode=True).decode('utf-8')
            
    return text_content.strip() if text_content else None


# Function to generate summary from user prompt and input file using Bedrock AI model:
def generate_summary_from_bedrock(content: str) -> str:
    
    prompt = f"""Human: Summarize the following meeting notes: {content}
    Assistant:"""
    
    body = {
        "prompt": prompt,
        "max_tokens_to_sample": 5000,
        "temperature": 0.1,
        "top_p": 0.2,
        "top_k": 250, 
        "stop_sequences": ["\n\nHuman:"]
    }
    
    try:
        bedrock_client = boto3.client("bedrock-runtime", region_name = 'us-west-2', config = botocore.config.Config(read_timeout = 300, retries = {'max_attempts':3}))
        response = bedrock_client.invoke_model(body = json.dumps(body), modelId = "anthropic.claude-v2")
        response_content = response.get('body').read().decode('utf-8')
        response_data = json.loads(response_content)
        summary = response_data['completion'].strip()
        print('Summary generated')
        return summary
    
    except Exception as e:
        print(f"Error while generating summary: {e}")
        return ""

# Function to save the generated summary into an s3 bucket:
def save_to_s3_bucket(summary, s3_bucket, s3_key):
    
    s3 = boto3.client('s3')
    
    try:
        s3. put_object(Body = summary, Key = s3_key, Bucket = s3_bucket)
        print(f"Sumary saved to the S3 bucket {s3_bucket}")
    
    except Exception as e:
        print(f"Error while saving the summary: {e}")
        

# Lambda handler function:
def lambda_handler(event, context):
    
    decoded_body = base64.b64decode(event['body'])
    
    # Function call extract text from multi-part:
    text_content = extract_text_from_multipart(decoded_body)
    
    if not text_content:
        return {
            'statusCode': 400,
            'body': json.dumps('Failed to extract content')
        }
    
    # Function call to generate summary of the meeting notes document using bedrock's Claude-v2 AI model:
    summary = generate_summary_from_bedrock(text_content)
    
    if summary:
        current_time = datetime.now().strftime('%H%M%S')
        s3_bucket = 'bedrock-bucket-007'
        s3_key = f'summary-output/{current_time}.txt'
        
        # Function call to save the summary generated into the s3 bucket:
        save_to_s3_bucket(summary, s3_bucket, s3_key)
        
    else:
        print("No summary was generated")
    
    return{
        'statusCode': 200,
        'body': json.dumps('Summary generation finished')
    }