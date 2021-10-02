[IKEA TRÅDFRI remote control](https://www.ikea.com/gb/en/p/tradfri-remote-control-30443124/) as a macropad.

Here's a sample video with Zoom commands:

https://user-images.githubusercontent.com/1573409/135712027-4ca00df0-36a5-497e-831b-1b38749b0184.mp4

In the video, the remote buttons are mapped to the following commands:
- Brightness up click: mute/unmute
- Brightness down click: webcam on/off
- Brightness up long press: volume up
- Brightness down long press: volume down
- On/off click: leave meeting
- Left arrow click: ESC (used to cancel actions)
- Right arrow click: Enter (used to confirm actions)

# How does it work?
1. The IKEA TRÅDFRI remote control uses the [Zigbee](https://en.wikipedia.org/wiki/Zigbee) protocol to communicate its keypresses wirelessly
2. A [Zigbee adapter](https://www.zigbee2mqtt.io/information/supported_adapters.html) receives those keypresses
3. [zigbee2mqtt](https://www.zigbee2mqtt.io/) talks to the adapter and publishes received keypressed to an [MQTT broker](https://en.wikipedia.org/wiki/MQTT)
4. The script [ikea-macropad.py](./ikea-macropad.py) connects to the MQTT broker and listens to zibee2mqtt messages. It then translates those received messages into simulated keypresses
