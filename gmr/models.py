from .data import drivers

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
    
    @property
    def week_of_year(self):
        """Returns the week number of the current year (1-48)."""
        return (self.month * 4) + self.week


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
        self.car_durability = 0
        self.car_handling = 0
        self.constructor_earnings = 0
        self.last_week_income = 0
        self.last_week_outgoings = 0
        self.last_week_purchases = 0
        self.news = []
        self.garage = GarageState()

        # Car / engine & chassis
        self.current_engine = None
        self.current_chassis = None

        # Track which absolute weeks have already had a race run
        self.completed_races = set()

    def reset_championship(self):
        self.points = {d["name"]: 0 for d in drivers}
