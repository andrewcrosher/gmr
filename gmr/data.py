# Game Data

drivers = [
    {"name": "Carlo Bianci", "constructor": "Enzoni", "skill": 7, "consistency": 6},
    {"name": "Alberto Rossi", "constructor": "Enzoni", "skill": 7, "consistency": 7},

    {"name": "Emmanuel Dubois", "constructor": "Independent", "skill": 5, "consistency": 5},
    {"name": "George McCallister", "constructor": "Independent", "skill": 5, "consistency": 5},
    {"name": "Hans Keller", "constructor": "Independent", "skill": 5, "consistency": 4},
    {"name": "Luis Navarro", "constructor": "Independent", "skill": 4, "consistency": 6},
    {"name": "Ivan Petrov", "constructor": "Independent", "skill": 4, "consistency": 5},
    {"name": "Antonio Marquez", "constructor": "Independent", "skill": 5, "consistency": 3},

    # Extra independents for driver market
    {"name": "Franco Moretti", "constructor": "Independent", "skill": 6, "consistency": 6},
    {"name": "Peter Lang", "constructor": "Independent", "skill": 6, "consistency": 5},
    {"name": "Jan Novak", "constructor": "Independent", "skill": 5, "consistency": 6},
    {"name": "Mikel Herrera", "constructor": "Independent", "skill": 4, "consistency": 7},
]

constructors = {
    "Enzoni": {"speed": 7, "reliability": 6},
    "Independent": {"speed": 5, "reliability": 4},
}

race_calendar = {
    5: "Marblethorpe GP",
    12: "Château-des-Prés GP",
    20: "Vallone GP",
    28: "Rougemont GP"
}

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
