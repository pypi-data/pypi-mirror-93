from aws_cdk.core import Stack, CustomResource, RemovalPolicy

from b_stage_deployment.function import StageDeploymentSingletonFunction


class StageDeploymentResource(CustomResource):
    """
    Custom resource used for create a custom stage deployment.
    """

    def __init__(
            self,
            scope: Stack,
            resource_name: str,
            deployment_function: StageDeploymentSingletonFunction,
            api_id: str,
            stage_name: str,
            description: str
    ) -> None:
        """
        Constructor.

        :param scope: CloudFormation template stack in which this resource will belong.
        :param resource_name: Custom name for a resource.
        :param deployment_function: Resource function.
        :param api_id: Identification string of an api for which a deployment should be managed.
        :param stage_name: The name of the stage belonging to an api.
        :param description: Deployment description.
        """
        super().__init__(
            scope=scope,
            id=resource_name,
            service_token=deployment_function.function_arn,
            pascal_case_properties=True,
            removal_policy=RemovalPolicy.DESTROY,
            properties={
                'ApiId': api_id,
                'StageName': stage_name,
                'Description': description
            }
        )
