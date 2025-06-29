#!/usr/bin/env python3
import aws_cdk as cdk
from postgrest_cdk.postgrest_stack import PostgrestStack

app = cdk.App()
PostgrestStack(app, "PostgrestStack")
app.synth()
