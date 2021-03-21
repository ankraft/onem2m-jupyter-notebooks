
import random


def randomTemperature() -> str:
    """ Create a random temperature between 10 and 30
    """
    return str(random.randint(10, 30))


def randomHumidity() -> str:
    """ Create a random humidity between 30 and 80
    """
    return str(random.randint(30, 80))