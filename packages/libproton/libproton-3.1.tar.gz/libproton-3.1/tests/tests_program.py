import unittest
from io import StringIO
from unittest import mock

import yaml

from libproton import program

from . import helpers


class ProgramTests(unittest.TestCase):
    @mock.mock_open()
    def test_get_reader_file(self, open_mock):
        mock_default = mock.Mock()
        open_mock.return_value = open_return = mock.Mock()

        file_name = 'bees'
        reader = program.get_reader(['self', file_name], mock_default)

        self.assertIs(open_return, reader, 'Should have returned the file reader')

        open_mock.assert_called_once_with(file_name, 'r')

    @mock.mock_open()
    def test_get_reader_default(self, open_mock):
        mock_default = mock.Mock()
        open_mock.return_value = mock.Mock()

        reader = program.get_reader(['self'], mock_default)

        self.assertIs(mock_default, reader, 'Should have returned the file reader')

        self.assertFalse(open_mock.called)

    def test_get_reader_help(self):
        for arg in ('-h', '--help'):
            with self.subTest(arg):
                mock_default = mock.Mock()
                with self.assertRaises(SystemExit) as cm:
                    program.get_reader(['self', arg], mock_default)

                    self.assertIn("Usage: ", cm.exception.args[0])
                    self.assertIn(" self ", cm.exception.args[0])

    def test_inner_error(self):
        mock_helper_cls = mock.Mock()
        mock_helper = mock.Mock(extra_data='extra_data')
        mock_helper_cls.return_value = mock_helper

        mock_reader = mock.Mock()
        mock_reader.read = mock.Mock(return_value='')

        mock_scorer = mock.Mock()
        exception_message = 'Boom!'
        mock_scorer.side_effect = Exception(exception_message)

        fake_stderr = StringIO()

        with mock.patch('libproton.program.ProtonHelper', mock_helper_cls):
            with self.assertRaises(SystemExit) as cm:
                program.generate_output(mock_reader, mock_scorer, fake_stderr)

            self.assertEqual(2, cm.exception.code)

            output = fake_stderr.getvalue()
            self.assertIn('Traceback', output)
            self.assertIn(exception_message, output)

    def test_no_validation(self):
        mock_helper_cls = mock.Mock()
        mock_helper = mock.Mock(extra_data='extra_data')
        mock_helper_cls.return_value = mock_helper

        mock_reader = mock.Mock()
        mock_reader.read = mock.Mock(return_value='')

        scores = 'SCORES'
        mock_calc_scores = mock.Mock(return_value=scores)
        mock_scorer = mock.Mock(spec=['calculate_scores'],
                                calculate_scores=mock_calc_scores)
        mock_scorer_cls = mock.Mock(return_value=mock_scorer)

        fake_stderr = StringIO()

        with mock.patch('libproton.program.ProtonHelper', mock_helper_cls):
            program.generate_output(mock_reader, mock_scorer_cls, fake_stderr)

            mock_helper.produce.assert_called_with(scores)

    # helper for system tests

    def run_full_system(self, input_stream, expected_output):
        mock_io = mock.Mock()
        mock_io.stdout = StringIO()
        mock_io.stderr = StringIO()
        mock_io.stdin = input_stream
        mock_io.argv = ['test']

        class Scorer:
            def __init__(self, teams_data, arena_data):
                self._teams_data = teams_data
                self._arena_data = arena_data or {}

            def calculate_scores(self):
                scores = {}
                for name, data in self._teams_data.items():
                    zone = data["zone"]
                    zone_score = self._arena_data.get(zone, {}).get('tokens', 0)
                    scores[name] = zone + zone_score
                return scores

        program.main(Scorer, io=mock_io)

        print('stdout:\n', mock_io.stdout.getvalue())
        print('stderr:\n', mock_io.stderr.getvalue())
        print(yaml.dump(expected_output))
        output = yaml.load(mock_io.stdout.getvalue())
        self.assertEqual(expected_output, output)

    def test_system(self):
        for data_file in helpers.get_input_files('tests/data/system'):
            with self.subTest(data_file):
                data_input, data_output = helpers.get_data('tests/data/system',
                                                           data_file)
                with open(data_input) as input_file:
                    self.run_full_system(input_file, data_output)
