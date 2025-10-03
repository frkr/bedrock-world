#!/usr/bin/env python3
"""
AWS Bedrock Permissions Auto-Apply Script

This script automatically applies Bedrock full access permissions to your current AWS user.
It will:
1. Check AWS CLI is configured
2. Get your current AWS username
3. Apply the Bedrock full access policy
4. Verify the permissions were applied
"""

import json
import subprocess
import sys
import os

# IAM Policy for full Bedrock access
BEDROCK_FULL_ACCESS_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "bedrock-runtime:*"
            ],
            "Resource": "*"
        }
    ]
}

def print_header():
    """Print script header."""
    print("\n" + "█" * 80)
    print("  AWS BEDROCK PERMISSIONS AUTO-APPLY SCRIPT")
    print("█" * 80 + "\n")

def check_aws_cli():
    """Check if AWS CLI is installed and configured."""
    print("🔍 Checking AWS CLI configuration...")
    try:
        result = subprocess.run(
            ['aws', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ AWS CLI found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ERROR: AWS CLI not found or not configured.")
        print("\nPlease install and configure AWS CLI:")
        print("  1. Install: https://aws.amazon.com/cli/")
        print("  2. Configure: aws configure")
        return False

def get_caller_identity():
    """Get the current AWS caller identity."""
    try:
        result = subprocess.run(
            ['aws', 'sts', 'get-caller-identity'],
            capture_output=True,
            text=True,
            check=True
        )
        identity = json.loads(result.stdout)
        return identity
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Could not get AWS identity: {e.stderr}")
        return None
    except json.JSONDecodeError:
        print("❌ ERROR: Could not parse AWS identity response.")
        return None

def get_username():
    """Get the current AWS username."""
    print("\n🔍 Getting your AWS username...")
    try:
        result = subprocess.run(
            ['aws', 'iam', 'get-user'],
            capture_output=True,
            text=True,
            check=True
        )
        user_info = json.loads(result.stdout)
        username = user_info['User']['UserName']
        print(f"✓ Username: {username}")
        return username
    except subprocess.CalledProcessError as e:
        print(f"⚠ Could not get username directly. Trying to extract from ARN...")
        # Try to get username from caller identity
        identity = get_caller_identity()
        if identity and 'Arn' in identity:
            arn = identity['Arn']
            # ARN format: arn:aws:iam::123456789012:user/username
            if '/user/' in arn or ':user/' in arn:
                username = arn.split('/')[-1]
                print(f"✓ Username extracted from ARN: {username}")
                return username
        print(f"❌ ERROR: Could not determine username.")
        return None

def save_policy_to_file(filename="bedrock-full-access-policy.json"):
    """Save the policy to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(BEDROCK_FULL_ACCESS_POLICY, f, indent=2)
    return os.path.abspath(filename)

def apply_inline_policy(username, policy_file):
    """Apply the policy as an inline policy to the user."""
    print(f"\n🚀 Applying Bedrock permissions to user: {username}...")
    print("   Policy type: Inline Policy")
    print("   Policy name: BedrockFullAccess")
    
    try:
        result = subprocess.run(
            [
                'aws', 'iam', 'put-user-policy',
                '--user-name', username,
                '--policy-name', 'BedrockFullAccess',
                '--policy-document', f'file://{policy_file}'
            ],
            capture_output=True,
            text=True,
            check=True
        )
        print("✓ Policy applied successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Failed to apply policy: {e.stderr}")
        return False

def try_managed_policy(username):
    """Try to attach AWS managed Bedrock policy."""
    print(f"\n🚀 Trying to attach AWS Managed Policy (AmazonBedrockFullAccess)...")
    
    try:
        result = subprocess.run(
            [
                'aws', 'iam', 'attach-user-policy',
                '--user-name', username,
                '--policy-arn', 'arn:aws:iam::aws:policy/AmazonBedrockFullAccess'
            ],
            capture_output=True,
            text=True,
            check=True
        )
        print("✓ AWS Managed Policy attached successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠ Could not attach managed policy: {e.stderr.strip()}")
        return False

def verify_policy_applied(username):
    """Verify the policy was applied."""
    print(f"\n🔍 Verifying policies for user: {username}...")
    
    # Check inline policies
    try:
        result = subprocess.run(
            ['aws', 'iam', 'list-user-policies', '--user-name', username],
            capture_output=True,
            text=True,
            check=True
        )
        policies = json.loads(result.stdout)
        inline_policies = policies.get('PolicyNames', [])
        if inline_policies:
            print(f"✓ Inline policies found: {', '.join(inline_policies)}")
    except subprocess.CalledProcessError:
        print("⚠ Could not list inline policies")
    
    # Check attached managed policies
    try:
        result = subprocess.run(
            ['aws', 'iam', 'list-attached-user-policies', '--user-name', username],
            capture_output=True,
            text=True,
            check=True
        )
        policies = json.loads(result.stdout)
        attached_policies = policies.get('AttachedPolicies', [])
        if attached_policies:
            print(f"✓ Attached managed policies:")
            for policy in attached_policies:
                print(f"   - {policy['PolicyName']} ({policy['PolicyArn']})")
    except subprocess.CalledProcessError:
        print("⚠ Could not list attached policies")

def test_bedrock_access():
    """Test if Bedrock access is working."""
    print(f"\n🧪 Testing Bedrock access...")
    print("   Running: python3 ../bedrock.py")
    
    try:
        result = subprocess.run(
            ['python3', '../bedrock.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✓ Bedrock access test PASSED!")
            print("\nSample output:")
            lines = result.stdout.split('\n')[:10]
            for line in lines:
                if line.strip():
                    print(f"   {line}")
            return True
        else:
            print("❌ Bedrock access test FAILED!")
            print(f"\nError output:\n{result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("⚠ Test timed out (this might be normal if there are many models)")
        return None
    except Exception as e:
        print(f"⚠ Could not run test: {e}")
        return None

def main():
    """Main function."""
    print_header()
    
    # Step 1: Check AWS CLI
    if not check_aws_cli():
        sys.exit(1)
    
    # Step 2: Get caller identity
    identity = get_caller_identity()
    if not identity:
        sys.exit(1)
    
    print(f"\n✓ AWS Account ID: {identity.get('Account', 'Unknown')}")
    print(f"✓ AWS ARN: {identity.get('Arn', 'Unknown')}")
    
    # Step 3: Get username
    username = get_username()
    if not username:
        sys.exit(1)
    
    # Step 4: Save policy to file
    print("\n📝 Saving policy to file...")
    policy_file = save_policy_to_file()
    print(f"✓ Policy saved to: {policy_file}")
    
    # Step 5: Try to attach AWS managed policy first (recommended)
    managed_success = try_managed_policy(username)
    
    # Step 6: Apply inline policy (as backup or additional)
    inline_success = apply_inline_policy(username, policy_file)
    
    if not managed_success and not inline_success:
        print("\n❌ FAILED: Could not apply any policies.")
        print("\nPossible reasons:")
        print("  1. You don't have IAM permissions to modify your own user")
        print("  2. You need an administrator to apply these policies")
        print("\nPlease contact your AWS administrator or use the AWS Console.")
        sys.exit(1)
    
    # Step 7: Verify
    verify_policy_applied(username)
    
    # Step 8: Test access
    test_result = test_bedrock_access()
    
    # Final summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    if managed_success or inline_success:
        print("✓ Permissions applied successfully!")
        if test_result == True:
            print("✓ Bedrock access verified - you can now use AWS Bedrock!")
        elif test_result == False:
            print("⚠ Permissions applied but test failed - may need to wait for propagation")
        else:
            print("⚠ Permissions applied but test inconclusive")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
