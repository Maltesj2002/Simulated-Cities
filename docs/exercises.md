# Exercises

These exercises guide you through building pieces of the simulated city step by step.

## Exercise 1 — Simulate a man drinking beer

In this exercise you create a simple **agent**: a man who drinks a glass of beer.

The agent has two pieces of state:

- **`beer_ml`** — how much beer is left in the glass (millilitres).
- **`thirst`** — how thirsty the man is right now (0.0 = not thirsty, 1.0 = very thirsty).

Each simulation step is one of two outcomes:

- **Drink**: if thirst is at or above `drink_threshold` and beer remains, the man takes a sip — `beer_ml` decreases and thirst drops to zero (or proportionally for the last partial sip).
- **Get thirsty**: otherwise thirst increases by `thirst_rate`.

The simulation ends when the glass is empty (`is_done` is `True`).

### Import

```python
from simulated_city.agents import BeerDrinker
```

### Quick start

```python
man = BeerDrinker(name="Erik")

while not man.is_done:
    state = man.step()
    print(state)
```

### Customise the agent

```python
man = BeerDrinker(
    name="Erik",
    beer_ml=330.0,        # small can
    sip_ml=33.0,          # 10 sips to finish
    thirst_rate=0.2,      # gets thirsty quickly
    drink_threshold=0.6,  # waits until fairly thirsty
)
```

### Publish state over MQTT

```python
import json
from simulated_city.config import load_config
from simulated_city.mqtt import MqttConnector, MqttPublisher
from simulated_city.agents import BeerDrinker

cfg = load_config()
connector = MqttConnector(cfg.mqtt, client_id_suffix="beer-demo")
publisher = MqttPublisher(connector)
connector.connect()
connector.wait_for_connection()

man = BeerDrinker(name="Erik")
topic = "simulated-city/agents/beer-drinker"

while not man.is_done:
    state = man.step()
    publisher.publish_json(topic, json.dumps(state), qos=0)

connector.disconnect()
```

### What to explore next

- Add a **location** field and move the man between a bar and a park on each step.
- Add multiple agents and run them in the same loop.
- Subscribe to the MQTT topic in a second script and react to the published state.
