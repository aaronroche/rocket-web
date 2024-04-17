#!/usr/bin/env python3

import aws_cdk as cdk

from ec2_cdk.ec2_cdk_stack import Ec2CdkStack


app = cdk.App()

Ec2CdkStack(app, "rons-ec2-cdk")

app.synth()
