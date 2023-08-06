import json
import logging
import boto3
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)


class Action:
    def __init__(self, invocation_event: Dict[str, Any]):
        self.__invocation_event: Dict[str, Any] = invocation_event
        self.__parameters: Dict[str, Any] = invocation_event['ResourceProperties']
        self.__api_id = self.__parameters['ApiId']
        self.__stage_name = self.__parameters['StageName']
        self.__description = self.__parameters['Description']
        self.__client = boto3.client('apigatewayv2')

    def create(self) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """
        Creates a resource.

        :return: A tuple containing two items:
            1. Custom data to return back to CloudFormation service.
            2. Physical resource id (can be empty).
        """
        logger.info(f'Initiating resource creation with these parameters: {json.dumps(self.__parameters)}.')

        self.__client.create_deployment(
            ApiId=self.__api_id,
            Description=self.__description,
            StageName=self.__stage_name
        )

        return {}, None

    def update(self) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """
        Updates a resource.

        :return: A tuple containing two items:
            1. Custom data to return back to CloudFormation service.
            2. Physical resource id (can be empty).
        """
        logger.info(f'Initiating resource update with these parameters: {json.dumps(self.__parameters)}.')

        # Creation and update should both result in a new deployment.
        return self.create()

    def delete(self) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """
        Actually it makes no sense to delete a deployment. What does it even mean to delete
        a deployment? In a matter of fact, if you attempt to delete a deployment without
        deleting a stage first, you would get an error from CloudFormation:

        Active stages pointing to this deployment must be moved or deleted
        (Service: AmazonApiGatewayV2; Status Code: 400; Error Code: BadRequestException;
        Request ID: <some-random-generated-id>; Proxy: null)

        Hence, this function does nothing, effectively solving all bugs that original
        deployment resource has.

        :return: A tuple containing two items:
            1. Custom data to return back to CloudFormation service.
            2. Physical resource id (can be empty).
        """
        return {}, None
