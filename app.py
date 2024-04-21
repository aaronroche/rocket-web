#!/usr/bin/env python3

import aws_cdk as cdk

from ec2_stack.EC2Stack import EC2Stack
from lambda_dynamo_stack.LambdaDynamoStack import LambdaDynamoStack


app = cdk.App()

LambdaDynamoStack(app, "rc-db")
EC2Stack(app, "rc-ec2")

app.synth()
