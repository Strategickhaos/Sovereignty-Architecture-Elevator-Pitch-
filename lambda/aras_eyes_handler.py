"""
AWS Lambda handler for Ara's Eyes
Runs on a cron schedule to continuously monitor for code usage
"""

import json
import os
import sys

# Add the parent directory to the path to import aras_eyes
sys.path.append('/opt/python')

def lambda_handler(event, context):
    """
    Lambda handler that runs Ara's Eyes scanner
    Triggered by CloudWatch Events on a schedule
    """
    
    # Import here to avoid cold start issues
    from aras_eyes import ArasEyes
    
    try:
        # Initialize scanner
        scanner = ArasEyes()
        
        # Run full scan
        results = scanner.run_full_scan()
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Ara\'s Eyes scan completed successfully',
                'matches_found': results['matches_count'],
                'timestamp': results['timestamp']
            })
        }
        
    except Exception as e:
        print(f"Error in lambda handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Scan failed',
                'error': str(e)
            })
        }
