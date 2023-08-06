"""

This file contains the API bridge that communicates with the Youless
device.

"""

import json
from urllib.request import urlopen
from youless_api.youless_sensor import YoulessSensor


class YoulessAPI:
    """A helper class to obtain data from the YouLess Sensor."""

    def __init__(self, host):
        """Initialize the data bridge."""
        self._url = 'http://' + host + '/'
        self._cache = None
        self._device = None

    def initialize(self):
        self._device = json.loads(urlopen(f"{self._url}d")
                                  .read()
                                  .decode('utf-8'))

    def update(self):
        """Fetch the latest settings from the Youless Sensor."""
        self._cache = json.loads(urlopen(f"{self._url}e")
                                 .read()
                                 .decode('utf-8'))[0]

    @property
    def mac_address(self):
        if self._device is not None:
            return self._device['mac']

        return None

    @property
    def model(self):
        if self._device is not None:
            return self._device['model']

        return None

    @property
    def gas_meter(self):
        """"Get the gas data available."""
        if self._cache is not None:
            return YoulessSensor(self._cache['gas'], 'm3')

        return None

    @property
    def current_power_usage(self):
        """Get the current power usage."""
        if self._cache is not None:
            return YoulessSensor(self._cache['pwr'], 'W')

        return None

    @property
    def power_meter(self):
        """Get the power meter values."""
        if self._cache is not None:
            return PowerMeter(
                YoulessSensor(self._cache['p1'], 'kWh'),
                YoulessSensor(self._cache['p2'], 'kWh'),
                YoulessSensor(self._cache['net'], 'kWh')
            )

        return None

    @property
    def delivery_meter(self):
        """Get the power delivered values."""
        if self._cache is not None:
            return DeliveryMeter(
                YoulessSensor(self._cache['n1'], 'kWh'),
                YoulessSensor(self._cache['n2'], 'kWh')
            )

        return None

    @property
    def extra_meter(self):
        """Get the meter values of an attached meter."""
        if self._cache is not None:
            return {
                'total': YoulessSensor(self._cache['cs0'], 'kWh'),
                'current': YoulessSensor(self._cache['ps0'], 'kWh')
            }

        return None


class DeliveryMeter:

    def __init__(self, low: YoulessSensor, high: YoulessSensor):
        self._low = low
        self._high = high

    @property
    def low(self):
        return self._low

    @property
    def high(self):
        return self._high


class PowerMeter:

    def __init__(self, low: YoulessSensor, high: YoulessSensor,
                 total: YoulessSensor):
        self._low = low
        self._high = high
        self._total = total

    @property
    def low(self):
        return self._low

    @property
    def high(self):
        return self._high

    @property
    def total(self):
        return self._total
