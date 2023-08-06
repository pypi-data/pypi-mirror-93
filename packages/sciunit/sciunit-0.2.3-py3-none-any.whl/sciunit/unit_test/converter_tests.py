"""Unit tests for score converters"""

import unittest


class ConvertersTestCase(unittest.TestCase):
    """Unit tests for Score converters"""

    def test_converters(self):
        from sciunit.converters import (
            AtLeastToBoolean,
            AtMostToBoolean,
            LambdaConversion,
            NoConversion,
            RangeToBoolean,
        )
        from sciunit.scores import BooleanScore, ZScore

        old_score = ZScore(1.3)
        new_score = NoConversion().convert(old_score)
        self.assertEqual(old_score, new_score)
        new_score = LambdaConversion(lambda x: x.score ** 2).convert(old_score)
        self.assertEqual(old_score.score ** 2, new_score.score)
        new_score = AtMostToBoolean(3).convert(old_score)
        self.assertEqual(new_score, BooleanScore(True))
        new_score = AtMostToBoolean(1).convert(old_score)
        self.assertEqual(new_score, BooleanScore(False))
        new_score = AtLeastToBoolean(1).convert(old_score)
        self.assertEqual(new_score, BooleanScore(True))
        new_score = AtLeastToBoolean(3).convert(old_score)
        self.assertEqual(new_score, BooleanScore(False))
        new_score = RangeToBoolean(1, 3).convert(old_score)
        self.assertEqual(new_score, BooleanScore(True))
        new_score = RangeToBoolean(3, 5).convert(old_score)
        self.assertEqual(new_score, BooleanScore(False))
        self.assertEqual(new_score.raw, str(old_score.score))

    def test_converters2(self):
        from sciunit import Score
        from sciunit.converters import Converter

        converterObj = Converter()

        self.assertIsInstance(converterObj.description, str)
        self.assertRaises(NotImplementedError, converterObj._convert, Score(0.5))

        class MyConverter(Converter):
            pass

        myConverterObj = MyConverter()
        self.assertEqual(myConverterObj.description, "No description available")


if __name__ == "__main__":
    unittest.main()
