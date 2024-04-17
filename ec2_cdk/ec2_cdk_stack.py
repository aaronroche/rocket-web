import os
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2,
    Fn
)

class Ec2CdkStack(Stack):

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
        security_group = ec2.SecurityGroup(self, "Ron-ec2-SecurityGroup",
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

        # Userdata to execute bash script upon ec2 launch
        user_data = ec2.UserData.for_linux()
        with open("webscript.sh", 'r') as file:
            webscript_content = file.read()
        user_data.add_commands(
            Fn.sub(webscript_content)
        )

        # Instance Role and SSM Managed Policy
        role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

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
