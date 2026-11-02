# TalentFlow AI – AI-Powered Recruitment and Talent Management System

## Project Overview

TalentFlow AI is a cloud-based resume-screening prototype developed as part of the Davine Technologies AWS Cloud Internship.

The project demonstrates how AWS services can automate the initial stage of resume screening by extracting technical skills from PDF resumes, calculating a rule-based skill-match score, and storing screening results.

## Technologies Used

* Python
* Flask
* Boto3
* Amazon S3
* AWS Lambda
* Amazon DynamoDB
* AWS IAM
* Amazon CloudWatch
* pypdf
* HTML, CSS, and JavaScript

## Project Workflow

1. A user uploads a resume in PDF format.
2. The resume is stored in Amazon S3.
3. The upload triggers the Lambda processing workflow.
4. Lambda extracts resume text using pypdf.
5. The application detects predefined technical skills.
6. A rule-based skill-match percentage is calculated.
7. A candidate classification is generated.
8. The screening result is stored in DynamoDB.
9. CloudWatch logs are used to monitor execution and troubleshoot issues.


Step 1: The user uploads a resume

The user selects a PDF file through the TalentFlow-AI application.

Step 2: The resume is stored in S3

The application uploads the PDF to the configured S3 bucket.

Bucket: talentflow-ai-resumes-2026

Step 3: S3 triggers Lambda

The configured S3 event notification triggers the Lambda processing workflow.

Lambda starts executing the relevant Python code.

Step 4: Lambda retrieves the PDF

Lambda accesses the uploaded document from S3 using the permissions configured for its execution role.

Step 5: The application extracts the text

The pypdf library reads the PDF and extracts its text.

Step 6: The application detects skills

The extracted text is checked against the predefined technical-skill list.

For the documented test, seven skills were detected.

Step 7: The application calculates a score

The system calculates the percentage-based skill-match score.

The documented result was 50.0%.

Step 8: The application classifies the candidate

The system applies its configured screening rule.

The documented classification was SHORTLISTED.

Step 9: The result is stored

The screening information is saved in DynamoDB.

Step 10: The execution is monitored

CloudWatch records Lambda execution logs, allowing you to verify processing and investigate errors.

Step 11: The result is reviewed

The screening result can be reviewed by the user or recruiter.


## Project Status

This project is an internship prototype demonstrating an AWS-based serverless resume-screening workflow.

## Security Notes

* Do not commit AWS access keys, secret keys, passwords, or private credentials.
* Configure AWS credentials securely in the local development environment.
* Review IAM permissions before deploying the application.
* Do not include real candidate resumes or personal information in this public repository.

## Author

Developed as part of the Davine Technologies AWS Cloud Internship.

## Disclaimer

The skill-matching functionality uses predefined rules. The screening result is intended to assist initial review and should not replace human recruitment decisions.
