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

    def to_dict(self):
        return {"year": self.year, "month": self.month, "week": self.week, "absolute_week": self.absolute_week}

    @classmethod
    def from_dict(cls, data):
        gt = cls(data["year"])
        gt.month = data["month"]
        gt.week = data["week"]
        gt.absolute_week = data["absolute_week"]
        return gt


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

    def to_dict(self):
        return vars(self)

    @classmethod
    def from_dict(cls, data):
        gs = cls()
        gs.__dict__.update(data)
        return gs


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

    def to_dict(self):
        data = vars(self).copy()
        data["garage"] = self.garage.to_dict()
        data["completed_races"] = list(self.completed_races)
        return data

    @classmethod
    def from_dict(cls, data):
        gs = cls()
        if "garage" in data:
            garage_data = data.pop("garage")
            gs.garage = GarageState.from_dict(garage_data)
        if "completed_races" in data:
            completed_races = data.pop("completed_races")
            gs.completed_races = set(completed_races)
        gs.__dict__.update(data)
        return gs
