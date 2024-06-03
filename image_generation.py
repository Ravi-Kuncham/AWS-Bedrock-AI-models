import boto3
import botocore.config
import json
import base64
from datetime import datetime

def lambda_handler(event, context):
    
    # Creating payload for image generation:
    event = json.loads(event['body'])
    message = event['message']
    
    payload = {
        "text_prompts":[{f"text":message}],
        "cfg_scale":10,
        "seed":0,
        "steps":100
    }
    
    # Invoking the Stability model and passing the payload for image generation:
    bedrock_client = boto3.client('bedrock-runtime', region_name = 'us-west-2', config = botocore.config.Config(read_timeout = 300, retries = {'max_attempts':3}))
    response = bedrock_client.invoke_model(body = json.dumps(payload), modelId = 'stability.stable-diffusion-xl-v1', contentType = "application/json", accept = "application/json")
    response_body = json.loads(response.get('body').read())
    base64_img_str = response_body['artifacts'][0].get('base64')
    image_content = base64.decodebytes(bytes(base64_img_str, 'utf-8'))
    
    # Saving to S3:
    s3_client = boto3.client('s3')
    s3_bucket = 'bedrock-bucket-007'
    current_time = datetime.now().strftime('%H%M%S')
    s3_key = f"image-output/{current_time}.png"
    
    s3_client.put_object(Body = image_content, Bucket = s3_bucket, Key = s3_key, ContentType = 'image/png')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Image saved to S3!')
    }
