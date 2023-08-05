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
                'OfflineActivity': {
                    'friendly_name': 'Offline',
                    'availability': False
                },
                # Created by default.
                'AvailableActivity': {
                    'friendly_name': 'Available',
                    'availability': True
                },
                # Created by default.
                'UnavailableActivity': {
                    'friendly_name': 'Unavailable',
                    'availability': False
                },
                # Custom activity, used after finishing a call (post-work activity).
                'WrapUpActivity': {
                    'friendly_name': 'Wrap Up',
                    'availability': False
                }
            }
        )

    @property
    def offline_activity_sid(self):
        return self.get_att_string('OfflineActivitySid')

    @property
    def available_activity_sid(self):
        return self.get_att_string('AvailableActivitySid')

    @property
    def unavailable_activity_sid(self):
        return self.get_att_string('UnavailableActivitySid')

    @property
    def wrap_up_activity_sid(self):
        return self.get_att_string('WrapUpActivitySid')
