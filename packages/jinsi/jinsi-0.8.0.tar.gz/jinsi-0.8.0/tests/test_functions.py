import unittest

from jinsi.functions import Functions


class FunctionsTest(unittest.TestCase):
    def test_concat_list(self):
        self.assertEqual([1, 2, 3], Functions.concat([1, 2], [3]))

    def test_concat_string(self):
        self.assertEqual("123", Functions.concat("12", "3"))

    def test_drop_right_list(self):
        self.assertEqual([1, 2], Functions.drop_right(2, [1, 2, 3, 4]))

    def test_drop_list(self):
        self.assertEqual([3, 4], Functions.drop(2, [1, 2, 3, 4]))

    def test_drop_right_string(self):
        self.assertEqual("ab", Functions.drop_right(2, "abcd"))

    def test_drop_string(self):
        self.assertEqual("cd", Functions.drop(2, "abcd"))

    def test_take_right_list(self):
        self.assertEqual([3, 4], Functions.take_right(2, [1, 2, 3, 4]))

    def test_take_list(self):
        self.assertEqual([1, 2], Functions.take(2, [1, 2, 3, 4]))

    def test_take_right_string(self):
        self.assertEqual("cd", Functions.take_right(2, "abcd"))

    def test_take_string(self):
        self.assertEqual("ab", Functions.take(2, "abcd"))

    def test_replace(self):
        self.assertEqual("foo qux bar foo qux", Functions.str_replace("foo", "foo qux", "foo bar foo"))


if __name__ == '__main__':
    unittest.main()
