import pytest
from gmr.models import GameState, GarageState, GameTime

def test_gametime_serialization():
    gt = GameTime(1950)
    gt.month = 5
    gt.week = 2
    
    data = gt.to_dict()
    assert data["year"] == 1950
    assert data["month"] == 5
    
    gt2 = GameTime.from_dict(data)
    assert gt2.year == 1950
    assert gt2.week_of_year == gt.week_of_year

def test_gamestate_serialization():
    gs = GameState()
    gs.money = 12345
    gs.garage.level = 2
    gs.history.append({"year": 1948, "winner": "Me"})
    gs.completed_races.add("1948-5")
    
    data = gs.to_dict()
    assert data["money"] == 12345
    assert data["garage"]["level"] == 2
    assert "1948-5" in data["completed_races"]
    
    gs2 = GameState.from_dict(data)
    assert gs2.money == 12345
    assert gs2.garage.level == 2
    assert gs2.history[0]["winner"] == "Me"
    assert "1948-5" in gs2.completed_races
