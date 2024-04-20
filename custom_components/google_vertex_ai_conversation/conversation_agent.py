from __future__ import annotations

import logging
from typing import Literal

from google.api_core.exceptions import ClientError
from homeassistant.components import conversation
from homeassistant.components.homeassistant.exposed_entities import async_should_expose
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MATCH_ALL
from homeassistant.core import (
    HomeAssistant,
)
from homeassistant.exceptions import (
    TemplateError,
)
from homeassistant.helpers import intent, template, entity_registry as er
from homeassistant.util import ulid
from vertexai.generative_models import Content, Part
from vertexai.preview.generative_models import GenerativeModel

from .const import (
    CONF_CHAT_MODEL,
    CONF_MAX_TOKENS,
    CONF_PROMPT,
    CONF_TEMPERATURE,
    CONF_TOP_K,
    CONF_TOP_P,
    DEFAULT_CHAT_MODEL,
    DEFAULT_MAX_TOKENS,
    DEFAULT_PROMPT,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_K,
    DEFAULT_TOP_P,
)

_LOGGER = logging.getLogger(__name__)

class GoogleVertexAIAgent(conversation.AbstractConversationAgent):
    """Google Vertex AI conversation agent."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the agent."""
        self.hass = hass
        self.entry = entry
        self.history: dict[str, list[Content]] = {}

    @property
    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return a list of supported languages."""
        return MATCH_ALL

    async def async_process(
        self, user_input: conversation.ConversationInput
    ) -> conversation.ConversationResult:
        """Process a sentence."""
        model_name = self.entry.options.get(CONF_CHAT_MODEL, DEFAULT_CHAT_MODEL)
        _LOGGER.debug("Model: %s", model_name)

        model = GenerativeModel(
            model_name=model_name,
            generation_config={
                "temperature": self.entry.options.get(
                    CONF_TEMPERATURE, DEFAULT_TEMPERATURE
                ),
                "top_p": self.entry.options.get(CONF_TOP_P, DEFAULT_TOP_P),
                "top_k": self.entry.options.get(CONF_TOP_K, DEFAULT_TOP_K),
                "max_output_tokens": self.entry.options.get(
                    CONF_MAX_TOKENS, DEFAULT_MAX_TOKENS
                ),
            },
        )
        exposed_entities = self.get_exposed_entities()

        if user_input.conversation_id in self.history:
            conversation_id = user_input.conversation_id
            messages = self.history[conversation_id]
        else:
            conversation_id = ulid.ulid_now()
            messages = [{}, {}]

        try:
            system_prompt = self._async_generate_prompt(exposed_entities, user_input)
        except TemplateError as err:
            _LOGGER.error("Error rendering prompt: %s", err)
            intent_response = intent.IntentResponse(language=user_input.language)
            intent_response.async_set_error(
                intent.IntentResponseErrorCode.UNKNOWN,
                f"Sorry, I had a problem with my template: {err}",
            )
            return conversation.ConversationResult(
                response=intent_response, conversation_id=conversation_id
            )

        messages[0] = Content(role="user", parts=[Part.from_text(system_prompt)])
        messages[1] = Content(role="model", parts=[Part.from_text("Ok")])

        _LOGGER.debug("Input: '%s' with history: %s", user_input.text, messages)

        chat = model.start_chat(history=messages)
        try:
            chat_response = await chat.send_message_async(user_input.text)
        except (
            ClientError,
            ValueError,
            RuntimeError,
        ) as err:
            _LOGGER.error("Error sending message: %s", err)
            intent_response = intent.IntentResponse(language=user_input.language)
            intent_response.async_set_error(
                intent.IntentResponseErrorCode.UNKNOWN,
                f"Sorry, I had a problem talking to Google Generative AI: {err}",
            )
            return conversation.ConversationResult(
                response=intent_response, conversation_id=conversation_id
            )

        _LOGGER.debug("Response: %s", chat_response.text)
        self.history[conversation_id] = chat.history

        intent_response = intent.IntentResponse(language=user_input.language)
        intent_response.async_set_speech(chat_response.text)
        return conversation.ConversationResult(
            response=intent_response, conversation_id=conversation_id
        )

    def _async_generate_prompt(self, exposed_entities, user_input: conversation.ConversationInput) -> str:
        """Generate a system message for the user containing entities states."""

        raw_prompt = self.entry.options.get(CONF_PROMPT, DEFAULT_PROMPT)
        return template.Template(raw_prompt, self.hass).async_render(
            {
                "ha_name": self.hass.config.location_name,
                "exposed_entities": exposed_entities,
                "current_device_id": user_input.device_id,
            },
            parse_result=False,
        )

    def get_exposed_entities(self):
        states = [
            state
            for state in self.hass.states.async_all()
            if async_should_expose(self.hass, conversation.DOMAIN, state.entity_id)
        ]
        entity_registry = er.async_get(self.hass)
        exposed_entities = []
        for state in states:
            entity_id = state.entity_id
            entity = entity_registry.async_get(entity_id)

            aliases = []
            if entity and entity.aliases:
                aliases = entity.aliases

            exposed_entities.append(
                {
                    "entity_id": entity_id,
                    "name": state.name,
                    "state": self.hass.states.get(entity_id).state,
                    "aliases": aliases,
                }
            )
        return exposed_entities