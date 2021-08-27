"""Test for zap.py

Test for the utility for zap operations.
"""
import re
from io import BytesIO, StringIO, TextIOWrapper
from unittest import mock
from unittest.mock import patch, call, mock_open

import sh
from ploigos_step_runner.exceptions import StepRunnerException
from ploigos_step_runner.utils.zap import *
from testfixtures import TempDirectory
from tests.helpers.base_test_case import BaseTestCase
from tests.helpers.test_utils import Any


class TestZapUtils_run_zap(BaseTestCase):
    @patch('sh.__init__')
    @patch('ploigos_step_runner.utils.zap.create_sh_redirect_to_multiple_streams_fn_callback')
    @patch("builtins.open", new_callable=mock_open)
    def test_success_defaults(self, mocksh, mock_open, redirect_mock):
        call_mock = mock.Mock()
        mocksh.Command = call_mock

        with TempDirectory() as temp_dir:
            zap_output_file_path = os.path.join(temp_dir.path, 'zap_output.txt')
            zap_host = "127.0.0.1"
            zap_port = "8080"
             

            run_zap(
                zap_host=zap_host,
                zap_port=zap_port,
                zap_output_file_path=zap_output_file_path,
            )

            file_descriptor = mock.Mock()
            mock_open.side_effect = file_descriptor

            # mock_open.assert_called_with(zap_output_file_path, 'w')
            # redirect_mock.assert_has_calls([
            #     call([
            #         sys.stdout,
            #         file_descriptor
            #     ]),
            #     call([
            #         sys.stderr,
            #         file_descriptor
            #     ])
            # ])

            mocksh.assert_called_once_with(
                '/zap/zap.sh'
            )

            call_mock.assert_called_once_with(
                '-daemon',
                '-dir', '/home/.ZAP',
                '-host', '/fake/pom.xml',
                '-port', '/fake/settings.xml',
                _out=Any(StringIO),
                _err=Any(StringIO)
            )
