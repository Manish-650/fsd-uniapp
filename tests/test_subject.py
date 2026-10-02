import unittest
from unittest.mock import patch

from uniapp.models.subject import Subject


class SubjectTests(unittest.TestCase):
    def test_grade_boundaries(self):
        cases = [(25, "Z"), (49, "Z"), (50, "P"), (64, "P"),
                 (65, "C"), (74, "C"), (75, "D"), (84, "D"),
                 (85, "HD"), (100, "HD")]
        for mark, grade in cases:
            with self.subTest(mark=mark):
                self.assertEqual(Subject(7, mark).grade, grade)

    def test_saved_record_round_trip_does_not_use_random(self):
        record = {"id": "007", "mark": 85}
        with patch("uniapp.models.subject.random.choice") as choose:
            with patch("uniapp.models.subject.random.randint") as mark:
                subject = Subject.from_dict(record)
        choose.assert_not_called()
        mark.assert_not_called()
        self.assertEqual(subject.to_dict(), record)
        self.assertEqual(subject.grade, "HD")

    def test_creation_uses_only_remaining_id(self):
        used = {f"{number:03d}" for number in range(1, 999)}
        subject = Subject.create(used)
        self.assertEqual(subject.id, "999")
        self.assertTrue(25 <= subject.mark <= 100)

    def test_exhausted_ids_raise_error(self):
        with self.assertRaises(ValueError):
            Subject.create({f"{n:03d}" for n in range(1, 1000)})

    def test_invalid_values_are_rejected(self):
        for subject_id in [0, 1000, True, 1.5, "007"]:
            with self.subTest(subject_id=subject_id):
                with self.assertRaises(ValueError):
                    Subject(subject_id, 50)
        for mark in [24, 101, True, 50.5, "50"]:
            with self.subTest(mark=mark):
                with self.assertRaises(ValueError):
                    Subject(1, mark)

    def test_malformed_saved_ids_are_rejected(self):
        for value in ["7", "000", "abc", "１２３", 7]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    Subject.from_dict({"id": value, "mark": 50})


if __name__ == "__main__":
    unittest.main()
