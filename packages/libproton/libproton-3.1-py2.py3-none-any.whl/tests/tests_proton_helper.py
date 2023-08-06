import unittest
from unittest import mock

from libproton import ProtonHelper

from . import helpers


class ProtonHelperTests(unittest.TestCase):
    def assertLoad(self, data_to_load):
        mock_loader = mock.Mock()
        mock_loader.return_value = data_to_load
        ph = ProtonHelper(mock_loader)

        input_ = 'bacon'
        ph.load(input_)

        mock_loader.assert_called_once_with(input_)

        return ph

    def test_load(self):
        loaded_data = {
            'arena_id': 'A',
            'match_number': 1,
            'teams': {
                'TLA1': {
                    'zone': 0,
                },
                'TLA2': {
                    'zone': 2,
                },
            },
        }

        self.assertLoad(loaded_data)

    def test_team_scoresheets(self):
        teams_data_complete = {
            'TLA1': {
                'zone': 0,
                'bacon': 4,
                'present': True,
                'disqualified': False,
            },
            'TLA2': {
                'zone': 2,
                'bacon': 13,
                'present': False,
                'disqualified': True,
            },
        }
        loaded_data = {
            'arena_id': 'A',
            'match_number': 1,
            'teams': {
                'TLA1': {
                    'zone': 0,
                    'bacon': 4,
                    # defaults
                },
                'TLA2': {
                    'zone': 2,
                    'bacon': 13,
                    'present': False,
                    'disqualified': True,
                },
            },
        }

        ph = self.assertLoad(loaded_data)

        team_scoresheets = ph.team_scoresheets

        self.assertEqual(teams_data_complete, team_scoresheets)

    def test_extra_data(self):
        extra_data = 'extra_data'
        loaded_data = {
            'arena_id': 'A',
            'match_number': 1,
            'teams': {
                'TLA1': {
                    'zone': 0,
                    'bacon': 4,
                    # defaults
                },
                'TLA2': {
                    'zone': 2,
                    'bacon': 13,
                    'present': False,
                    'disqualified': True,
                },
            },
            'other': extra_data,
        }

        ph = self.assertLoad(loaded_data)

        actual_data = ph.extra_data

        self.assertEqual(extra_data, actual_data)

    def test_no_extra_data(self):
        loaded_data = {
            'arena_id': 'A',
            'match_number': 1,
            'teams': {
                'TLA1': {
                    'zone': 0,
                    'bacon': 4,
                    # defaults
                },
                'TLA2': {
                    'zone': 2,
                    'bacon': 13,
                    'present': False,
                    'disqualified': True,
                },
            },
        }

        ph = self.assertLoad(loaded_data)

        actual_data = ph.extra_data

        self.assertIsNone(actual_data, "Should return None when no extra data")

    def test_arena_data(self):
        arena_data = 'arena_data'
        loaded_data = {
            'arena_id': 'A',
            'match_number': 1,
            'teams': {
                'TLA1': {
                    'zone': 0,
                    'bacon': 4,
                    # defaults
                },
                'TLA2': {
                    'zone': 2,
                    'bacon': 13,
                    'present': False,
                    'disqualified': True,
                },
            },
            'arena_zones': arena_data,
        }

        ph = self.assertLoad(loaded_data)

        actual_data = ph.arena_data

        self.assertEqual(arena_data, actual_data)

    def test_no_arena_data(self):
        loaded_data = {
            'arena_id': 'A',
            'match_number': 1,
            'teams': {
                'TLA1': {
                    'zone': 0,
                    'bacon': 4,
                    # defaults
                },
                'TLA2': {
                    'zone': 2,
                    'bacon': 13,
                    'present': False,
                    'disqualified': True,
                },
            },
        }

        ph = self.assertLoad(loaded_data)

        actual_data = ph.arena_data

        self.assertIsNone(actual_data, "Should return None when no arena data")

    def test_produce(self):
        input_ = {
            'arena_id': 'A',
            'match_number': 1,
            'teams': {
                'TLA1': {
                    'zone': 0,
                },
                'TLA2': {
                    'zone': 2,
                    'present': False,
                    'disqualified': True,
                },
            },
        }

        mock_loader = mock.Mock()
        mock_loader.return_value = input_
        ph = ProtonHelper(mock_loader)
        ph.load(None)

        scores = {'TLA1': 0, 'TLA2': 13}

        whole = ph.produce(scores)

        self.assertEqual('3.0.0-rc2', whole['version'])
        self.assertEqual(1, whole['match_number'])
        self.assertEqual('A', whole['arena_id'])
        self.assertEqual(
            {
                'TLA1': helpers.tla_result_fixture(0, 0),
                'TLA2': {
                    'score': 13,
                    'zone': 2,
                    # while not sane these are expected to be pass-through
                    'present': False,
                    'disqualified': True,
                },
            },
            whole['scores'],
        )
