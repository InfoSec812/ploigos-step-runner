"""Abstract parent class for StepImplementers that use ZAP.

Step Configuration
------------------
Step configuration expected as input to this step.
Could come from:
* static configuration
* runtime configuration
* previous step results

Configuration Key            | Required? | Default | Description
-----------------------------|-----------|---------|-----------
`tls-verify`                 | No        | `True`      | Disables TLS Verification if set to False
`proxy-host`                 | No | `127.0.0.1` | Hostname/IP of the proxy
`proxy-port`                 | No | `8080`    | Port of the proxy
`zaproxy-api-key` | No        | `00000000-0000-0000-0000-000000000000`  | api key for zap
"""


from ploigos_step_runner import StepResult, StepRunnerException
from ploigos_step_runner.config.config_value import ConfigValue
from ploigos_step_runner.step_implementer import StepImplementer
from ploigos_step_runner.utils.zap import run_zap

DEFAULT_CONFIG = {
    'tls-verify': True,
    'proxy-host': '127.0.0.1',
    'proxy-port': 8080,
    'zaproxy-api-key': '95993b18-0698-11ec-82a6-5f29471b38af'
}

REQUIRED_CONFIG_OR_PREVIOUS_STEP_RESULT_ARTIFACT_KEYS = [ 
]

class ZAProxyGeneric(StepImplementer):
    """Abstract parent class for StepImplementers that use Maven.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        workflow_result,
        parent_work_dir_path,
        config,
        environment=None
    ):
        super().__init__(
            workflow_result=workflow_result,
            parent_work_dir_path=parent_work_dir_path,
            config=config,
            environment=environment
        )


    @staticmethod
    def step_implementer_config_defaults():
        """Getter for the StepImplementer's configuration defaults.

        Returns
        -------
        dict
            Default values to use for step configuration values.

        Notes
        -----
        These are the lowest precedence configuration values.
        """
        return DEFAULT_CONFIG

    @staticmethod
    def _required_config_or_result_keys():
        """Getter for step configuration or previous step result artifacts that are required before
        running this step.

        See Also
        --------
        _validate_required_config_or_previous_step_result_artifact_keys

        Returns
        -------
        array_list
            Array of configuration keys or previous step result artifacts
            that are required before running the step.
        """
        return REQUIRED_CONFIG_OR_PREVIOUS_STEP_RESULT_ARTIFACT_KEYS


    def _validate_required_config_or_previous_step_result_artifact_keys(self):
        """Validates that the required configuration keys or previous step result artifacts
        are set and have valid values.

        Validates that:
        * required configuration is given
        * given 'pom-file' exists

        Raises
        ------
        AssertionError
            If step configuration or previous step result artifacts have invalid required values
        """
        super()._validate_required_config_or_previous_step_result_artifact_keys()


    def _run_zap_command(
        self,
        zap_host,
        zap_port,
        zap_output_file_path,
        step_implementer_additional_arguments=None
    ):
        """Runs zap using the configuration given to this step runner.

        Parameters
        ----------
        zap_output_file_path : str
            Path to file containing the maven stdout and stderr output.
        step_implementer_additional_arguments : []
            Additional arguments hard coded by the step implementer.

        Raises
        ------
        StepRunnerException
            If zap returns a none 0 exit code.
        """


        additional_arguments = []
        if step_implementer_additional_arguments:
            additional_arguments = \ 
                step_implementer_additional_arguments + self.get_value('zap-additional-arguments')
        else:
            additional_arguments = self.get_value('zap-additional-arguments')


        run_zap(
            zap_host=zap_host,
            zap_port=zap_port,
            additional_arguments=additional_arguments,
            zap_output_file_path=zap_output_file_path
        )
        
    def _run_step(self): # pylint: disable=too-many-locals
        """Runs the step implemented by this StepImplementer.

        Returns
        -------
        StepResult
            Object containing the dictionary results of this step.
        """
        step_result = StepResult.from_step_implementer(self)

        zap_host = self.get_value('proxy-host')
        zap_port = self.get_value('proxy-port')
        zap_apikey = self.get_value('zaproxy-api-key')

        #package the artifacts
        zap_output_file_path = self.write_working_file('zap_output.txt')
        try:
            self._run_zap_command(
                zap_host=zap_host,
                zap_port=zap_port,
                zap_output_file_path=zap_output_file_path
            )
        except StepRunnerException as error:
            step_result.success = False
            step_result.message = "Error executing ZAProxy command" \
                f"More details may be found in 'zap output' report artifact: {error}"

        finally:
            step_result.add_artifact(
                description="Standard out from ZAP",
                name='zap-output',
                value=zap_output_file_path
            )

         return step_result
