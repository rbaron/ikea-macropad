import argparse
import json
from urllib.parse import urlparse
import paho.mqtt.client as mqtt
from pynput.keyboard import Key, Controller


def on_connect(client, userdata, flags, rc):
    if rc != 0:
        print(f'Error connecting to the MQTT broker: {rc}')
        return
    client.subscribe(userdata['remote_topic'])


def on_subscribe(mqttc, userdata, mid, granted_qos):
    print(f'Successfully subscribed to {userdata["remote_topic"]}')


keys_by_ikea_event = {
    # Toggle audio.
    'brightness_up_click': [Key.cmd, Key.shift, 'a'],
    # Toggle video.
    'brightness_down_click': [Key.cmd, Key.shift, 'v'],
    # Volume up.
    'brightness_up_hold': [Key.media_volume_up],
    # Volume down.
    'brightness_down_hold': [Key.media_volume_down],
    # Leave meeting - "toggle" is the on/off button.
    'toggle': [Key.cmd, 'w'],
    # Enter.
    'arrow_right_click': [Key.enter],
    # Esc.
    'arrow_left_click': [Key.esc],
}


def execute_keys(keyboard, keys):
    for k in keys:
        keyboard.press(k)
    for k in reversed(keys):
        keyboard.release(k)


def on_message(client, userdata, msg):
    ikea_event = json.loads(msg.payload).get('action')
    if not ikea_event:
        return
    elif ikea_event not in keys_by_ikea_event:
        print(f'Unhandled event: {ikea_event}')
        return
    return execute_keys(userdata['keyboard'], keys_by_ikea_event[ikea_event])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mqtt-addr', type=str, required=True,
                        help="Address of your MQTT broker. E.g.: mqtt://myhost:1883")
    parser.add_argument('--remote-topic', type=str, required=True,
                        help="zigbee2mqtt MQTT topic of the ikea remote. E.g.: zigbee2mqtt/0x8471a5ffdecc3109")
    parser.add_argument('--username', type=str, help="MQTT username")
    parser.add_argument('--password', type=str, help="MQTT password")
    return parser.parse_args()


def main():
    args = parse_args()
    # userdata will be passed to MQTT callbacks.
    userdata = {
        'keyboard': Controller(),
        'remote_topic': args.remote_topic,
    }
    client = mqtt.Client(userdata=userdata)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    if args.username:
        client.username_pw_set(args.username, args.password)

    addr = urlparse(args.mqtt_addr)
    client.connect(addr.hostname, addr.port)

    client.loop_forever()


if __name__ == '__main__':
    main()
