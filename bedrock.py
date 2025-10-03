#!/usr/bin/env python3

import boto3
import json

client = boto3.client(service_name='bedrock-runtime', region_name="us-west-2")

def list_bedrock_models():
    try:
        response = client.list_foundation_models()
        for model in response['modelSummaries']:
            print(f"Model ID: {model['modelId']}")
            print(f"Provider: {model['providerName']}")
            print(f"Model Name: {model['modelName']}")
    except Exception as e:
        print(f"Error listing models: {str(e)}")
    finally:
        print("-" * 50)


def generate_text(prompt, max_tokens=100):
    try:
        body = json.dumps({
            "prompt": prompt,
            "max_tokens_to_sample": max_tokens,
            "temperature": 1,
            "top_p": 0.1
        })

        response = client.invoke_model(
            modelId="anthropic.claude-instant-v1",
            body=body
        )

        response_body = json.loads(response.get('body').read())
        return response_body.get('completion')
    except Exception as e:
        print(f"Error generating text: {str(e)}")
        return None
    finally:
        print("-" * 50)


# List available models
list_bedrock_models()


# Test text generation
prompt = "Tell me a short joke"
response = generate_text(prompt)
if response:
    print("\nGenerated text:")
    print(response)
