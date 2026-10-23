from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import boto3
import json
import uuid

S3_BUCKET = "talentflow-ai-resumes-2026"
AWS_REGION = "ap-south-1"
DYNAMODB_TABLE = "TalentFlowApplications"

s3 = boto3.client("s3", region_name=AWS_REGION)
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMODB_TABLE)


app = Flask(__name__)
CORS(app)

# ==========================================
# AWS S3 CONFIGURATION
# ==========================================

S3_BUCKET = "talentflow-ai-resumes-2026"
AWS_REGION = "ap-south-1"

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return jsonify({
        "message": "TalentFlow AI Backend is running"
    })


# ==========================================
# GET ALL JOBS
# ==========================================

@app.route("/jobs")
def jobs():

    with open("jobs.json", "r") as file:
        jobs_data = json.load(file)

    return jsonify(jobs_data)


# ==========================================
# GET JOB BY ID
# ==========================================

@app.route("/jobs/<int:job_id>")
def get_job(job_id):

    with open("jobs.json", "r") as file:
        jobs_data = json.load(file)

    for job in jobs_data:

        if job["id"] == job_id:

            return jsonify(job)

    return jsonify({
        "message": "Job not found"
    }), 404


# ==========================================
# APPLY FOR JOB + UPLOAD RESUME TO S3
# ==========================================

@app.route("/apply", methods=["POST"])
def apply():

    # Get candidate information
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    job_id = request.form.get("job_id")

    # Get uploaded resume
    resume = request.files.get("resume")

    # ------------------------------------------
    # Validate candidate information
    # ------------------------------------------

    if not name or not email or not phone or not job_id:

        return jsonify({
            "message": "All application fields are required"
        }), 400

    # ------------------------------------------
    # Validate resume
    # ------------------------------------------

    if not resume:

        return jsonify({
            "message": "Resume file is required"
        }), 400

    allowed_extensions = {
        "pdf",
        "doc",
        "docx"
    }

    filename = secure_filename(
        resume.filename
    )

    if "." not in filename:

        return jsonify({
            "message": "Invalid resume file"
        }), 400

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    if extension not in allowed_extensions:

        return jsonify({
            "message": "Only PDF, DOC and DOCX files are allowed"
        }), 400

    # ------------------------------------------
    # Generate unique application ID
    # ------------------------------------------

    application_id = str(uuid.uuid4())

    unique_filename = (
        f"applications/{application_id}/{filename}"
    )

    # ------------------------------------------
    # Create candidate application object
    # ------------------------------------------

    application = {
        "application_id": application_id,
        "name": name,
        "email": email,
        "phone": phone,
        "job_id": int(job_id),
        "resume_filename": filename,
        "resume_s3_key": unique_filename
    }

    # ------------------------------------------
    # Save candidate information to DynamoDB
    # ------------------------------------------

    try:

        table.put_item(
            Item={
                "application_id": application_id,
                "name": name,
                "email": email,
                "phone": phone,
                "job_id": int(job_id),
                "resume_filename": filename,
                "resume_s3_key": unique_filename
            }
        )

        print(
            "Candidate application saved to DynamoDB"
        )

    except Exception as error:

        print(
            "DynamoDB Error:",
            error
        )

        return jsonify({
            "message":
                "Application could not be saved to DynamoDB"
        }), 500

    # ------------------------------------------
    # Upload resume to S3
    # ------------------------------------------

    try:

        s3.upload_fileobj(
            resume,
            S3_BUCKET,
            unique_filename,
            ExtraArgs={
                "ContentType": resume.content_type
            }
        )

        print(
            "Resume uploaded to S3 successfully"
        )

    except Exception as error:

        print(
            "S3 Upload Error:",
            error
        )

        return jsonify({
            "message":
                "Resume upload to S3 failed"
        }), 500

    # ------------------------------------------
    # Save application locally
    # ------------------------------------------

    try:

        with open(
            "applications.json",
            "r"
        ) as file:

            applications = json.load(file)

    except FileNotFoundError:

        applications = []

    applications.append(
        application
    )

    with open(
        "applications.json",
        "w"
    ) as file:

        json.dump(
            applications,
            file,
            indent=2
        )

    # ------------------------------------------
    # Success response
    # ------------------------------------------

    return jsonify({

        "message":
            "Application submitted successfully",

        "application":
            application

    }), 201



# ==========================================
# START FLASK SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )