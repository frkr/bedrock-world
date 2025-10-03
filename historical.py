#!/usr/bin/env python3

import boto3
import json


def call_bedrock_model(prompt):
    """Call Bedrock model with the given prompt."""
    try:
        client = boto3.client(service_name='bedrock-runtime', region_name="us-west-2")
        
        body = json.dumps({
            "prompt": prompt,
            "max_tokens_to_sample": 500,
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
        print(f"Error calling Bedrock model: {str(e)}")
        return None


def main():
    """Main function to get user input and call Bedrock model."""
    print("Welcome to Historical - Bedrock Chat")
    print("Press Ctrl+C to exit")
    print("-" * 50)
    
    history = []
    
    try:
        while True:
            user_input = input("\nUser: ").strip()
            
            if user_input:
                # Add to history
                history.append(user_input)
                
                # Call Bedrock model
                print("\nCalling Bedrock model...")
                response = call_bedrock_model(user_input)
                
                if response:
                    print(f"\nAssistant: {response}")
                else:
                    print("\nFailed to get response from Bedrock model.")
            else:
                print("Empty input, please enter something.")
    
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting...")
        print(f"Total inputs in history: {len(history)}")
        print("Goodbye!")


if __name__ == "__main__":
    main()
