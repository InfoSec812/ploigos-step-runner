"""`StepImplementer` for the `zaproxy_init` step. This step will initialize and potentially
customize the configuration of Zed Attack Proxy for the automated analysis of web applications
for security vulnerabilities

Step Configuration
------------------
Step configuration expected as input to this step.
Could come from:
* static configuration
* runtime configuration
* previous step results

Configuration Key            | Required? | Default | Description
-----------------------------|-----------|---------|------------
`target-domains`             | Yes       |         | This limits the scope of what ZAP will analyze/scan/attack

Result Artifacts
----------------
Results artifacts output by this step.

Result Artifact Key    | Description
-----------------------|------------
`proxy-host`           | The hostname/service/route of the ZAProxy instance
`proxy-port`           | The port on which ZAProxy listens
`zaproxy-api-key`      | The API Key (either generated on the fly or predefined
"""

import os

import sh

from ploigos_step_runner import StepResult
from ploigos_step_runner.exceptions import StepRunnerException
from ploigos_step_runner.step_implementers.zaproxy.zaproxy_generic import ZAProxyGeneric

#jsonReport = sh(returnStdout: true, script: 'curl http://127.0.0.1:9080/OTHER/core/other/jsonreport')
class ZAProxyReporting(ZAProxyGeneric):
    """

    """
    def _run_step(self):
        zap_host = self.config['proxy-host']
        zap_port = self.config['proxy-port']
        zap_initiate_url = "http://%s:%s/OTHER/core/other/jsonreport"
        zap_shutdown_url = "http://%s:%s/JSON/core/action/shutdown"
        zap_file_output_path = self.config['zap_output_file_path']

        # Fetch JSON Report from ZAP
        json_report = sh.curl(zap_initiate_url % (zap_host, zap_port))

        # Write to file out path
        self.write_working_file(zap_file_output_path, json_report)

        # Add json to stepRunner.addArtifact()

        # Shutdown
        json_report = sh.curl(zap_shutdown_url % (zap_host, zap_port))


