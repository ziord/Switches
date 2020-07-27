"""
:copyright: Copyright (c) 2020 Jeremiah Ikosin (@ziord)
:license: MIT, see LICENSE for more details
"""

import unittest
from tests.funcs import *


class TestSwitches(unittest.TestCase):
    # fallthrough,
    # no fallthrough
    def test_ft_switch_case(self):
        self.assertListEqual(test_valNum_ft(), ['pop', 'push'])
        self.assertListEqual(test_valList_ft(), [])
        self.assertListEqual(test_valFoo_ft(), ['poof', 'poof2'])

    def test_ft_switch_case_break(self):
        self.assertListEqual(test_valNum2_ft(), ['pop'])
        self.assertListEqual(test_valList2_ft(), ['pop'])
        self.assertListEqual(test_valFoo2_ft(), ['poof', 'poof2'])

    def test_ft_switch_icase(self):
        self.assertListEqual(test_valNum3_ft(), ['push'])
        self.assertListEqual(test_valFoo3_ft(Foo('foo')), ['poof'])
        self.assertListEqual(test_valFoo3_ft(5), ['poof'])
        self.assertListEqual(test_valFoo3_ft(12), ['poof'])

    def test_ft_switch_fcase(self):
        self.assertListEqual(test_valNum4_ft(), ['push'])
        self.assertListEqual(test_valNum5_ft(), [])

    def test_ft_callable_value(self):
        self.assertTupleEqual(test_call_ft(), ((2, 3), {}))
        self.assertListEqual(test_valCall_ft(), ['pop', 'push'])
        self.assertListEqual(test_valCall2_ft(), ['push'])

    def test_ft_switch_default(self):
        self.assertListEqual(test_new_ft(), ['defaulted'])

    def test_nft_switch_case(self):
        self.assertListEqual(test_valNum_nft(), ['pop'])
        self.assertListEqual(test_valList_nft(), [])
        self.assertListEqual(test_valFoo_nft(), ['poof'])

    def test_nft_switch_case_break(self):
        self.assertListEqual(test_valNum2_nft(), ['pop', 'push'])
        self.assertListEqual(test_valList2_nft(), ['pop'])
        self.assertListEqual(test_valFoo2_nft(), ['poof', 'poof2'])

    def test_nft_switch_icase(self):
        self.assertListEqual(test_valNum3_nft(), ['push'])
        self.assertListEqual(test_valFoo3_nft(Foo('foo')), ['poof'])
        self.assertListEqual(test_valFoo3_nft(5), [])
        self.assertListEqual(test_valFoo3_nft(12), [])

    def test_nft_switch_fcase(self):
        self.assertListEqual(test_valNum4_nft(), ['push'])
        self.assertListEqual(test_valNum5_nft(), ['foofoo'])

    def test_nft_callable_value(self):
        self.assertTupleEqual(test_call_nft(), ((2, 3), {}))
        self.assertListEqual(test_valCall_nft(), ['pop'])
        self.assertListEqual(test_valCall2_nft(), [])

    def test_nft_switch_default(self):
        self.assertListEqual(test_new_nft(), ['defaulted'])

    def test_warns(self):
        self.assertWarns(UserWarning, test_valNum_wn, )
        self.assertWarns(UserWarning, test_valTup_wn, )

    def test_dup_error(self):
        with self.assertRaises(SwitchError):
            test_dup_err()

    def test_c_break_error(self):
        with self.assertRaises(SwitchError):
            test_double_cbreak_err()

    def test_case_after_default_error(self):
        with self.assertRaises(SwitchError):
            test_case_after_default_err()

    def test_double_cbreak2_error(self):
        with self.assertRaises(SwitchError):
            test_double_cbreak2_err()

    def test_call_error(self):
        with self.assertRaises(SwitchError):
            test_call_err()

    def test_iter_error(self):
        with self.assertRaises(SwitchError):
            test_iter_err()

    def test_value_args_error(self):
        with self.assertRaises(SwitchError):
            test_value_args_err()

    def test_value_kwargs_error(self):
        with self.assertRaises(SwitchError):
            test_value_kwargs_err()

    def test_fcase_f_args_error(self):
        with self.assertRaises(SwitchError):
            test_fcase_f_args_err()

    def test_fcase_f_kwargs_error(self):
        with self.assertRaises(SwitchError):
            test_fcase_f_kwargs_err()

    def test_case_args_error(self):
        with self.assertRaises(SwitchError):
            test_case_args_err()

    def test_case_kwargs_error(self):
        with self.assertRaises(SwitchError):
            test_case_kwargs_err()

    def test_icase_args_error(self):
        with self.assertRaises(SwitchError):
            test_case_args_err()

    def test_icase_kwargs_error(self):
        with self.assertRaises(SwitchError):
            test_icase_kwargs_err()


if __name__ == '__main__':
    unittest.main()
