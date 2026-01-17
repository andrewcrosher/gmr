import pytest
from gmr.mechanics import calculate_driver_performance
from gmr.models import GameState
from gmr.data import constructors

def test_performance_calculation_basics():
    state = GameState()
    state.car_speed = 5
    state.car_handling = 5
    state.car_reliability = 10
    state.car_durability = 10
    
    driver = {"name": "Test Driver", "constructor": "Enzoni", "skill": 5, "consistency": 10} 
    state.player_driver = driver
    
    perf, finished, reason = calculate_driver_performance(driver, state, constructors)
    
    assert finished is True 
    assert perf > 0

def test_weather_impact_rain():
    state = GameState()
    state.car_speed = 10
    state.car_handling = 1
    # Rain favors handling. Low handling should hurt.
    state.car_reliability = 10
    state.car_durability = 10
    
    driver = {"name": "Test", "constructor": "Enzoni", "skill": 5, "consistency": 10}
    state.player_driver = driver
    
    perf_rain, _, _ = calculate_driver_performance(driver, state, constructors, weather="Rain")
    perf_sunny, _, _ = calculate_driver_performance(driver, state, constructors, weather="Sunny")
    
    assert perf_rain < perf_sunny

def test_track_type_impact():
    state = GameState()
    state.car_speed = 10
    state.car_handling = 2
    state.car_reliability = 10
    state.car_durability = 10
    
    driver = {"name": "Test", "constructor": "Enzoni", "skill": 5, "consistency": 10}
    state.player_driver = driver
    
    perf_fast, _, _ = calculate_driver_performance(driver, state, constructors, race_type="High Speed")
    perf_tech, _, _ = calculate_driver_performance(driver, state, constructors, race_type="Technical")
    
    assert perf_fast > perf_tech
