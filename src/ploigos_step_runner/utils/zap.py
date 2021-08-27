"""Shared utils for zap operations.
"""
import os
import sys

import sh
from ploigos_step_runner.exceptions import StepRunnerException
from ploigos_step_runner.utils.io import \
    create_sh_redirect_to_multiple_streams_fn_callback


def run_zap( #pylint: disable=too-many-arguments
    *args,
    zap_output_file_path='/tmp/zap_command_output.txt'
):
    """Runs zap using the given configuration.

    Parameters
    ----------
    zap_output_file_path : str
        Path to file containing the maven stdout and stderr output.
    additional_arguments : [str]
        List of additional arguments to use.

    Raises
    ------
    StepRunnerException
        If zap returns a none 0 exit code.
    """

    # run zap
    try:
        with open(zap_output_file_path, 'w') as zap_output_file:
            out_callback = create_sh_redirect_to_multiple_streams_fn_callback([
                sys.stdout,
                zap_output_file
            ])
            err_callback = create_sh_redirect_to_multiple_streams_fn_callback([
                sys.stderr,
                zap_output_file
            ])

            zapcmd = sh.Command("/zap/zap.sh")
            zapcmd( # pylint: disable=no-member
                '-dir',
                '/home/.ZAP',
                *args,
                _out=out_callback,
                _err=err_callback
            )
    except sh.ErrorReturnCode as error:
        raise StepRunnerException(
            f"Error running zap. {error}"
        ) from error
