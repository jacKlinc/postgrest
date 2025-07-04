import aws_cdk as core
import aws_cdk.assertions as assertions

from postgrest_cdk.postgrest_cdk.postgrest_stack import PostgrestCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in postgrest_cdk/postgrest_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PostgrestCdkStack(app, "postgrest-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
