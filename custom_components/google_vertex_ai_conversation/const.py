"""Constants for the Google Vertex AI Conversation integration."""

DOMAIN = "google_vertex_ai_conversation"
CONF_PROMPT = "prompt"
CONF_IMAGE_FILENAME = "image_filename"
DEFAULT_PROMPT = """I want you to act as smart home manager of Home Assistant.
I will provide information of smart home along with a question, you will truthfully make correction or answer using information provided in one sentence in everyday language.

Current Time: {{now()}}

Available Devices:
```csv
entity_id,name,state,aliases
{% for entity in exposed_entities -%}
{{ entity.entity_id }},{{ entity.name }},{{ entity.state }},{{entity.aliases | join('/')}}
{% endfor -%}
```

The current state of devices is provided in available devices.
"""
CONF_CHAT_MODEL = "model"
DEFAULT_CHAT_MODEL = "gemini-1.0-pro"
CONF_TEMPERATURE = "temperature"
DEFAULT_TEMPERATURE = 0.9
CONF_TOP_P = "top_p"
DEFAULT_TOP_P = 1.0
CONF_TOP_K = "top_k"
DEFAULT_TOP_K = 1
CONF_MAX_TOKENS = "max_tokens"
DEFAULT_MAX_TOKENS = 150
CONF_CREDENTIALS = "credentials"
DEFAULT_CREDENTIALS = "/config/googlecloud.json"
DEFAULT_LOCATION = "us-central1"
