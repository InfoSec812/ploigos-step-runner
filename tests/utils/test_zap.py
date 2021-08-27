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

    @patch('sh.Command')
    @patch('ploigos_step_runner.utils.zap.create_sh_redirect_to_multiple_streams_fn_callback')
    @patch("builtins.open", new_callable=mock_open)
    def test_success_defaults(self, mock_open, redirect_mock, mocksh):

        file_descriptor = mock.Mock()
        mock_open().return_value = file_descriptor

        with TempDirectory() as temp_dir:
            zap_output_file_path = os.path.join(temp_dir.path, 'zap_output.txt')

            run_zap(
                '-cmd', 
                '-h',
                zap_output_file_path=zap_output_file_path
            )

            mock_open.assert_called_with(zap_output_file_path, 'w')
            redirect_mock.assert_has_calls([
                call([
                    sys.stdout,
                    mock.ANY
                ]),
                call([
                    sys.stderr,
                    mock.ANY
                ])
            ])

            mocksh.assert_called_once_with(
                '/zap/zap.sh'
            )

            mocksh().assert_called_once_with(
                '-dir', '/home/.ZAP',
                '-cmd',
                '-h',
                _out=Any(StringIO),
                _err=Any(StringIO)
            )

    @patch('sh.Command')
    @patch('ploigos_step_runner.utils.zap.create_sh_redirect_to_multiple_streams_fn_callback')
    @patch("builtins.open", new_callable=mock_open)
    def test_failure_defaults(self, mock_open, redirect_mock, mocksh):

        file_descriptor = mock.Mock()
        mock_open().return_value = file_descriptor

        with TempDirectory() as temp_dir:
            zap_output_file_path = os.path.join(temp_dir.path, 'zap_output.txt')

            mocksh.side_effect = sh.ErrorReturnCode('zap', b'mock stdout', b'mock error')
            
            with self.assertRaisesRegex(
                StepRunnerException,
                re.compile(
                    r"Error running zap."
                    r".*RAN: zap"
                    r".*STDOUT:"
                    r".*mock stdout"
                    r".*STDERR:"
                    r".*mock error",
                    re.DOTALL
                )
            ):
                run_zap(
                    '-cmd', 
                    '-h',
                    zap_output_file_path=zap_output_file_path
                )

                mock_open.assert_called_with(zap_output_file_path, 'w')
           
                redirect_mock.assert_has_calls([
                    call([
                        sys.stdout,
                        mock.ANY
                    ]),
                    call([
                        sys.stderr,
                        mock.ANY
                    ])
                ])

                mocksh.assert_called_once_with(
                    '/zap/zap.sh'
                )

                mocksh().assert_called_once_with(
                    '-dir', '/home/.ZAP',
                    '-cmd',
                    '-h',
                    _out=Any(StringIO),
                    _err=Any(StringIO)
                )
