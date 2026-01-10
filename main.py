# ------------------------------
# GMR Bootloader - Stable Build
# ------------------------------

import random

MONTHS = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

POINTS_TABLE = [8, 6, 4, 3, 2, 1]
PRIZE_MONEY = [300, 200, 100]
CONSTRUCTOR_SHARE = 0.3
WEEKLY_RUNNING_COST = 80
ERA_RELIABILITY_MULTIPLIER = 2.5


# ------------------------------
# TIME SYSTEM
# ------------------------------
class GameTime:
    def __init__(self, year=1947):
        self.year = year
        self.month = 0
        self.week = 1
        self.absolute_week = 1

    def advance_week(self):
        self.week += 1
        self.absolute_week += 1
        if self.week > 4:
            self.week = 1
            self.month += 1
            if self.month > 11:
                self.month = 0
                self.year += 1


# ------------------------------
# GARAGE STATE
# ------------------------------
class GarageState:
    def __init__(self):
        self.level = 0  # 0 = home shed
        self.base_cost = 80  # weekly running cost
        self.staff_count = 1  # number of people in the garage
        self.staff_salary = 20  # cost per staff member per week

        # Flags for future mechanics
        self.customer_parts_only = True
        self.r_and_d_enabled = False
        self.factory_team = False


# ------------------------------
# DATA
# ------------------------------
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


# ------------------------------
# ENGINES
# ------------------------------
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
        "description": "A creaking pre-war single-carb straight-4. Reliable enough to run, but outclassed already."
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
        "description": "A factory-refurbished upgrade. Same bones as the Type-1, but tighter tolerances and better power delivery."
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
        "description": "A refined Italian thoroughbred V12. Smooth, powerful, and surprisingly cool-running — the benchmark for late-40s racing."
    },
]



# ------------------------------
# GAME STATE
# ------------------------------
class GameState:
    def __init__(self):
        self.money = 5000
        self.points = {}
        self.player_constructor = None
        self.player_driver = None
        self.car_speed = 0
        self.car_reliability = 0
        self.constructor_earnings = 0
        self.last_week_income = 0
        self.last_week_outgoings = 0
        self.last_week_purchases = 0
        self.news = []
        self.garage = GarageState()

        # Car / engine
        self.current_engine = None

        # Track which absolute weeks have already had a race run
        self.completed_races = set()

    def reset_championship(self):
        self.points = {d["name"]: 0 for d in drivers}


# ------------------------------
# PLAYER SETUP
# ------------------------------
def setup_player(state):
    print("\nYour father passed away, leaving you his old racing chassis and a worn Level 1 engine.")
    print("You inherit a small shed for a garage and a single mechanic.")
    print("This is the start of your racing adventure.\n")

    # Ask player for constructor/company name
    state.player_constructor = input("Enter the name of your racing company: ")

    # Garage starting state
    state.garage.level = 0  # home shed
    state.garage.base_cost = 80
    state.garage.staff_count = 1
    state.garage.staff_salary = 20

    # Starting engine: inherited old unit
    starting_engine = next(e for e in engines if e["id"] == "dad_old")
    state.current_engine = starting_engine
    state.car_speed = starting_engine["speed"]
    state.car_reliability = starting_engine["reliability"]

    # Player driver is None for now
    state.player_driver = None

    print(f"\nWelcome to {state.player_constructor}! Your journey begins...\n")


# ------------------------------
# RACE LOGIC (FIXED)
# ------------------------------
def run_race(state, race_name, time):
    state.news.append(f"=== {race_name} ===")
    state.last_week_income = 0

    finishers = []

    for d in drivers:
        # Base driver performance with consistency variance
        consistency_factor = d["consistency"] / 10
        variance = random.uniform(-1, 1) * (1 - consistency_factor) * d["skill"]
        performance = d["skill"] + variance

        # Decide where the car performance comes from
        if d == state.player_driver:
            # Player's car: use your actual car stats (engine etc.)
            car_speed = state.car_speed
            car_reliability = state.car_reliability
        else:
            # AI drivers: use their constructor stats from the table
            ctor_stats = constructors.get(d["constructor"], {"speed": 5, "reliability": 5})
            car_speed = ctor_stats["speed"]
            car_reliability = ctor_stats["reliability"]

        performance += car_speed

        # Reliability + DNF chance
        reliability = car_reliability
        dnf_chance = (11 - reliability) * 0.02 * ERA_RELIABILITY_MULTIPLIER

        if random.random() < dnf_chance:
            state.news.append(
                f"{d['name']} ({d['constructor']}) retired due to reliability issues."
            )
            continue

        finishers.append((d, performance))

    # Sort by performance
    finishers.sort(key=lambda x: x[1], reverse=True)

    # Points & prize money ONLY for classified finishers
    for pos, (d, _) in enumerate(finishers):
        if pos < len(POINTS_TABLE):
            state.points[d["name"]] += POINTS_TABLE[pos]

        if d == state.player_driver and pos < len(PRIZE_MONEY):
            prize = int(PRIZE_MONEY[pos] * CONSTRUCTOR_SHARE)
            state.money += prize
            state.constructor_earnings += prize
            state.last_week_income += prize

    # Race classification (Top 10)
    for i, (d, _) in enumerate(finishers[:10]):
        state.news.append(f"{i+1}. {d['name']} ({d['constructor']})")

    # Championship standings (Top 10)
    sorted_points = sorted(state.points.items(), key=lambda x: x[1], reverse=True)
    state.news.append("Championship Standings (Top 10):")
    for name, pts in sorted_points[:10]:
        driver = next(d for d in drivers if d["name"] == name)
        state.news.append(f"{name} ({driver['constructor']}): {pts} pts")

    # End of season
    if time.absolute_week == max(race_calendar.keys()):
        winner = max(state.points, key=state.points.get)
        state.news.append(f"*** {winner} wins the {time.year} Championship! ***")
        state.reset_championship()



