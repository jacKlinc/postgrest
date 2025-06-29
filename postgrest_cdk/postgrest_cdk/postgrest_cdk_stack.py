from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_lambda as _lambda,
    aws_logs as logs,
    RemovalPolicy,
    Duration,
)
from constructs import Construct

class PostgrestStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create VPC with default settings (2 AZs, subnets etc)
        vpc = ec2.Vpc(self, "PostgrestVPC", max_azs=2)

        # Create security group for RDS
        rds_sg = ec2.SecurityGroup(self, "RDSSecurityGroup", vpc=vpc, description="Allow Lambda access to RDS")
        
        # Allow Lambda SG to connect on default postgres port (5432)
        # We'll create Lambda SG next and allow it here.

        # Create RDS Postgres instance
        db_instance = rds.DatabaseInstance(
            self, "PostgresInstance",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_13_4),
            vpc=vpc,
            credentials=rds.Credentials.from_generated_secret("jack"),  # Creates username 'jack' and a generated password in Secrets Manager
            multi_az=False,
            allocated_storage=20,
            max_allocated_storage=100,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            security_groups=[rds_sg],
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False,
            publicly_accessible=False,
        )

        # Create RDS Proxy
        rds_proxy = rds.DatabaseProxy(
            self, "RDSProxy",
            proxy_target=rds.ProxyTarget.from_instance(db_instance),
            secrets=[db_instance.secret],
            vpc=vpc,
            security_groups=[rds_sg],
            require_tls=True,
            idle_client_timeout=Duration.minutes(30),
        )

        # Create security group for Lambda and allow outbound DB traffic
        lambda_sg = ec2.SecurityGroup(self, "LambdaSecurityGroup", vpc=vpc, description="Allow Lambda to access RDS Proxy")
        lambda_sg.add_egress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(5432), "Allow outbound to Postgres port")

        # Allow Lambda SG access on port 5432 to RDS SG
        rds_sg.add_ingress_rule(lambda_sg, ec2.Port.tcp(5432), "Allow Lambda SG inbound on Postgres port")

        # Create Lambda function inside the VPC with Lambda SG
        lambda_fn = _lambda.Function(
            self, "PostgrestLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_handler.handler",
            code=_lambda.Code.from_asset("lambda"),  # assumes a lambda/ directory with code
            vpc=vpc,
            security_groups=[lambda_sg],
            environment={
                "DB_SECRET_ARN": rds_proxy.secret.secret_arn,
                "DB_PROXY_ENDPOINT": rds_proxy.endpoint,
                "DB_NAME": db_instance.instance_identifier,
            },
            timeout=Duration.seconds(10),
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        # Grant Lambda permission to read DB credentials from Secrets Manager
        rds_proxy.secret.grant_read(lambda_fn)

        # Output useful info
        cdk.CfnOutput(self, "RDSProxyEndpoint", value=rds_proxy.endpoint)
        cdk.CfnOutput(self, "LambdaFunctionName", value=lambda_fn.function_name)
