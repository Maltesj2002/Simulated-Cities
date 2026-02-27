"""simulated_city.agents — simulation agents for the workshop.

Each agent is a plain Python dataclass with a :meth:`step` method that
advances the simulation by one time unit and returns the current state as
a plain dictionary (ready to serialise to JSON / MQTT).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BeerDrinker:
    """An agent that simulates a man drinking a glass of beer.

    The man starts with a full glass and drinks a sip whenever his thirst
    reaches the ``drink_threshold``.  Thirst builds back up after each sip
    so the cycle repeats until the glass is empty.

    Attributes:
        name: Display name used in published messages.
        beer_ml: Beer remaining in the glass (millilitres).
        thirst: Current thirst level in the range [0.0, 1.0].
        sip_ml: Volume consumed per sip (ml).
        thirst_rate: Thirst increase per simulation step.
        drink_threshold: Thirst level at which the man takes a sip.
    """

    name: str
    beer_ml: float = 500.0
    thirst: float = 1.0
    sip_ml: float = 50.0
    thirst_rate: float = 0.1
    drink_threshold: float = 0.5

    @property
    def is_done(self) -> bool:
        """True when the glass is empty."""
        return self.beer_ml <= 0.0

    def step(self) -> dict:
        """Advance the simulation by one time step.

        If thirsty enough and beer remains, the man takes a sip and his
        thirst resets to zero.  Otherwise thirst increases by *thirst_rate*.

        Returns:
            The current state as a dictionary (suitable for JSON / MQTT).
        """
        if self.thirst >= self.drink_threshold and self.beer_ml > 0.0:
            sip = min(self.sip_ml, self.beer_ml)
            self.beer_ml = round(self.beer_ml - sip, 6)
            # A full sip fully quenches thirst; a partial sip quenches proportionally.
            self.thirst = max(0.0, self.thirst - sip / self.sip_ml)
        else:
            self.thirst = min(1.0, self.thirst + self.thirst_rate)
        return self.state()

    def state(self) -> dict:
        """Return the current state as a plain dictionary."""
        return {
            "name": self.name,
            "beer_ml": round(self.beer_ml, 2),
            "thirst": round(self.thirst, 4),
            "is_done": self.is_done,
        }
