# Serverless Tasks API with AWS Lambda and DynamoDB

This is a simple example of a RESTful API built with AWS Lambda and DynamoDB. The API allows you to create, read, update, and delete tasks.

## Run locally

```bash
# Run the local DynamoDB instance
docker compose up 
```

```bash
export AWS_ACCESS_KEY_ID=abc && export AWS_SECRET_ACCESS_KEY=abc && export AWS_DEFAULT_REGION=eu-central-1 && export TABLE_NAME="local-tasks-api-table" && export DYNAMODB_URL=http://localhost:9999
```

```bash
python create_dynamodb_locally.py
```

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

```bash
# Create a task
 curl --location --request POST 'http://localhost:8000/api/create-task' \
--header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2duaXRvOnVzZXJuYW1lIjoiam9obkBkb2UuY29tIn0.6UvNP3lIrXAinXYqH4WzyNrYCxUFIRhAluWyAxcCoUc' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Jump"
}'
```

```bash
# List open tasks
curl --location --request GET 'http://localhost:8000/api/open-tasks' \
--header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2duaXRvOnVzZXJuYW1lIjoiam9obkBkb2UuY29tIn0.6UvNP3lIrXAinXYqH4WzyNrYCxUFIRhAluWyAxcCoUc'
```

```bash