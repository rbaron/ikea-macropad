[IKEA TRÅDFRI remote control](https://www.ikea.com/gb/en/p/tradfri-remote-control-30443124/) as a macropad.

# How does it work?
1. The IKEA TRÅDFRI remote control uses the [Zigbee](https://en.wikipedia.org/wiki/Zigbee) protocol for communicating its keypresses wirelessly
2. A [Zigbee adapter](https://www.zigbee2mqtt.io/information/supported_adapters.html) receives those keypresses
3. [zigbee2mqtt](https://www.zigbee2mqtt.io/) talks to the adapter and publishes messages to an [MQTT broker](https://en.wikipedia.org/wiki/MQTT)
4. The script [ikea-macropad.py](./ikea-macropad.py) connects to the MQTT broker and listens to zibee2mqtt messages. It then translates those messages into simulated keypresses
