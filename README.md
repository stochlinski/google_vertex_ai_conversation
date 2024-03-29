# Google Vertex AI Conversation
This is custom component of Home Assistant.

Derived from [Google Generative AI Conversation] [[https://www.home-assistant.io/integrations/google_generative_ai_conversation/](https://github.com/home-assistant/core/tree/dev/homeassistant/components/google_generative_ai_conversation)]


This component use Google Vertex AI insted of Google Gemini API which is not available in Europe for now.

## Installation
1. Install via registering as a custom repository of HACS or by copying `google_vertex_ai_conversation` folder into `<config directory>/custom_components`
2. Restart Home Assistant
3. Go to Settings > Devices & Services.
4. In the bottom right corner, select the Add Integration button.
5. Follow the instructions on screen to complete the setup
   - Specify region (ex. us-central1)
   - Specify path to API key file to use with Google Cloud Platform. Here you can find some information how to get it: [How to obtain API Key File](https://www.home-assistant.io/integrations/google_cloud#obtaining-an-api-key)
7. Go to Settings > [Voice Assistants](https://my.home-assistant.io/redirect/voice_assistants/).
8. Click to edit Assistant (named "Home Assistant" by default).
9. Select "Google Vertext AI Conversation" from "Conversation agent" tab.

## Logging
In order to monitor logs of API requests and responses, add following config to `configuration.yaml` file

```yaml
logger:
  logs:
    custom_components.google_vertex_ai_conversation: info
```

## Support
If you want to support my work with a donation you can use one of the following platforms:

<table>
  <tr>
    <th>Platform</th>
    <th>Payment methods</th>
    <th>Link</th>
    <th>Comment</th>
  </tr>
  <tr>
    <td>PayPal</td>
    <td>
      <li>PayPal</li>
    </td>
    <td>
      <a href="https://paypal.me/Stochlinski" target="_blank"><img src="https://www.paypalobjects.com/webstatic/mktg/logo/pp_cc_mark_37x23.jpg" border="0" alt="PayPal Logo" height="35px" style="height: auto !important;width: auto !important;"></a>
    </td>
    <td>
      <li>No fees</li>
    </td>
  </tr>
</table>


[paypal_me_shield]: https://img.shields.io/static/v1.svg?label=%20&message=PayPal.Me&logo=paypal

[paypal_me]: https://paypal.me/Stochlinski

<!-- piotrmachowski_support_links_end -->