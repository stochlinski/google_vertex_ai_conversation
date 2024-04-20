from __future__ import annotations

import mimetypes
from pathlib import Path

import voluptuous as vol
from google.api_core.exceptions import ClientError
from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
)
from homeassistant.exceptions import (
    HomeAssistantError,
)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
from vertexai.generative_models import Part
from vertexai.preview.generative_models import GenerativeModel

from .const import (
    CONF_PROMPT,
    CONF_IMAGE_FILENAME,
    DOMAIN,
)

SERVICE_GENERATE_CONTENT = "generate_content"

async def async_setup_services(hass: HomeAssistant, config: ConfigType) -> None:
    """Set up services for the Google Vertex AI Conversation component."""

    async def generate_content(call: ServiceCall) -> ServiceResponse:
        """Generate content from text and optionally images."""
        prompt_parts = [call.data[CONF_PROMPT]]
        image_filenames = call.data[CONF_IMAGE_FILENAME]
        for image_filename in image_filenames:
            if not hass.config.is_allowed_path(image_filename):
                raise HomeAssistantError(
                    f"Cannot read `{image_filename}`, no access to path; "
                    "`allowlist_external_dirs` may need to be adjusted in "
                    "`configuration.yaml`"
                )
            if not Path(image_filename).exists():
                raise HomeAssistantError(f"`{image_filename}` does not exist")
            mime_type, _ = mimetypes.guess_type(image_filename)
            if mime_type is None or not mime_type.startswith("image"):
                raise HomeAssistantError(f"`{image_filename}` is not an image")
            prompt_parts.append(Part.from_data(mime_type=mime_type, data=await hass.async_add_executor_job(Path(image_filename).read_bytes)))

        model_name = "gemini-1.0-pro-vision" if image_filenames else "gemini-1.0-pro"
        model = GenerativeModel(model_name=model_name)

        try:
            response = await model.generate_content_async(prompt_parts)
        except (
            ClientError,
            ValueError,
            RuntimeError,
        ) as err:
            raise HomeAssistantError(f"Error generating content: {err}") from err

        return {"text": response.text}

    hass.services.async_register(
        DOMAIN,
        SERVICE_GENERATE_CONTENT,
        generate_content,
        schema=vol.Schema(
            {
                vol.Required(CONF_PROMPT): cv.string,
                vol.Optional(CONF_IMAGE_FILENAME, default=[]): vol.All(
                    cv.ensure_list, [cv.string]
                ),
            }
        ),
        supports_response=SupportsResponse.ONLY,
    )
