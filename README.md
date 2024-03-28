# Google Vertex AI Conversation
This is custom component of Home Assistant.

Derived from [Google Generative AI Conversation]([[https://www.home-assistant.io/integrations/openai_conversation/](https://github.com/home-assistant/core/tree/dev/homeassistant/components/google_generative_ai_conversation)](https://github.com/home-assistant/core/tree/dev/homeassistant/components/google_generative_ai_conversation)).

This component use Google Vertex AI insted of Google Gemini which is not available in Europe for now.

## Installation
1. Install via registering as a custom repository of HACS or by copying `google_vertex_ai_conversation` folder into `<config directory>/custom_components`
2. Restart Home Assistant
3. Go to Settings > Devices & Services.
4. In the bottom right corner, select the Add Integration button.
5. Follow the instructions on screen to complete the setup 
6. Go to Settings > [Voice Assistants](https://my.home-assistant.io/redirect/voice_assistants/).
7. Click to edit Assistant (named "Home Assistant" by default).
8. Select "Google Vertext AI Conversation" from "Conversation agent" tab.

## Logging
In order to monitor logs of API requests and responses, add following config to `configuration.yaml` file

```yaml
logger:
  logs:
    custom_components.google_vertext_ai_conversation: info
```
