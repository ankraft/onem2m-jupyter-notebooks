
import datetime, random
from typing import Generator



def randomTemperature() -> str:
    """ Create a random temperature between 10 and 30
    """
    return str(random.randint(10, 30))




HumidityGenerator = Generator[int, None, None]
_randomHumidity:HumidityGenerator = None

def randomHumidity() -> str:
    global _randomHumidity
    def _randomHumidityGenerator() -> HumidityGenerator:
        """ Create a random humidity between 30 and 80
        """
        low  = 30
        high = 80
        humidity = random.randint(low, high)
        while True:
            humidity += random.randint(-2, 2)
            humidity = low if humidity < low else humidity
            humidity = high if humidity > high else humidity
            yield humidity
    if _randomHumidity is None:
        _randomHumidity = _randomHumidityGenerator()
    return str(next(_randomHumidity))


def today() -> str:
    """	Return today's date in the ISO format YYYY-MM-DD.
    """
    return datetime.datetime.now().strftime('%Y-%m-%d')


def yesterday(days:int=1) -> str:
    """	Return yesterday's date in the ISO format YYYY-MM-DD.
    """
    return (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')