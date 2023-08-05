import json
from typing import Optional

from aws_cdk.core import Stack, CustomResource, RemovalPolicy

from b_cfn_twilio_workflow.function import TwilioWorkflowSingletonFunction


class TwilioWorkflowResource(CustomResource):
    """
    Custom resource used for managing a Twilio workflow for a deployment.

    Creates a workflow on stack creation.
    Updates the workflow on workflow name change.
    Deletes the workflow on stack deletion.
    """

    def __init__(
            self,
            scope: Stack,
            workflow_function: TwilioWorkflowSingletonFunction,
            workflow_name: str,
            task_queue_sid: str,
            assignment_callback_url: Optional[str] = None,
            fallback_assignment_callback_url: Optional[str] = None,
            task_reservation_timeout: Optional[int] = None
    ) -> None:
        """

        :param scope: CloudFormation template stack in which this resource will belong.
        :param workflow_function: Resource function.
        :param workflow_name: Name that will be provided to the created Workflow.
        :param task_queue_sid: TaskQueue that will be assigned as default queue for this Workflow.
        :param assignment_callback_url: Endpoint URL where Twilio will get instructions how to assign a call to a worker.
        :param fallback_assignment_callback_url: Secondary assignment endpoint URL.
        :param task_reservation_timeout: This is the value (in seconds), on how long a task should be reserved before going to the next matching worker.
        """
        super().__init__(
            scope=scope,
            id=f'CustomResource{workflow_function.function_name}',
            service_token=workflow_function.function_arn,
            pascal_case_properties=True,
            removal_policy=RemovalPolicy.DESTROY,
            properties={
                'TwilioWorkflowName': workflow_name,
                'WorkflowConfiguration': json.dumps({
                    'task_routing': {
                        'filters': [],
                        'default_filter': {
                            'queue': task_queue_sid
                        }
                    }
                }),
                'AssignmentCallbackUrl': assignment_callback_url,
                'FallbackAssignmentCallbackUrl': fallback_assignment_callback_url,
                'TaskReservationTimeout': task_reservation_timeout
            }
        )

    @property
    def workflow_sid(self):
        return self.get_att_string("WorkflowSid")
