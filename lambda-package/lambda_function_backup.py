import json
import boto3
import uuid
from decimal import Decimal
from io import BytesIO
from urllib.parse import unquote_plus
from pypdf import PdfReader

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = "TalentFlowApplications"

table = dynamodb.Table(TABLE_NAME)

SKILLS = [
    "AWS",
    "Python",
    "Linux",
    "Docker",
    "Kubernetes",
    "Terraform",
    "Ansible",
    "Git",
    "GitHub",
    "Flask",
    "SQL",
    "Networking",
    "CCNA",
    "CI/CD"
]


def extract_text_from_pdf(pdf_bytes):

    pdf_file = BytesIO(pdf_bytes)

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def detect_skills(text):

    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text_lower:

            found_skills.append(skill)

    return found_skills


def calculate_score(found_skills):

    total_skills = len(SKILLS)

    if total_skills == 0:

        return 0

    score = (
        len(found_skills) /
        total_skills
    ) * 100

    return round(score, 2)


def lambda_handler(event, context):

    print("====================================")
    print("TalentFlow AI Resume Processor")
    print("====================================")

    if "Records" not in event:

        print("No S3 event received")

        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "No S3 event received"
            })
        }

    for record in event["Records"]:

        bucket_name = (
            record["s3"]["bucket"]["name"]
        )

        object_key = unquote_plus(
            record["s3"]["object"]["key"]
        )

        print(f"Bucket: {bucket_name}")
        print(f"Resume: {object_key}")

        try:

            # Read resume from S3
            response = s3.get_object(
                Bucket=bucket_name,
                Key=object_key
            )

            pdf_bytes = response["Body"].read()

            print(
                f"Resume downloaded: "
                f"{len(pdf_bytes)} bytes"
            )

            # Extract PDF text
            resume_text = extract_text_from_pdf(
                pdf_bytes
            )

            print(
                f"Extracted text length: "
                f"{len(resume_text)} characters"
            )

            # Detect skills
            found_skills = detect_skills(
                resume_text
            )

            # Calculate skill match score
            score = calculate_score(
                found_skills
            )

            # Determine screening status
            if score >= 50:

                screening_status = "SHORTLISTED"

            else:

                screening_status = "REVIEW REQUIRED"

            # Generate unique application ID
            application_id = str(
                uuid.uuid4()
            )

            # Save result to DynamoDB
            table.put_item(
                Item={
                    "application_id":
                        application_id,

                    "resume_filename":
                        object_key,

                    "skills_found":
                        found_skills,

                    "skills_count":
                        len(found_skills),

                    "skill_match_score":
                        Decimal(str(score)),

                    "screening_status":
                        screening_status
                }
            )

            print("------------------------------------")
            print("Resume Screening Result")
            print("------------------------------------")

            print(
                f"Skills Found: "
                f"{', '.join(found_skills)}"
            )

            print(
                f"Skills Count: "
                f"{len(found_skills)}"
            )

            print(
                f"Skill Match Score: "
                f"{score}%"
            )

            print(
                f"Screening Status: "
                f"{screening_status}"
            )

            print(
                f"Application ID: "
                f"{application_id}"
            )

            print(
                "Screening result saved to DynamoDB"
            )

            print("------------------------------------")

        except Exception as error:

            print(
                "Resume Processing Error:",
                str(error)
            )

            return {
                "statusCode": 500,
                "body": json.dumps({
                    "message":
                        "Resume processing failed",
                    "error":
                        str(error)
                })
            }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message":
                "Resume processed and screening "
                "result saved successfully"
        })
    }