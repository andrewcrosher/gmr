import random
from .config import ERA_RELIABILITY_MULTIPLIER

def calculate_driver_performance(driver, state, constructors):
    """
    Calculates the race performance for a driver.
    Returns a tuple (performance_score, did_finish, failure_reason)
    """
    # Base driver performance with consistency variance
    consistency_factor = driver["consistency"] / 10
    variance = random.uniform(-1, 1) * (1 - consistency_factor) * driver["skill"]
    performance = driver["skill"] + variance

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
        car_durability = 5 # Base durability for AI

    # Performance formula: Skill + Speed + Handling
    performance += car_speed + (car_handling * 0.5)

    # Reliability + DNF chance
    # Combined reliability factor (Engine Rel + Chassis Durability)
    total_reliability = (car_reliability + car_durability) / 2
    dnf_chance = (11 - total_reliability) * 0.02 * ERA_RELIABILITY_MULTIPLIER

    did_finish = True
    failure_reason = None

    if random.random() < dnf_chance:
        did_finish = False
        failure_reason = "Engine Failure" if random.random() > 0.5 else "Mechanical Failure"

    return performance, did_finish, failure_reason
