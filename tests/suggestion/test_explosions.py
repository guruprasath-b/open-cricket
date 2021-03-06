import glob
import os
from os.path import basename
import unittest
from opencricket.chart.syntax_cache import SyntaxCache

from opencricket.suggestion.productions import Productions


class TestProductions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        SyntaxCache().build_cache()

    def setUp(self):
        self.expansions = {
            "word_in": "in",
            "word_year": "year",
            "word_by": "by",
            "word_between": "between",
            "word_with": "with",
            "word_matches": "matches",
            "word_batting": "batting",
            "word_left": "left",
            "word_scoring": "scoring",
            "word_against": "against",
            "word_and": "and",
            "word_played": "played",
            "word_wickets": "wickets",
            "word_chasing": "chasing"
        }

        self.most_x_expansions = {'word_a': 'a',
                                  'word_against': 'against',
                                  'word_captain': 'captain',
                                  'words_wicket_keeper': 'wicket keeper',
                                  'word_has': 'has',
                                  'word_in': 'in',
                                  'word_player': 'player',
                                  'word_the': 'the',
                                  'word_which': 'which',
                                  'word_who': 'who',
                                  'word_batting': 'batting',
                                  'word_year': 'year',
                                  'words_single_ground': 'single ground',
                                  'words_single_innings': 'single innings',
                                  'words_single_match': 'single match',
                                  'words_single_series': 'single series',
                                  'words_single_year': 'single year'}

        self.dynamic_expansions = {
            "clause_innings_score": [
                "word_scoring innings_score"
            ],
            "clause_wickets_left": [
                "word_with wickets word_wickets word_left"
            ],
            "clause_batting_order": [
                "word_batting word_batting_order"
            ],
            "clause_result_by_team": [
                "word_won_lost word_by team",
                "word_played word_by team",
                "word_played word_by team_A word_and team_B",
                "word_won_lost word_by team_A word_against team_B"
            ],
            "clause_chasing_score": [
                "word_chasing target"
            ]
        }

    def test_productions(self):
        expansions_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'expansions')
        productions = Productions().productions(expansions_path)

        self.assertEqual(8, len(productions))

        matches_productions = productions[1]['matches']
        most_x_productions = productions[3]['most_x']

        # Remove keys that get random words everytime (1st, 2nd etc). Should fix this, to get reproducible results.
        matches_productions['expansions'].pop('word_batting_order')
        matches_productions['expansions'].pop('word_won_lost')
        matches_productions['expansions'].pop('word_this_last')
        most_x_productions['expansions'].pop('word_this_last')
        most_x_productions['expansions'].pop('word_most')
        most_x_productions['expansions'].pop('word_wkt_order')

        # Unable to assert the actual list content. It permutation order changes every time. Not reproducible.
        self.assertEqual(len(matches_productions['syntax']), 11)
        self.assertEqual(matches_productions['expansions'], self.expansions)
        self.assertEqual(matches_productions['dynamic_expansions'], self.dynamic_expansions)

        self.assertEqual(most_x_productions['expansions'], self.most_x_expansions)

    def test_explode(self):
        expansions_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'expansions')
        exploded_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'exploded')

        Productions().explode(expansions_path, exploded_path)

        self.assertCountEqual(list(map(basename, glob.iglob(os.path.join(exploded_path, '*')))),
                         ['compare', 'matches', 'matches_cond', 'most_x', 'partnerships', 'player_dismissals',
                          'player_stats', 'scores'])


if __name__ == '__main__':
    unittest.main()

