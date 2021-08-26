from ploigos_step_runner import StepImplementer, StepResult, StepRunnerException

DEFAULT_CONFIG = {
    'proxy-host': '127.0.0.1',
    'proxy-port': 8080,
    'zaproxy-api-key': '95993b18-0698-11ec-82a6-5f29471b38af'
}


class ZAProxyGeneric(StepImplementer):
    """

    """

    def __init__(
            self,
            workflow_result,
            parent_work_dir_path,
            config,
            environment=None
    ):
        super().__init__(workflow_result, parent_work_dir_path, config, environment)

    @staticmethod
    def _required_config_or_result_keys():
        pass

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
        return {**ZAProxyGeneric.step_implementer_config_defaults(), **DEFAULT_CONFIG}

    def _run_zap_command(self, args):
        return

    def _run_step(self):
        step_result = StepResult.from_step_implementer(self)

        try:
            self._run_zap_command(
                args=["-daemon"]
            )
        except StepRunnerException as error:
            step_result.success = False
            step_result.message = "Error executing ZAProxy command" \
                f"More details may be found in 'zap output' report artifact: {error}"
            return
