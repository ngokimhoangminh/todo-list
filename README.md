# To-do List API

A to-do list API, with a Python FastAPI backend. It is hosted on serverless AWS infrastructure (using Lambda and DynamoDB).

## API Folder

The `/api` folder contains the Python FastAPI code. Run this shell script to build the code into a zip (required for CDK to upload to Lambda):

```bash
# Only work on UNIX (Mac/Linux) systems!
./package_for_lambda.sh
```

This should generate a `lambda_function.zip`.

## Infrastructure Folder

The `/todo-infra` folder contains the CDK code to deploy all the infrastructure (Lambda function and DynamoDB table) to your AWS account.

You must have [AWS CLI](https://aws.amazon.com/cli/) configured, and [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) installed on your machine.

First, install the node modules.

```bash
npm install
```

Then run bootstrap if you never used CDK with your account before.

```bash
cdk bootstrap
```

Now you can use this to deploy.

```bash
cdk deploy
```

## Test Folder

The `/test` folder contains the Pytest integration tests you can use to test your endpoint directly. Don't forget to change your `API` to the one you want to use (in `test_api_integration.py`).

You can run the test like this (but you have to have `pytest` installed):

```bash
pytest
```

Or run each test file

```bash
pytest test_api_integration.py
```
