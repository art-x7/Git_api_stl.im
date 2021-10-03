import unittest
from main import abort_if_keys_doenst_exist


class Test_api(unittest.TestCase):

    def test_list(self):
        data_test = [{"a": 11}, {"a": 22}]
        self.assertEqual(abort_if_keys_doenst_exist("a", data_test), True)

    def test_list_one(self):
        data_test = {"a": 11}
        self.assertEqual(abort_if_keys_doenst_exist("a", data_test), True)


if __name__ == "__main__":
  unittest.main()