#!/usr/bin/env python3

import aws_cdk as cdk

from ec2_stack.EC2Stack import EC2Stack
from lambda_dynamo_stack.LambdaDynamoStack import LambdaDynamoStack


app = cdk.App()

LambdaDynamoStack(app, "Rocket-Web-Lambda-DB-Stack")
EC2Stack(app, "Rocket-Web-EC2-Stack")

app.synth()
