"""
Draft Sport Python
Fantasy Metric Enumeration
author: hugh@blinkybeach.com
"""
from typing import TypeVar, Type, Any, List
from enum import Enum

Self = TypeVar('Self', bound='FantasyMetric')


class FantasyMetric(Enum):

    KICKS_FROM_HAND = 'Kicks from hand'
    BAD_PASSES = 'Bad passes'
    CARRIES = 'Carries'
    CLEAN_BREAKS = 'Clean breaks'
    CONVERSION_GOALS = 'Conversion goals'
    DEFENDERS_BEATEN = 'Defenders beaten'
    DROP_GOALS_CONVERTED = 'Drop goals converted'
    LINEOUTS_WON_STEAL = 'Lineouts won (steal)'
    LINEOUTS_TO_OWN_PLAYER = 'Lineouts to own player'
    LINEOUTS_WON_AS_HOOKER = 'Lineouts won as hooker'
    METRES = 'Metres'
    MISSED_PENALTY_GOALS = 'Missed penalty goals'
    MISSED_TACKLES = 'Missed tackles'
    OFFLOADS = 'Offloads'
    PASSES = 'Passes'
    DEFENSIVE_PENALTIES = 'Defensive penalties'
    OFFENSIVE_PENALTIES = 'Offensive penalties'
    PENALTY_GOALS = 'Penalty goals'
    RED_CARDS = 'Red cards'
    TACKLES = 'Tackles'
    THROWS_LOST = 'Throws lost'
    TRIES = 'Tries'
    TRY_ASSISTS = 'Try assists'
    TURNOVERS_CONCEDED = 'Turnovers conceded'
    TURNOVERS_WON = 'Turnovers won'
    YELLOW_CARDS = 'Yellow cards'
    SCRUMS_WON = 'Scrums won'
    SCRUMS_LOST = 'Scrums lost'
    PLAYED_MORE_THAN_60_MIN = 'Played more than 60 min'
    TOOK_THE_FIELD = 'Took the field'
    UNKNOWN = 'Unknown'

    @classmethod
    def list_names(cls: Type[Self]) -> List[str]:
        return sorted([m.value for m in cls if m.value != 'Unknown'])

    @classmethod
    def decode(cls: Type[Self], data: Any) -> Self:

        try:
            result = FantasyMetric(data)
        except ValueError:
            return FantasyMetric.UNKNOWN

        return result

    @classmethod
    def with_key(cls: Type[Self], key: str) -> Self:
        return cls.decode(key)
