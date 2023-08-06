"""
Draft Sport Python
Point Score Module
author: hugh@blinkybeach.com
"""
from nozomi import Decodable, Immutable
from typing import TypeVar, Type, Any
from draft_sport.fantasy.scores.player.metrics import FantasyMetric

T = TypeVar('T', bound='Score')


class Score(Decodable):
    """An integer score with respect to some fantasy metric"""

    def __init__(
        self,
        fantasy_metric: FantasyMetric,
        score: int
    ) -> None:

        self._fantasy_metric = fantasy_metric
        self._score = score

        return

    value = Immutable(lambda s: s._score)
    fantasy_metric = Immutable(lambda s: s._fantasy_metric)
    fantasy_metric_name = Immutable(lambda s: s._fantasy_metric.value)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            fantasy_metric=FantasyMetric.decode(data['fantasy_metric_name']),
            score=data['score']
        )
