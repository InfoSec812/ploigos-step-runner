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

from ploigos_step_runner import StepResult
from ploigos_step_runner.exceptions import StepRunnerException
from ploigos_step_runner.step_implementers.zaproxy.zaproxy_generic import ZAProxyGeneric


class ZAProxyInit(ZAProxyGeneric):
    """

    """
