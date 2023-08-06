import os
import unittest
import subprocess

import yaml

from . import helpers


class CLITests(unittest.TestCase):
    def get_bacon_scorer(self):
        my_dir = os.path.dirname(os.path.realpath(__file__))
        bacon_scorer = os.path.join(my_dir, 'data/cli/bacon_scorer.py')
        self.assertTrue(
            os.path.exists(bacon_scorer),
            f"{bacon_scorer!r} does not exist",
        )

        return bacon_scorer

    def run_scorer(self, relative_path):
        bacon_scorer = self.get_bacon_scorer()
        process = subprocess.Popen([bacon_scorer, relative_path],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr

    def assertRun(self, relative_path):
        retcode, stdout, stderr = self.run_scorer(relative_path)
        if retcode != 0:
            print(stderr)

        self.assertEqual(0, retcode, "Bad return code scoring '{0}'.".format(relative_path))

        result_dict = yaml.load(stdout)
        return result_dict

    def test_input_file(self):
        inputs = helpers.get_input_files('tests/data/cli')

        for input_name in inputs:
            with self.subTest(input_name):
                input_file, expected_output = helpers.get_data('tests/data/cli', input_name)

                output = self.assertRun(input_file)

                self.assertEqual(
                    expected_output,
                    output,
                    "Incorrect scores for '{0}'.".format(input_name),
                )

    def test_stdin(self):
        # A proton compliant program MUST consume YAML from stdin
        # if it is not given a filename.

        with open('tests/data/cli/zero.yaml', 'r') as zeros_input:
            with open('tests/data/cli/zero.out.yaml') as f:
                zeros_output = yaml.load(f)

            bacon_scorer = self.get_bacon_scorer()
            process = subprocess.Popen([bacon_scorer], stdin=zeros_input,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                print(stderr)

            self.assertEqual(0, process.returncode, "Bad return code scoring from stdin.")

            result_dict = yaml.load(stdout)

            self.assertEqual(zeros_output, result_dict, "Bad output when reading from stdin")

    def test_missing_file(self):
        nope = 'bacon'
        self.assertFalse(os.path.exists(nope), f"{nope!r} path unexpectedly exists")
        retcode, _, _ = self.run_scorer(nope)
        self.assertEqual(
            1,
            retcode,
            "Should error when nonexistent input file '{}' is provided.".format(
                nope,
            ),
        )
