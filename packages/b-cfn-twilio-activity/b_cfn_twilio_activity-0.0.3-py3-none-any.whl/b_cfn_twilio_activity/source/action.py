import base64
import json
import logging
import os
from typing import Dict, Any, Optional, Tuple

from twilio.base.exceptions import TwilioException
from twilio.rest import Client

logger = logging.getLogger(__name__)


class Action:
    def __init__(self, invocation_event: Dict[str, Any]):
        self.__invocation_event: Dict[str, Any] = invocation_event
        self.__parameters: Dict[str, Any] = invocation_event['ResourceProperties']
        self.__resource_id: Optional[str] = invocation_event.get('PhysicalResourceId')

        try:
            self.TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
            self.TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
            self.TWILIO_WORKSPACE_SID = os.environ['TWILIO_WORKSPACE_SID']

            self.TWILIO_OFFLINE_ACTIVITY = self.__parameters['OfflineActivity']
            self.TWILIO_AVAILABLE_ACTIVITY = self.__parameters['AvailableActivity']
            self.TWILIO_UNAVAILABLE_ACTIVITY = self.__parameters['UnavailableActivity']
            self.TWILIO_WRAP_UP_ACTIVITY = self.__parameters['WrapUpActivity']
        except KeyError as ex:
            logger.error(f'Missing environment: {repr(ex)}.')
            raise

        self.client = self.__get_twilio_client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)

    def create(self) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """
        Creates a resource.

        :return: A tuple containing two items:
            1. Custom data to return back to CloudFormation service.
            2. Physical resource id (can be empty).
        """
        logger.info(f'Initiating resource creation with these parameters: {json.dumps(self.__parameters)}.')

        workspace = self.client.taskrouter.workspaces.get(self.TWILIO_WORKSPACE_SID)

        # Find activities created by default.
        offline_activity = workspace.activities.list(
            friendly_name=self.TWILIO_OFFLINE_ACTIVITY['friendly_name'],
            available=self.TWILIO_OFFLINE_ACTIVITY['availability']
        )[0]

        available_activity = workspace.activities.list(
            friendly_name=self.TWILIO_AVAILABLE_ACTIVITY['friendly_name'],
            available=self.TWILIO_AVAILABLE_ACTIVITY['availability']
        )[0]

        unavailable_activity = workspace.activities.list(
            friendly_name=self.TWILIO_UNAVAILABLE_ACTIVITY['friendly_name'],
            available=self.TWILIO_UNAVAILABLE_ACTIVITY['availability']
        )[0]

        # Create defined activities from scratch.
        activity_sids = {
            'OfflineActivitySid': offline_activity.sid,
            'AvailableActivitySid': available_activity.sid,
            'UnavailableActivitySid': unavailable_activity.sid,
            'WrapUpActivitySid': workspace.activities.create(
                friendly_name=self.TWILIO_WRAP_UP_ACTIVITY['friendly_name'],
                available=self.TWILIO_WRAP_UP_ACTIVITY['availability']
            ).sid,
        }

        return activity_sids, base64.b64encode(json.dumps(activity_sids).encode('utf-8')).decode('utf-8')

    def update(self) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """
        Updates a resource.

        :return: A tuple containing two items:
            1. Custom data to return back to CloudFormation service.
            2. Physical resource id (can be empty).
        """
        logger.info(f'Initiating resource update with these parameters: {json.dumps(self.__parameters)}.')

        activity_sids: Dict[str, str] = json.loads(base64.b64decode(self.__resource_id))

        workspace = self.client.taskrouter.workspaces.get(self.TWILIO_WORKSPACE_SID)
        wrap_up_activity = workspace.activities.get(activity_sids['WrapUpActivitySid']).fetch()

        if wrap_up_activity.friendly_name != self.TWILIO_WRAP_UP_ACTIVITY['friendly_name']:
            wrap_up_activity.update(friendly_name=self.TWILIO_WRAP_UP_ACTIVITY['friendly_name'])

        return activity_sids, self.__resource_id

    def delete(self) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """
        Deletes a resource.

        :return: A tuple containing two items:
            1. Custom data to return back to CloudFormation service.
            2. Physical resource id (can be empty).
        """
        logger.info(f'Initiating resource deletion with these parameters: {json.dumps(self.__parameters)}.')

        activity_sids: Dict[str, str] = json.loads(base64.b64decode(self.__resource_id))

        self.client.taskrouter.workspaces.get(self.TWILIO_WORKSPACE_SID).activities.get(activity_sids['WrapUpActivitySid']).delete()

        return activity_sids, self.__resource_id

    @staticmethod
    def __get_twilio_client(account_sid: str, auth_token: str) -> Client:
        """
        Creates a Twilio Client.

        :return: Twilio Client.
        """
        try:
            return Client(username=account_sid, password=auth_token)
        except TwilioException as ex:
            logger.error(f'Could not create Twilio client. Reason: {repr(ex)}.')
            raise
