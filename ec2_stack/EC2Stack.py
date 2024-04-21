import os
from dotenv import load_dotenv
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_dynamodb as dynamodb,
    Fn
)

load_dotenv()   # Load .env file

REACT_APP_AWS_ACCESS_KEY_ID=os.getenv("REACT_APP_AWS_ACCESS_KEY_ID")
REACT_APP_AWS_SECRET_ACCESS_KEY=os.getenv("REACT_APP_AWS_SECRET_ACCESS_KEY")

# Used as substitution for .env within ec2 instance
access_key_mappings = {
    "__REACT_APP_AWS_ACCESS_KEY_ID__" : REACT_APP_AWS_ACCESS_KEY_ID,
    "__REACT_APP_AWS_SECRET_ACCESS_KEY__": REACT_APP_AWS_SECRET_ACCESS_KEY
}

class EC2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        vpc = ec2.Vpc(self, "VPC",
            nat_gateways=0,
            subnet_configuration=[ec2.SubnetConfiguration(name="public",subnet_type=ec2.SubnetType.PUBLIC)],
            availability_zones=["us-east-1a"]
            )

        # AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2023,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            )
        
        # Security group
        security_group = ec2.SecurityGroup(self, "Rocket-Web-EC2-SecurityGroup",
            vpc=vpc,
            description="Allow ssh, http, and https access to ec2 instances",
            allow_all_outbound=False       # Restrict all outbound connections
            )
        
        # Add inbound connections
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow ssh access from the world")
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP access from anywhere")
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(443), "Allow HTTP access from anywhere")

        # Add outbound connections
        security_group.add_egress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(80), description="Allow HTTP outbound")
        security_group.add_egress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(443), description="Allow HTTPS outbound")
        security_group.add_egress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(22), description="Allow SSH outbound")

        # Import existing key pair
        key_pair = ec2.KeyPair.from_key_pair_name(self, "KeyPair", "RonKeyPair")

        # Create reference to DynamoDB table
        table = dynamodb.Table.from_table_name(self, "MyTable", "rocket-web") 

        # Instance Role and SSM Managed Policy
        role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

        # Create and attach DynamoDB read policy to EC2 instance
        read_dynamodb_policy = iam.PolicyStatement(
            actions=["dynamodb:GetItem", "dynamodb:Scan", "dynamodb:Query"],
            resources=[table.table_arn],
            effect=iam.Effect.ALLOW
        )
        role.add_to_policy(read_dynamodb_policy)

        # Userdata to install dependencies and launch webserver upon ec2 launch
        user_data = ec2.UserData.for_linux()
        with open("webscript.sh", 'r') as file:
            webscript_content = file.read()
        user_data.add_commands(
            Fn.sub(webscript_content, access_key_mappings)
        )   

        # Instance
        instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=amzn_linux,
            vpc = vpc,
            role = role,
            user_data=user_data,
            key_pair=key_pair,
            security_group=security_group
            )
