from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json
import os
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return jsonify({
        "message": "TalentFlow AI Backend is running"
    })


@app.route("/jobs")
def jobs():
    with open("jobs.json", "r") as file:
        jobs_data = json.load(file)

    return jsonify(jobs_data)


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


@app.route("/apply", methods=["POST"])
def apply():

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    job_id = request.form.get("job_id")

    resume = request.files.get("resume")

    if not name or not email or not phone or not job_id:
        return jsonify({
            "message": "All application fields are required"
        }), 400

    if not resume:
        return jsonify({
            "message": "Resume file is required"
        }), 400

    allowed_extensions = {"pdf", "doc", "docx"}

    filename = secure_filename(resume.filename)

    if "." not in filename:
        return jsonify({
            "message": "Invalid resume file"
        }), 400

    extension = filename.rsplit(".", 1)[1].lower()

    if extension not in allowed_extensions:
        return jsonify({
            "message": "Only PDF, DOC and DOCX files are allowed"
        }), 400

    unique_filename = f"{uuid.uuid4().hex}_{filename}"

    resume_path = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )

    resume.save(resume_path)

    application = {
        "name": name,
        "email": email,
        "phone": phone,
        "job_id": int(job_id),
        "resume_filename": unique_filename
    }

    with open("applications.json", "r") as file:
        applications = json.load(file)

    applications.append(application)

    with open("applications.json", "w") as file:
        json.dump(applications, file, indent=2)

    return jsonify({
        "message": "Application and resume submitted successfully",
        "application": application
    }), 201


if __name__ == "__main__":
    app.run(debug=True)