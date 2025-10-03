#!/usr/bin/env python3

import boto3
import json
import base64
from datetime import datetime

# Initialize Bedrock Runtime client
client = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')

def generate_cat_image():
    """
    Generate an image of a cat using AWS Bedrock's Amazon Titan Image Generator
    """
    try:
        # Prepare the request body for Amazon Titan Image Generator
        request_body = json.dumps({
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": "a cute cat, high quality, detailed, photorealistic"
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "standard",
                "cfgScale": 8.0,
                "height": 512,
                "width": 512,
                "seed": 0
            }
        })
        
        # Model ID for Amazon Titan Image Generator
        model_id = "amazon.titan-image-generator-v1"
        
        print(f"Generating cat image using {model_id}...")
        
        # Invoke the model
        response = client.invoke_model(
            modelId=model_id,
            body=request_body,
            accept="application/json",
            contentType="application/json"
        )
        
        # Parse the response
        response_body = json.loads(response['body'].read())
        
        # Extract the base64 encoded image
        image_base64 = response_body['images'][0]
        
        # Decode the image
        image_data = base64.b64decode(image_base64)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cat_image_{timestamp}.png"
        
        # Save the image
        with open(filename, 'wb') as f:
            f.write(image_data)
        
        print(f"✓ Image successfully generated and saved as: {filename}")
        return filename
        
    except Exception as e:
        print(f"Error with Amazon Titan: {str(e)}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("AWS Bedrock - Cat Image Generator")
    print("=" * 60)
    
    result = generate_cat_image()
    
    if result:
        print("\nImage generation completed successfully!")
    else:
        print("\nImage generation failed. Please check your AWS credentials and Bedrock access.")
