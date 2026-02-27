"""Demo: simulate a man drinking beer.

This script runs a BeerDrinker agent for several steps and prints the state
at each step.  Optionally it publishes the state over MQTT.

Run:
    python scripts/demo/03_beer_drinker.py

If imports fail, install the library first:
    pip install -e "."
"""

from __future__ import annotations

import json

from simulated_city.agents import BeerDrinker
from simulated_city.config import load_config
from simulated_city.mqtt import MqttConnector, MqttPublisher


# Safety switch: publishing sends a real MQTT message.
# Keep this False unless you have a broker running.
ENABLE_PUBLISH = False

TOPIC = "simulated-city/agents/beer-drinker"


def main() -> None:
    man = BeerDrinker(name="Erik")

    print(f"Starting simulation for '{man.name}'")
    print(f"  glass: {man.beer_ml} ml | sip: {man.sip_ml} ml | thirst_rate: {man.thirst_rate}")
    print()

    publisher: MqttPublisher | None = None
    connector: MqttConnector | None = None

    if ENABLE_PUBLISH:
        cfg = load_config()
        connector = MqttConnector(cfg.mqtt, client_id_suffix="beer-demo")
        publisher = MqttPublisher(connector)
        connector.connect()
        connector.wait_for_connection()

    step = 0
    while not man.is_done:
        step += 1
        state = man.step()
        print(f"step {step:3d}: beer={state['beer_ml']:6.1f} ml  thirst={state['thirst']:.2f}")
        if publisher is not None:
            publisher.publish_json(TOPIC, json.dumps(state), qos=0)

    print()
    print(f"Glass empty after {step} steps.")

    if connector is not None and connector.client.is_connected():
        connector.disconnect()


if __name__ == "__main__":
    main()
