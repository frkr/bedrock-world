#!/usr/bin/env python3

import boto3
import json

# Initialize Bedrock client
client = boto3.client(service_name='bedrock-runtime', region_name="us-west-2")

# Mock database of CPF to user names for demonstration
CPF_DATABASE = {
    "123.456.789-00": "João da Silva",
    "987.654.321-00": "Maria Santos",
    "111.222.333-44": "Pedro Oliveira",
    "555.666.777-88": "Ana Costa",
    "12345678900": "João da Silva",  # Also accept without formatting
    "98765432100": "Maria Santos",
    "11122233344": "Pedro Oliveira",
    "55566677788": "Ana Costa"
}


def cpf_to_username(cpf):
    """
    Convert a CPF number to a full user name.
    This is a mock implementation using a sample database.
    
    Args:
        cpf (str): The CPF number (with or without formatting)
        
    Returns:
        str: The full name associated with the CPF, or an error message
    """
    # Normalize CPF by removing formatting characters
    normalized_cpf = ''.join(char for char in cpf if char.isdigit())

    # Try to find in database (try both formatted and unformatted)
    if cpf in CPF_DATABASE:
        return CPF_DATABASE[cpf]
    elif normalized_cpf in CPF_DATABASE:
        return CPF_DATABASE[normalized_cpf]
    else:
        return f"CPF {cpf} not found in database"


def invoke_model_with_tools(user_message):
    """
    Invoke Bedrock model with tool calling capability.
    
    Args:
        user_message (str): The user's message/query
        
    Returns:
        str: The final response from the model
    """
    # Define the tool specification
    tools = [
        {
            "name": "cpf_to_username",
            "description": "Converts a Brazilian CPF (Cadastro de Pessoas Físicas) number to the full name of the person. The CPF can be provided with or without formatting (dots and dashes).",
            "input_schema": {
                "type": "object",
                "properties": {
                    "cpf": {
                        "type": "string",
                        "description": "The CPF number to look up. Can be formatted (e.g., 123.456.789-00) or unformatted (e.g., 12345678900)"
                    }
                },
                "required": ["cpf"]
            }
        }
    ]
    
    # Prepare the initial message
    messages = [
        {
            "role": "user",
            "content": user_message
        }
    ]
    
    # Model configuration
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    # First API call - send the query with tool definitions
    print(f"User: {user_message}")
    print("-" * 50)
    
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "tools": tools,
        "messages": messages
    }
    
    try:
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response['body'].read())
        print("Model response (first call):")
        print(json.dumps(response_body, indent=2))
        print("-" * 50)
        
        # Check if model wants to use a tool
        stop_reason = response_body.get('stop_reason')
        
        if stop_reason == 'tool_use':
            # Extract tool use request
            content_blocks = response_body.get('content', [])
            
            # Build assistant message with all content blocks
            assistant_message = {
                "role": "assistant",
                "content": content_blocks
            }
            messages.append(assistant_message)
            
            # Process each tool use in the response
            tool_results = []
            for block in content_blocks:
                if block.get('type') == 'tool_use':
                    tool_name = block.get('name')
                    tool_input = block.get('input', {})
                    tool_use_id = block.get('id')
                    
                    print(f"Model wants to use tool: {tool_name}")
                    print(f"Tool input: {json.dumps(tool_input, indent=2)}")
                    print("-" * 50)
                    
                    # Execute the tool
                    if tool_name == 'cpf_to_username':
                        cpf = tool_input.get('cpf', '')
                        result = cpf_to_username(cpf)
                        print(f"Tool result: {result}")
                        print("-" * 50)
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": result
                        })
            
            # Send tool results back to model
            messages.append({
                "role": "user",
                "content": tool_results
            })
            
            # Second API call - send tool results
            request_body['messages'] = messages
            
            response = client.invoke_model(
                modelId=model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            print("Model response (after tool use):")
            print(json.dumps(response_body, indent=2))
            print("-" * 50)
        
        # Extract final text response
        final_response = ""
        for block in response_body.get('content', []):
            if block.get('type') == 'text':
                final_response += block.get('text', '')
        
        return final_response
        
    except Exception as e:
        print(f"Error invoking model: {str(e)}")
        return None


def main():
    """
    Main function to demonstrate tool calling with CPF to username conversion.
    """
    print("=" * 50)
    print("Bedrock Tool Calling Demo - CPF to Username")
    print("=" * 50)
    print()

    # Example 1: Ask for a specific CPF
    print("Example 1: Direct CPF lookup")
    user_query = "What is the full name of the person with CPF 123.456.789-00?"
    response = invoke_model_with_tools(user_query)
    if response:
        print(f"\nFinal Response:\n{response}")
    print("\n" + "=" * 50 + "\n")

    # Example 2: Ask for multiple CPFs
    print("Example 2: Multiple CPF lookup")
    user_query = "Can you tell me the names for these CPFs: 987.654.321-00 and 11122233344?"
    response = invoke_model_with_tools(user_query)
    if response:
        print(f"\nFinal Response:\n{response}")
    print("\n" + "=" * 50 + "\n")

    # Example 3: CPF not in database
    print("Example 3: CPF not found")
    user_query = "Who has CPF 999.999.999-99?"
    response = invoke_model_with_tools(user_query)
    if response:
        print(f"\nFinal Response:\n{response}")
    print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()
