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
