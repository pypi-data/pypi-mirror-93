"""Score types for tests that did not complete successfully.

These include details about the various possible reasons
that a particular combination of model and test could not be completed.
"""

from sciunit.errors import InvalidScoreError

from .base import Score


class NoneScore(Score):
    """A `None` score.

    Usually indicates that the model has not been
    checked to see if it has the capabilities required by the test."""

    def __init__(self, score: Score, related_data: dict = None):
        if isinstance(score, str) or score is None:
            super(NoneScore, self).__init__(score, related_data=related_data)
        else:
            raise InvalidScoreError("Score must be a string or None")

    @property
    def norm_score(self) -> None:
        """Return None as the norm score of this NoneScore instance.

        Returns:
            None: The norm score, which is None.
        """
        return None

    def __str__(self) -> str:
        if self.score:
            s = "%s (%s)" % (self.description, self.score)
        else:
            s = self.description
        return s


class TBDScore(NoneScore):
    """A TBD (to be determined) score. Indicates that the model has
    capabilities required by the test but has not yet taken it."""

    description = "None"


class NAScore(NoneScore):
    """A N/A (not applicable) score.

    Indicates that the model doesn't have the
    capabilities that the test requires."""

    description = "N/A"


class InsufficientDataScore(NoneScore):
    """A score returned when the model or test data
    is insufficient to score the test."""

    description = "Insufficient Data"
