from enum import Enum


class MoodChoices(Enum):
    ANGRY = "angry"
    HAPPY = "happy"
    NEUTRAL = "neutral"
    SAD = "sad"
    SURPRISE = "surprise"
    CALM = "calm"

    @classmethod
    def choices(cls):
        return [(mood.value, mood.name.title()) for mood in cls]
