from typing import Any, Dict

from aws_cdk.core import Stack, CustomResource, RemovalPolicy

from b_cfn_twilio_activity.function import TwilioActivitySingletonFunction


class TwilioActivityResource(CustomResource):
    """
    Custom resource used for managing a Twilio workspace for a deployment.

    Creates a workspace on stack creation.
    Updates the workspace on workspace name change.
    Deletes the workspace on stack deletion.
    """

    def __init__(
            self,
            scope: Stack,
            activity_function: TwilioActivitySingletonFunction
    ) -> None:
        super().__init__(
            scope=scope,
            id=f'CustomResource{activity_function.function_name}',
            service_token=activity_function.function_arn,
            pascal_case_properties=True,
            removal_policy=RemovalPolicy.DESTROY,
            properties={
                # Created by default.
                'OfflineActivity': self.offline_activity,
                # Created by default.
                'AvailableActivity': self.available_activity,
                # Created by default.
                'UnavailableActivity': self.unavailable_activity,
                # Custom activity, used after finishing a call (post-work activity).
                'WrapUpActivity': self.wrap_up_activity
            }
        )

    @property
    def offline_activity_sid(self) -> str:
        return self.get_att_string('OfflineActivitySid')

    @property
    def offline_activity(self) -> Dict[str, Any]:
        return {
            'friendly_name': 'Offline',
            'availability': False
        }

    @property
    def available_activity_sid(self) -> str:
        return self.get_att_string('AvailableActivitySid')

    @property
    def available_activity(self) -> Dict[str, Any]:
        return {
            'friendly_name': 'Available',
            'availability': True
        }

    @property
    def unavailable_activity_sid(self) -> str:
        return self.get_att_string('UnavailableActivitySid')

    @property
    def unavailable_activity(self) -> Dict[str, Any]:
        return {
            'friendly_name': 'Unavailable',
            'availability': False
        }

    @property
    def wrap_up_activity_sid(self) -> str:
        return self.get_att_string('WrapUpActivitySid')

    @property
    def wrap_up_activity(self) -> Dict[str, Any]:
        return {
            'friendly_name': 'Wrap Up',
            'availability': False
        }
