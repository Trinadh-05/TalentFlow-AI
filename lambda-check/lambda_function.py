import json

def lambda_handler(event, context):
    print("TalentFlow AI Resume Processor")
    print("pypdf dependency loaded successfully")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Lambda package is ready"
        })
    }