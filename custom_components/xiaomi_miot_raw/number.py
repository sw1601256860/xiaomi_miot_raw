import asyncio
import logging
from functools import partial

from datetime import timedelta
import json
from collections import OrderedDict
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.number import PLATFORM_SCHEMA, NumberEntity
from homeassistant.const import *
from homeassistant.exceptions import PlatformNotReady
from miio.exceptions import DeviceException
from .deps.miio_new import MiotDevice

from . import GenericMiotDevice, MiotSubDevice, dev_info, async_generic_setup_platform
from .sensor import MiotSubSensor
from .deps.const import (
    DOMAIN,
    CONF_UPDATE_INSTANT,
    CONF_MAPPING,
    CONF_CONTROL_PARAMS,
    CONF_CLOUD,
    CONF_MODEL,
    ATTR_STATE_VALUE,
    ATTR_MODEL,
    ATTR_FIRMWARE_VERSION,
    ATTR_HARDWARE_VERSION,
    SCHEMA,
    MAP,
    DUMMY_IP,
    DUMMY_TOKEN,
)
import copy

TYPE = 'number'

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Generic MIoT " + TYPE
DATA_KEY = TYPE + '.' + DOMAIN
SCAN_INTERVAL = timedelta(seconds=10)
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    SCHEMA
)
# pylint: disable=unused-argument
@asyncio.coroutine
async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    hass.data[DOMAIN]['add_handler'].setdefault(TYPE, {})
    if 'config_entry' in config:
        id = f"{config.get(CONF_HOST)}-{config.get(CONF_NAME)}"
        hass.data[DOMAIN]['add_handler'][TYPE].setdefault(id, async_add_devices)

    await async_generic_setup_platform(
        hass,
        config,
        async_add_devices,
        discovery_info,
        TYPE,
        {'default': None},
        {'default': MiotNumberInput}
    )

async def async_setup_entry(hass, config_entry, async_add_entities):
    config = copy.copy(hass.data[DOMAIN]['configs'].get(config_entry.entry_id, dict(config_entry.data)))
    await async_setup_platform(hass, config, async_add_entities)

class MiotNumberInput(NumberEntity, MiotSubSensor):
    @property
    def value(self):
        try:
            return float(self.state)
        except Exception as ex:
            _LOGGER.error(ex)

    async def async_set_value(self, value):
        _LOGGER.warn(value)

    # @property
    # def min_value(self):
    #     """Return the minimum value."""

    # @property
    # def max_value(self):
    #     """Return the maximum value."""

    # @property
    # def step(self):
    #     """Return the increment/decrement step."""
