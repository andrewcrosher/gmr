import random
from .config import ERA_RELIABILITY_MULTIPLIER
from .data import random_events


def process_random_events(state):
    """Checks for and applies random events.

    Returns a list of event messages that occurred.
    """
    occurred_events = []

    # Shuffle events so we don't always check them in the same order
    events_shuffled = list(random_events)
    random.shuffle(events_shuffled)

    for event in events_shuffled:
        if random.random() < event["probability"]:
            # Apply effect
            if event["effect_type"] == "money":
                state.money += event["value"]

            elif event["effect_type"] == "car_speed":
                state.car_speed += event["value"]
                # Also update current engine stats if possible to persist
                if state.current_engine:
                    state.current_engine["speed"] += event["value"]

            msg = f"[bold]{event['title']}[/bold]: {event['text']}"
            if event["effect_type"] == "money":
                msg += (
                    f" ({'Gain' if event['value'] > 0 else 'Cost'}: £{abs(event['value'])})"
                )
            elif event["effect_type"] == "car_speed":
                msg += f" (Speed +{event['value']})"

            occurred_events.append(msg)

            # Limit to one event per week for now
            return occurred_events

    return occurred_events


def calculate_driver_performance(
    driver, state, constructors, weather="Sunny", race_type="Balanced"
):
    """Calculates the race performance for a driver.

    Returns a tuple (performance_score, did_finish, failure_reason)
    """
    # Weights based on conditions
    speed_weight = 1.0
    handling_weight = 0.5
    skill_weight = 1.0
    reliability_penalty = 0.0

    # Track Type Effects
    if race_type == "High Speed":
        speed_weight = 1.3
        handling_weight = 0.3
    elif race_type == "Technical":
        speed_weight = 0.7
        handling_weight = 0.8

    # Weather Effects
    if weather == "Rain":
        speed_weight *= 0.6
        handling_weight *= 1.5
        skill_weight = 1.3
        reliability_penalty = 0.05  # Flat 5% extra DNF chance
    elif weather == "Overcast":
        reliability_penalty = 0.01

    # Base driver performance with consistency variance
    consistency_factor = driver["consistency"] / 10
    variance = (
        random.uniform(-1, 1) * (1 - consistency_factor) * driver["skill"]
    )
    driver_score = (driver["skill"] + variance) * skill_weight

    # Decide where the car performance comes from
    if driver == state.player_driver:
        # Player's car
        car_speed = state.car_speed
        car_handling = state.car_handling
        car_reliability = state.car_reliability
        car_durability = state.car_durability
    else:
        # AI drivers - assume average chassis stats for now
        ctor_stats = constructors.get(driver["constructor"], {"speed": 5, "reliability": 5})
        car_speed = ctor_stats["speed"]
        car_handling = 5  # Base handling for AI
        car_reliability = ctor_stats["reliability"]
        car_durability = 5  # Base durability for AI

    # Performance formula: (Skill * W) + (Speed * W) + (Handling * W)
    car_score = (car_speed * speed_weight) + (car_handling * handling_weight)
    performance = driver_score + car_score

    # Reliability + DNF chance
    # Combined reliability factor (Engine Rel + Chassis Durability)
    total_reliability = (car_reliability + car_durability) / 2
    dnf_chance = (
        ((11 - total_reliability) * 0.02 * ERA_RELIABILITY_MULTIPLIER) + reliability_penalty
    )

    did_finish = True
    failure_reason = None

    if random.random() < dnf_chance:
        did_finish = False
        failure_reason = (
            "Engine Failure" if random.random() > 0.5 else "Mechanical Failure"
        )
        if weather == "Rain" and random.random() > 0.7:
            failure_reason = "Crash (Wet)"

    return performance, did_finish, failure_reason
