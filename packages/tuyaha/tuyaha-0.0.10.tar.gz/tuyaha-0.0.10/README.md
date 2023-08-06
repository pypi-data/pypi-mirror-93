# tuyaha

Cloned from the abandoned package [tuyapy](https://pypi.org/project/tuyapy/) v0.1.3. This package implements a Tuya
API endpoint that was specially designed for Home Assistant.

This clone contains several critical fixes. Check commits.

## FAQ
## How to check whether the API this library using can control your device?

- Copy [this script](https://github.com/PaulAnnekov/tuyaha/blob/master/tools/debug_discovery.py) to your PC with Python
  installed or to https://repl.it/
- Set/update config inside and run it
- Check if your devices are listed
  - If they are - open an issue and provide the output
  - If they are not - don't open an issue. Ask [Tuya support](mailto:support@tuya.com) to support your device in their 
    `/homeassistant` API
- Remove the updated script, so your credentials won't leak

## My device is not listed in Tuya API response or contains incomplete state, what should I do?

Write an email to tuyasmart@tuya.com and mention the `tuyapy` library and `https://px1.tuya{}.com` API endpoint. Usually they ignore incoming emails, but perhaps, if they get a lot of emails, they will start fixing the API.