# ------------------------------
# UI
# ------------------------------
def show_finances(state):
    garage = state.garage
    staff_cost = garage.staff_count * garage.staff_salary
    print("\n=== Finances ===")
    print("Weekly Outgoings:")
    print(f"  Base garage cost: £{garage.base_cost}")
    print(f"  Staff cost ({garage.staff_count} staff): £{staff_cost}")
    if state.last_week_purchases > 0:
        print(f"  One-off purchases (engines/parts): £{state.last_week_purchases}")
    print(f"Total Outgoings this week: £{state.last_week_outgoings}")
    print(f"Income this week: £{state.last_week_income}")
    print(f"Total Money: £{state.money}")
    print(f"Cumulative Constructor Earnings: £{state.constructor_earnings}")


def show_engine_shop(state):
    print("\n=== Racecar Parts: Engines ===")

    # Show current engine
    if state.current_engine:
        eng = state.current_engine
        print("Current Engine:")
        print(f"  {eng['name']} (Source: {eng['supplier']})")
        print(f"    Speed .............. {eng['speed']}")
        print(f"    Reliability ........ {eng['reliability']}")
        print(f"    Acceleration ....... {eng['acceleration']}")
        print(f"    Heat Tolerance ..... {eng['heat_tolerance']}")
        print(f"    Notes: {eng['description']}")
    else:
        print("Current Engine: None installed")

    print("\nAvailable Engines:")
    for idx, engine in enumerate(engines, start=1):
        marker = " [CURRENT]" if state.current_engine and engine["id"] == state.current_engine["id"] else ""
        print(f"\n{idx}. {engine['name']}{marker}")
        print(f"   Supplier: {engine['supplier']}")
        print(f"     Speed .............. {engine['speed']}")
        print(f"     Reliability ........ {engine['reliability']}")
        print(f"     Acceleration ....... {engine['acceleration']}")
        print(f"     Heat Tolerance ..... {engine['heat_tolerance']}")
        print(f"     Price: £{engine['price']}")
        print(f"     About: {engine['description']}")



    # Buying logic
    choice = input("\nEnter the number of an engine to buy and install, or press Enter to go back: ").strip()

    if choice == "":
        return  # back to Garage menu

    if not choice.isdigit():
        print("Invalid input. No purchase made.")
        return

    idx = int(choice)
    if idx < 1 or idx > len(engines):
        print("Invalid engine selection.")
        return

    selected_engine = engines[idx - 1]

    # Already using this engine
    if state.current_engine and selected_engine["id"] == state.current_engine["id"]:
        print("You already have this engine installed.")
        return

    price = selected_engine["price"]
    if price > state.money:
        print(f"You cannot afford this engine. You need £{price}, but only have £{state.money}.")
        return

    # Perform purchase
    state.money -= price
    state.last_week_purchases += price

    state.current_engine = selected_engine
    state.car_speed = selected_engine["speed"]
    state.car_reliability = selected_engine["reliability"]

    print(f"\nYou have bought and installed the {selected_engine['name']}.")
    print(f"New car stats - Speed: {state.car_speed}, Reliability: {state.car_reliability}")


