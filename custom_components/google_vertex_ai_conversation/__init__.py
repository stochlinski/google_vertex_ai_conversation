"""The Google Generative AI Conversation integration."""
from __future__ import annotations

import logging

import vertexai
from google.api_core.exceptions import ClientError
from google.auth import load_credentials_from_file
from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LOCATION
from homeassistant.core import (
    HomeAssistant,
)
from homeassistant.exceptions import (
    ConfigEntryNotReady,
)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_CREDENTIALS,
    DOMAIN,
)
from .conversation_agent import GoogleVertexAIAgent

from .services import async_setup_services

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Google Vertex AI Conversation."""

    await async_setup_services(hass, config)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Google Vertex AI Conversation from a config entry."""

    credentials, project_id = load_credentials_from_file(filename=entry.data[CONF_CREDENTIALS]);

    try:
        vertexai.init(project=project_id, location=entry.data[CONF_LOCATION], credentials=credentials)
    except ClientError as err:
        if err.reason == "API_KEY_INVALID":
            _LOGGER.error("Invalid API key: %s", err)
            return False
        raise ConfigEntryNotReady(err) from err

    conversation.async_set_agent(hass, entry, GoogleVertexAIAgent(hass, entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload GoogleVertexAI."""
    vertexai.init(project=None, location=None, credentials=None)
    conversation.async_unset_agent(hass, entry)
    return True
