import boto3
import botocore.config
import json
from datetime import datetime

# Function to generate code using Anthropic's Claude v-2 model by passing a user prompt:
def generate_code_using_bedrock(message:str, programming_language: str) -> str:
    
    prompt = f"""Human: Write {programming_language} code for the following instructions: {message}.
    Assistant:"""
    
    body = {
        "prompt": prompt,
        "max_tokens_to_sample": 2048,
        "temperature": 0.1,
        "top_k": 250,
        "top_p": 0.2,
        "stop_sequences": ['\n\nHuman:']
    }
    
    try:
        bedrock = boto3.client("bedrock-runtime", region_name = "us-west-2", config = botocore.config.Config(read_timeout = 300, retries = {'max_attempts':3}))
        
        response = bedrock.invoke_model(body = json.dumps(body), modelId = "anthropic.claude-v2")
        response_content = response.get('body').read().decode('utf-8')
        response_data = json.loads(response_content)
        code = response_data["completion"].strip()
        
        return code
        
    except Exception as e:
        print(f"Error generating the code: {e}")
        return ""


# Function to save the generated code to S3 bucket:
def save_code_to_s3(code, s3_bucket, s3_key):
    
    s3_client = boto3.client('s3')
    
    try:
        s3_client.put_object(Bucket = s3_bucket, Key = s3_key, Body = code)
        print(f"Successfully saved the code to {s3_bucket} bucket")
        
    except Exception as e:
        print(f"Failed to save the code to s3: {e}")


# Lambda Handler function:
def lambda_handler(event, context):
    
    event = json.loads(event['body'])
    message = event['message']
    language = event['key']
    
    # Generating the code using the user prompt:
    generated_code = generate_code_using_bedrock(message, language)
    
    if generated_code:
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f'code-output/{current_time}.py'
        s3_bucket = 'bedrock-bucket-007'
        
        # Saving the generated code to S3 bucket:
        save_code_to_s3(generated_code, s3_bucket, s3_key)
        
    else:
        print("No code was generated")
    
    return{
        "statusCode": 200,
        "body": json.dumps('Code generation complete')
    }