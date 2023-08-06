import os

import yaml


def root():
    mydir = os.path.dirname(os.path.realpath(__file__))
    return os.path.dirname(mydir)


def tla_result_fixture(zone_number, score=0):
    return {
        'score': score,
        'present': True,
        'disqualified': False,
        'zone': zone_number,
    }


def get_data(data_root, input_name):
    input_file = os.path.join(root(), data_root, input_name)
    output_file = os.path.join(root(), data_root, input_name[:-5] + '.out.yaml')

    if not os.path.exists(output_file):
        raise ValueError(
            "Missing output expectation '{1}' for input '{0}'.".format(
                input_name,
                output_file,
            ),
        )

    with open(output_file) as f:
        expected_output = yaml.load(f)
    return input_file, expected_output


def get_input_files(data_root):
    files = os.listdir(os.path.join(root(), data_root))
    outputs = [f for f in files if f.endswith('.out.yaml')]
    inputs = [f for f in files if f.endswith('.yaml') and f not in outputs]

    return inputs