def show_driver_market(state):
    print("\n=== Driver Market ===")

    # Show current driver
    if state.player_driver:
        d = state.player_driver
        print("Current Driver:")
        print(f"  {d['name']} (Skill {d['skill']}, Consistency {d['consistency']})")
        print(f"  Racing for: {d['constructor']}")
    else:
        print("Current Driver: None hired")

    # Build market list: all non-Enzoni drivers
    market_drivers = [d for d in drivers if d["constructor"] != "Enzoni"]

    print("\nAvailable Drivers:")
    for idx, d in enumerate(market_drivers, start=1):
        marker = ""
        if state.player_driver is d:
            marker = " [CURRENT]"

        print(f"{idx}. {d['name']}{marker}")
        print(f"   Skill: {d['skill']}  Consistency: {d['consistency']}")
        print(f"   Registered constructor: {d['constructor']}")

    choice = input("\nEnter the number of a driver to hire, or press Enter to go back: ").strip()

    if choice == "":
        return  # back to main menu

    if not choice.isdigit():
        print("Invalid input. No hiring done.")
        return

    idx = int(choice)
    if idx < 1 or idx > len(market_drivers):
        print("Invalid driver selection.")
        return

    selected_driver = market_drivers[idx - 1]

    # Hire / assign to your team
    state.player_driver = selected_driver
    selected_driver["constructor"] = state.player_constructor  # now races for your company

    print(f"\nYou have hired {selected_driver['name']} as your driver.")
    print(f"They will now race for {state.player_constructor}.")


def show_garage(state):
    garage = state.garage
    print("\n=== Garage / Car Info ===")
    print(f"Garage Level: {garage.level}")
    print(f"Base Weekly Cost: £{garage.base_cost}")
    print(f"Staff Count: {garage.staff_count} (Salary £{garage.staff_salary} each)")
    print(f"Customer Parts Only: {garage.customer_parts_only}")
    print(f"R&D Enabled: {garage.r_and_d_enabled}")
    print(f"Factory Team: {garage.factory_team}")

    print("\nYour Car:")
    if state.current_engine:
        eng = state.current_engine
        print(f"  Engine: {eng['name']} (Supplier: {eng['supplier']})")
        print(f"    Speed .............. {eng['speed']}")
        print(f"    Reliability ........ {eng['reliability']}")
        print(f"    Acceleration ....... {eng['acceleration']}")
        print(f"    Heat Tolerance ..... {eng['heat_tolerance']}")
        print(f"    Notes: {eng['description']}")
    else:
        print("  Engine: None installed")


    print(f"  Overall Speed: {state.car_speed}")
    print(f"  Overall Reliability: {state.car_reliability}")

    if state.player_driver:
        print(f"Your Driver: {state.player_driver['name']} (Skill {state.player_driver['skill']}, Consistency {state.player_driver['consistency']})")
    else:
        print("No driver currently hired.")


# ------------------------------
# MAIN LOOP
# ------------------------------
def run_game():
    time = GameTime()
    state = GameState()
    setup_player(state)
    state.reset_championship()

    while True:
        # Auto-race if there's a race this week AND we haven't run it yet
        if (
            time.absolute_week in race_calendar
            and time.absolute_week not in state.completed_races
        ):
            run_race(state, race_calendar[time.absolute_week], time)
            state.completed_races.add(time.absolute_week)


        # Print news
        if state.news:
            print("\n=== News ===")
            for item in state.news:
                print(item)
            print("----------------")
            state.news.clear()

        # Main menu
        print(f"\n--- Week {time.week}, {MONTHS[time.month]} {time.year} ---")
        print("1. Calendar")
        print("2. Championship")
        print("3. Finances")
        print("4. Garage")
        print("5. Driver Market")
        print("6. Advance Week")

        choice = input("> ")

        if choice == "1":
            print(race_calendar.get(time.absolute_week, "No race this week."))
        elif choice == "2":
            print("\n=== Championship Standings (Top 10) ===")
            sorted_points = sorted(state.points.items(), key=lambda x: x[1], reverse=True)
            for name, pts in sorted_points[:10]:
                driver = next(d for d in drivers if d["name"] == name)
                print(f"{name} ({driver['constructor']}): {pts} pts")
        elif choice == "3":
            show_finances(state)
        elif choice == "4":  # Garage menu
            while True:
                print("\n=== Garage Menu ===")
                print("1. View Garage Info")
                print("2. Racecar Parts / Engine Shop")
                print("3. View Staff (coming soon)")
                print("4. Back to Main Menu")

                sub_choice = input("> ")

                if sub_choice == "1":
                    show_garage(state)
                elif sub_choice == "2":
                    show_engine_shop(state)
                elif sub_choice == "3":
                    print("Feature coming soon!")
                elif sub_choice == "4":
                    break
                else:
                    print("Invalid choice.")
        elif choice == "5":
            show_driver_market(state)
        elif choice == "6":
            # Apply weekly running costs for the week that just finished
            staff_cost = state.garage.staff_count * state.garage.staff_salary
            base_outgoings = state.garage.base_cost + staff_cost

            # total outgoings = base + staff + one-off purchases (for display)
            state.last_week_outgoings = base_outgoings + state.last_week_purchases

            # Deduct ONLY the recurring weekly costs from money
            state.money -= base_outgoings

            # Start a new week: clear purchases for the next period
            state.last_week_purchases = 0

            time.advance_week()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    run_game()
