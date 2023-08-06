import logging

from b_aws_testing_framework.credentials import Credentials
from b_stage_deployment_test.testing_infrastructure import TestingInfrastructure

logger = logging.getLogger(__name__)


def test_deployed() -> None:
    """
    Tests that deployments were created and stage was deployed.

    :return: No return.
    """
    response = Credentials().boto_session.client('apigatewayv2').get_deployments(
        ApiId=TestingInfrastructure.get_output('ApiId'),
        MaxResults='25'
    )

    items = response['Items']

    print(len(items))
    print(items)

    assert len(list(items)) >= 5

    for deployment in items:
        assert deployment['AutoDeployed'] is False
        assert deployment['DeploymentStatus'] == 'DEPLOYED'
