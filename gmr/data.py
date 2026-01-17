import copy

# Game Data

_default_drivers = [
    {"name": "Carlo Bianci", "constructor": "Enzoni", "skill": 7, "consistency": 6, "salary": 100, "signing_fee": 500},
    {"name": "Alberto Rossi", "constructor": "Enzoni", "skill": 7, "consistency": 7, "salary": 110, "signing_fee": 550},

    {"name": "Emmanuel Dubois", "constructor": "Independent", "skill": 5, "consistency": 5, "salary": 40, "signing_fee": 150},
    {"name": "George McCallister", "constructor": "Independent", "skill": 5, "consistency": 5, "salary": 40, "signing_fee": 150},
    {"name": "Hans Keller", "constructor": "Independent", "skill": 5, "consistency": 4, "salary": 35, "signing_fee": 120},
    {"name": "Luis Navarro", "constructor": "Independent", "skill": 4, "consistency": 6, "salary": 30, "signing_fee": 100},
    {"name": "Ivan Petrov", "constructor": "Independent", "skill": 4, "consistency": 5, "salary": 30, "signing_fee": 100},
    {"name": "Antonio Marquez", "constructor": "Independent", "skill": 5, "consistency": 3, "salary": 35, "signing_fee": 120},

    # Extra independents for driver market
    {"name": "Franco Moretti", "constructor": "Independent", "skill": 6, "consistency": 6, "salary": 60, "signing_fee": 250},
    {"name": "Peter Lang", "constructor": "Independent", "skill": 6, "consistency": 5, "salary": 55, "signing_fee": 220},
    {"name": "Jan Novak", "constructor": "Independent", "skill": 5, "consistency": 6, "salary": 45, "signing_fee": 180},
    {"name": "Mikel Herrera", "constructor": "Independent", "skill": 4, "consistency": 7, "salary": 35, "signing_fee": 140},
]

drivers = []

def reset_drivers():
    drivers.clear()
    drivers.extend(copy.deepcopy(_default_drivers))

reset_drivers()

constructors = {
    "Enzoni": {"speed": 7, "reliability": 6},
    "Independent": {"speed": 5, "reliability": 4},
}

race_calendar = {
    5: {"name": "Marblethorpe GP", "type": "Balanced"},
    9: {"name": "San Rico GP", "type": "Technical"},
    13: {"name": "Château-des-Prés GP", "type": "High Speed"},
    18: {"name": "Nordland GP", "type": "High Speed"},
    22: {"name": "Vallone GP", "type": "Technical"},
    26: {"name": "Britannia GP", "type": "Balanced"},
    30: {"name": "Rougemont GP", "type": "Balanced"},
    35: {"name": "Autodromo Nazionale", "type": "High Speed"},
    40: {"name": "Grand Prix of the Americas", "type": "Technical"},
    44: {"name": "Season Finale", "type": "Balanced"}
}

weather_options = ["Sunny", "Overcast", "Rain"]

random_events = [
    {
        "id": "sponsor_bonus",
        "title": "Local Sponsor Deal",
        "text": "A local bakery wants to put their sticker on your car.",
        "effect_type": "money",
        "value": 200,
        "probability": 0.1
    },
    {
        "id": "parts_found",
        "title": "Spare Parts Found",
        "text": "You found some usable spare parts in the back of the shed.",
        "effect_type": "money",
        "value": 50,
        "probability": 0.15
    },
    {
        "id": "minor_accident",
        "title": "Workshop Accident",
        "text": "A heavy tool fell on the chassis. Minor repairs needed.",
        "effect_type": "money",
        "value": -100,
        "probability": 0.05
    },
    {
        "id": "engine_tuning",
        "title": "Stroke of Genius",
        "text": "Your mechanic found a way to squeeze a bit more power out of the engine.",
        "effect_type": "car_speed",
        "value": 1,
        "probability": 0.02
    }
]

engines = [
    {
        "id": "dad_old",
        "name": "Harper Type-1",
        "supplier": "Inherited",
        "speed": 4,
        "reliability": 4,
        "acceleration": 3,
        "heat_tolerance": 3,
        "price": 0,
        "description": "A creaking pre-war single-carb straight-4."
    },
    {
        "id": "harper_improved",
        "name": "Harper Type-1B",
        "supplier": "Surplus Dealer",
        "speed": 5,
        "reliability": 5,
        "acceleration": 5,
        "heat_tolerance": 4,
        "price": 1500,
        "description": "Factory-refurbished upgrade. Tighter tolerances."
    },
    {
        "id": "enzoni_works",
        "name": "Enzoni 1500 V12",
        "supplier": "Enzoni",
        "speed": 7,
        "reliability": 6,
        "acceleration": 7,
        "heat_tolerance": 7,
        "price": 3500,
        "description": "Refined Italian thoroughbred V12. Benchmark for the era."
    },
]

chassis = [
    {
        "id": "dad_old_chassis",
        "name": "Modified Pre-War",
        "supplier": "Inherited",
        "durability": 4,
        "handling": 4,
        "price": 0,
        "description": "A rickety but familiar frame. Basic but functional."
    },
    {
        "id": "rebuilt_chassis",
        "name": "Standard Racing Frame",
        "supplier": "Local Fabricator",
        "durability": 6,
        "handling": 5,
        "price": 1000,
        "description": "A robust, general-purpose frame. Better than grandpa's."
    },
    {
        "id": "aero_chassis",
        "name": "Lightweight Aero",
        "supplier": "Speed-Tek",
        "durability": 5,
        "handling": 7,
        "price": 2500,
        "description": "Focus on agility and cornering. Less durable, but fast."
    },
]
