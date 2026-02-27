from simulated_city.agents import BeerDrinker


def test_initial_state() -> None:
    man = BeerDrinker(name="Erik")
    s = man.state()
    assert s["name"] == "Erik"
    assert s["beer_ml"] == 500.0
    assert s["thirst"] == 1.0
    assert s["is_done"] is False


def test_step_drinks_when_thirsty() -> None:
    # Starts with thirst=1.0 which is above the default drink_threshold=0.5
    man = BeerDrinker(name="Erik", beer_ml=500.0, thirst=1.0, sip_ml=50.0)
    s = man.step()
    assert s["beer_ml"] == 450.0
    assert s["thirst"] == 0.0  # full sip fully quenches thirst


def test_step_builds_thirst_when_not_thirsty() -> None:
    man = BeerDrinker(name="Erik", thirst=0.0, thirst_rate=0.1, drink_threshold=0.5)
    s = man.step()
    assert s["thirst"] == round(0.1, 4)
    assert s["beer_ml"] == 500.0  # no sip taken


def test_thirst_capped_at_one() -> None:
    man = BeerDrinker(name="Erik", thirst=0.95, thirst_rate=0.1, drink_threshold=2.0)
    s = man.step()
    assert s["thirst"] == 1.0


def test_is_done_when_glass_empty() -> None:
    man = BeerDrinker(name="Erik", beer_ml=50.0, thirst=1.0, sip_ml=50.0)
    s = man.step()
    assert s["beer_ml"] == 0.0
    assert s["is_done"] is True
    assert man.is_done is True


def test_partial_sip_when_less_than_sip_ml_remains() -> None:
    man = BeerDrinker(name="Erik", beer_ml=20.0, thirst=1.0, sip_ml=50.0)
    s = man.step()
    assert s["beer_ml"] == 0.0
    # partial sip: thirst reduced proportionally (20/50 = 0.4)
    assert s["thirst"] == round(1.0 - 20.0 / 50.0, 4)


def test_full_simulation_empties_glass() -> None:
    man = BeerDrinker(name="Erik", beer_ml=100.0, sip_ml=50.0, thirst_rate=0.5, drink_threshold=0.5)
    steps = 0
    while not man.is_done:
        man.step()
        steps += 1
        assert steps < 1000, "simulation did not terminate"
    assert man.beer_ml == 0.0
