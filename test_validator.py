import unittest

from validator import validate_record


class ValidatorTests(unittest.TestCase):
    def test_valid_record(self):
        record = {
            "product_code": "CRD-001",
            "quantity": "2",
            "price": "100",
            "status": "active",
        }

        self.assertEqual(validate_record(2, record), [])

    def test_invalid_record(self):
        record = {
            "product_code": "",
            "quantity": "-1",
            "price": "abc",
            "status": "wrong",
        }

        issues = validate_record(2, record)
        self.assertEqual(len(issues), 4)


if __name__ == "__main__":
    unittest.main()
