from functools import lru_cache

from aws_cdk.aws_iam import PolicyStatement
from aws_cdk.aws_lambda import Code, SingletonFunction, Runtime
from aws_cdk.core import Stack, Duration


class StageDeploymentSingletonFunction(SingletonFunction):
    """
    Custom api gateway stage deployment resource singleton lambda function.
    """

    def __init__(
            self,
            scope: Stack,
            name: str
    ) -> None:
        """
        Constructor.

        :param scope: CloudFormation stack in which this function will be deployed.
        :param name: The name of the function.
        """
        self.__name = name

        super().__init__(
            scope=scope,
            id=name,
            uuid=f'{name}-uuid',
            function_name=name,
            code=self.__code(),
            handler='index.handler',
            runtime=Runtime.PYTHON_3_8,
            timeout=Duration.minutes(1),
        )

        # Add permission to create deployments. Since this is a singleton lambda function,
        # we can not specify a specific api gateway resource.
        self.add_to_role_policy(PolicyStatement(
            actions=['apigateway:POST', 'apigateway:PATCH'],
            resources=['*']
        ))

    @lru_cache
    def __code(self) -> Code:
        """
        Gets (and caches) source code cor the lambda function.

        :return: Lambda function source code (as an asset).
        """
        from .source import root
        return Code.from_asset(root)

    @property
    def function_name(self) -> str:
        """
        Overrides original function_name function so the method would not create a dependency.

        :return: Name of the function.
        """
        return self.__name
