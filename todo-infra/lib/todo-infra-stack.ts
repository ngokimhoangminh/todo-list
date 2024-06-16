import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as lambda from "aws-cdk-lib/aws-lambda";

export class TodoInfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'TodoInfraQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });

    // Create dynamodb table to store the tasks with name "Tasks".
    const table = new dynamodb.Table(this, 'Tasks', {
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      timeToLiveAttribute: "ttl",
    });

    // Add GSI based on user_id
    table.addGlobalSecondaryIndex({
      indexName    : "user-index",
      partitionKey : { name: "user_id", type: dynamodb.AttributeType.STRING },
      sortKey      : { name: "created_time", type: dynamodb.AttributeType.NUMBER },
    });

    // Create Lambda function
    const lambdaFunc = new lambda.Function(this, 'API', {
      runtime: lambda.Runtime.PYTHON_3_10,
      code: lambda.Code.fromAsset("../api/lambda_function.zip"),
      handler: 'todo.handler',
      environment: {
        TABLE_NAME: table.tableName, // Define tables to access and interact with data.
      }
    });

    // Create a URL so we can access the function
    const functionUrl = lambdaFunc.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE,
      cors: {
        // ['*'] to allow all domain.
        allowedOrigins: ["*"],
        allowedMethods: [lambda.HttpMethod.ALL],
        allowedHeaders: ["*"],
      },
    });

    // Output the API function url.
    new cdk.CfnOutput(this, "APIUrl", {
      value: functionUrl.url,
    });

    // Give Lambda permissions to read/write to the table
    table.grantReadWriteData(lambdaFunc)
  }
}