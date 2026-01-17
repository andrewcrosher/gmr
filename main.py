# ------------------------------
# GMR Bootloader - Stable Build (Rich UI Enriched)
# ------------------------------

import random
import time as sys_time  # Renamed to avoid conflict with game time logic
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich import box

# Initialize Rich Console
console = Console()

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
    console.print(Panel.fit(
        "[bold cyan]Your father passed away, leaving you his old racing chassis.[/bold cyan]\n"
        "You inherit a small shed for a garage and a single mechanic.\n"
        "[italic]This is the start of your racing adventure.[/italic]",
        title="Welcome to GMR",
        border_style="cyan"
    ))

    # Ask player for constructor/company name
    state.player_constructor = console.input("[bold yellow]Enter the name of your racing company: [/bold yellow]")

    # Garage starting state
    state.garage.level = 0
    state.garage.base_cost = 80
    state.garage.staff_count = 1
    state.garage.staff_salary = 20

    # Starting engine
    starting_engine = next(e for e in engines if e["id"] == "dad_old")
    state.current_engine = starting_engine
    state.car_speed = starting_engine["speed"]
    state.car_reliability = starting_engine["reliability"]

    # Player driver is None for now
    state.player_driver = None

    console.print(f"\n[bold green]Welcome to {state.player_constructor}! Your journey begins...[/bold green]\n")
    sys_time.sleep(1.5)


# ------------------------------
# RACE LOGIC (VISUALIZED)
# ------------------------------
def run_race(state, race_name, time):
    console.clear()
    state.news.append(f"=== {race_name} ===")
    state.last_week_income = 0
    
    # --- VISUAL RACE SIMULATION ---
    console.rule(f"[bold red]{race_name}[/bold red]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        transient=True
    ) as progress:
        task = progress.add_task("[green]Racing...", total=100)
        
        for i in range(10):
            sys_time.sleep(0.3)  # Artificial delay for suspense
            progress.update(task, advance=10)
    
    # --- CALCULATION LOGIC ---
    finishers = []

    for d in drivers:
        # Base driver performance with consistency variance
        consistency_factor = d["consistency"] / 10
        variance = random.uniform(-1, 1) * (1 - consistency_factor) * d["skill"]
        performance = d["skill"] + variance

        # Decide where the car performance comes from
        if d == state.player_driver:
            # Player's car
            car_speed = state.car_speed
            car_reliability = state.car_reliability
        else:
            # AI drivers
            ctor_stats = constructors.get(d["constructor"], {"speed": 5, "reliability": 5})
            car_speed = ctor_stats["speed"]
            car_reliability = ctor_stats["reliability"]

        performance += car_speed

        # Reliability + DNF chance
        reliability = car_reliability
        dnf_chance = (11 - reliability) * 0.02 * ERA_RELIABILITY_MULTIPLIER

        if random.random() < dnf_chance:
            state.news.append(
                f"[red]{d['name']} ({d['constructor']}) retired (Engine Failure).[/red]"
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

    # Display Race Result Table
    table = Table(title=f"🏁 {race_name} Results 🏁", box=box.SIMPLE)
    table.add_column("Pos", style="cyan", justify="right")
    table.add_column("Driver", style="white")
    table.add_column("Team", style="dim")
    table.add_column("Pts", justify="right", style="bold yellow")

    for i, (d, _) in enumerate(finishers[:10]):
        pts = POINTS_TABLE[i] if i < len(POINTS_TABLE) else 0
        
        # Highlight player
        if d == state.player_driver:
            table.add_row(str(i+1), f"[bold green]{d['name']}[/bold green]", d['constructor'], str(pts))
        else:
            table.add_row(str(i+1), d['name'], d['constructor'], str(pts) if pts > 0 else "")

        state.news.append(f"{i+1}. {d['name']} ({d['constructor']})")

    console.print(table)
    console.input("\n[dim]Press Enter to continue...[/dim]")

    # End of season check
    # Check if we have completed the last race of the year
    last_race_week = max(race_calendar.keys())
    week_of_year = time.week_of_year
    
    if week_of_year == last_race_week and f"{time.year}-{week_of_year}" in state.completed_races:
        # Only trigger end of season once
        winner = max(state.points, key=state.points.get)
        state.news.append(f"*** [bold gold1]{winner} wins the {time.year} Championship![/bold gold1] ***")
        state.reset_championship()
        # Note: We don't clear completed_races because we use (year, week) keys now


# ------------------------------
# UI
# ------------------------------
def show_finances(state):
    garage = state.garage
    staff_cost = garage.staff_count * garage.staff_salary
    
    table = Table(title="Finances", box=box.ROUNDED)
    table.add_column("Item", style="cyan")
    table.add_column("Amount", justify="right")

    table.add_row("Base Garage Cost", f"£{garage.base_cost}")
    table.add_row(f"Staff Cost ({garage.staff_count})", f"£{staff_cost}")
    
    if state.last_week_purchases > 0:
        table.add_row("Parts/Engines", f"[red]£{state.last_week_purchases}[/red]")
    
    table.add_section()
    table.add_row("Total Outgoings", f"[red]£{state.last_week_outgoings}[/red]")
    table.add_row("Last Week Income", f"[green]£{state.last_week_income}[/green]")
    table.add_section()
    
    # Highlight total money
    money_style = "bold green" if state.money > 0 else "bold red"
    table.add_row("Current Balance", f"[{money_style}]£{state.money}[/{money_style}]")
    table.add_row("Lifetime Earnings", f"£{state.constructor_earnings}", style="dim")

    console.print(table)


def show_engine_shop(state):
    console.clear()
    
    # Current Engine Panel
    if state.current_engine:
        eng = state.current_engine
        txt = (
            f"[bold]{eng['name']}[/bold]\n"
            f"Supplier: {eng['supplier']}\n\n"
            f"Speed:       {'[cyan]▮[/cyan]' * eng['speed']}{'[dim]▮[/dim]' * (10-eng['speed'])}\n"
            f"Reliability: {'[green]▮[/green]' * eng['reliability']}{'[dim]▮[/dim]' * (10-eng['reliability'])}\n"
            f"Accel:       {eng['acceleration']}\n"
            f"Heat Tol:    {eng['heat_tolerance']}\n\n"
            f"[italic]{eng['description']}[/italic]"
        )
        console.print(Panel(txt, title="Current Installed Engine", border_style="blue"))
    else:
        console.print("[red]No engine installed![/red]")

    # Shop Table
    table = Table(title="Engine Supplier Catalogue", box=box.HEAVY_HEAD)
    table.add_column("#", style="dim")
    table.add_column("Name", style="bold")
    table.add_column("Stats (Spd/Rel)", justify="center")
    table.add_column("Price", justify="right", style="green")
    table.add_column("Description")

    for idx, engine in enumerate(engines, start=1):
        marker = " [bold blue](OWNED)[/bold blue]" if state.current_engine and engine["id"] == state.current_engine["id"] else ""
        stats = f"S:{engine['speed']} R:{engine['reliability']}"
        table.add_row(str(idx), f"{engine['name']}{marker}", stats, f"£{engine['price']}", engine['description'])

    console.print(table)

    # Buying logic
    choice = console.input("\nEnter [bold cyan]ID[/bold cyan] to buy, or Enter to go back: ").strip()

    if choice == "":
        return

    if not choice.isdigit():
        console.print("[red]Invalid input.[/red]")
        return

    idx = int(choice)
    if idx < 1 or idx > len(engines):
        console.print("[red]Invalid selection.[/red]")
        return

    selected_engine = engines[idx - 1]

    if state.current_engine and selected_engine["id"] == state.current_engine["id"]:
        console.print("[yellow]You already have this engine installed.[/yellow]")
        return

    price = selected_engine["price"]
    if price > state.money:
        console.print(f"[bold red]Insufficient Funds![/bold red] Cost: £{price}, You have: £{state.money}")
        return

    # Perform purchase
    state.money -= price
    state.last_week_purchases += price

    state.current_engine = selected_engine
    state.car_speed = selected_engine["speed"]
    state.car_reliability = selected_engine["reliability"]

    console.print(f"[bold green]Purchased and installed {selected_engine['name']}![/bold green]")
    sys_time.sleep(1.5)


def show_driver_market(state):
    console.clear()
    
    # Current Driver
    if state.player_driver:
        d = state.player_driver
        console.print(Panel(
            f"[bold]{d['name']}[/bold] (Skill: {d['skill']}, Consistency: {d['consistency']})", 
            title="Current Driver", border_style="green"
        ))
    else:
        console.print(Panel("No driver hired.", title="Current Driver", border_style="red"))

    market_drivers = [d for d in drivers if d["constructor"] != "Enzoni"]

    table = Table(title="Driver Market", box=box.SIMPLE)
    table.add_column("#", style="dim")
    table.add_column("Name", style="bold white")
    table.add_column("Skill", justify="center")
    table.add_column("Consistency", justify="center")
    table.add_column("Status", style="italic")

    for idx, d in enumerate(market_drivers, start=1):
        status = "Your Driver" if state.player_driver is d else d['constructor']
        style = "green" if state.player_driver is d else "white"
        table.add_row(
            str(idx), 
            f"[{style}]{d['name']}[/{style}]", 
            str(d['skill']), 
            str(d['consistency']), 
            status
        )

    console.print(table)
    choice = console.input("\nEnter [bold cyan]ID[/bold cyan] to hire, or Enter to go back: ").strip()

    if choice == "" or not choice.isdigit():
        return

    idx = int(choice)
    if idx < 1 or idx > len(market_drivers):
        return

    # RELEASE OLD DRIVER
    if state.player_driver:
        # Set the previous driver back to Independent
        state.player_driver["constructor"] = "Independent"
        # Reset their performance to base (optional, but good practice)

    selected_driver = market_drivers[idx - 1]
    state.player_driver = selected_driver
    selected_driver["constructor"] = state.player_constructor

    console.print(f"[bold green]Hired {selected_driver['name']}![/bold green]")
    sys_time.sleep(1)


def show_garage(state):
    garage = state.garage
    
    # Create a layout for nice info display
    info_table = Table.grid(padding=1)
    info_table.add_column(style="bold cyan", justify="right")
    info_table.add_column(style="white")
    
    info_table.add_row("Garage Level:", str(garage.level))
    info_table.add_row("Staff:", f"{garage.staff_count} (Cost: £{garage.staff_count * garage.staff_salary}/wk)")
    info_table.add_row("Base Cost:", f"£{garage.base_cost}/wk")

    # Car Stats visualization
    eng_name = state.current_engine['name'] if state.current_engine else "None"
    
    car_panel = Panel(
        f"Engine: [bold]{eng_name}[/bold]\n"
        f"Speed:       [cyan]{state.car_speed}[/cyan]\n"
        f"Reliability: [green]{state.car_reliability}[/green]",
        title="Car Status",
        border_style="yellow"
    )

    console.print(Panel(info_table, title="Facilities", border_style="blue"))
    console.print(car_panel)


# ------------------------------
# MAIN LOOP
# ------------------------------
def run_game():
    time = GameTime()
    state = GameState()
    
    console.clear()
    setup_player(state)
    state.reset_championship()

    while True:
        # Check if there is a race this specific week of the year
        week_of_year = time.week_of_year
        race_key = f"{time.year}-{week_of_year}"

        if (
            week_of_year in race_calendar
            and race_key not in state.completed_races
        ):
            run_race(state, race_calendar[week_of_year], time)
            state.completed_races.add(race_key)


        console.clear()
        
        # --- HEADER ---
        console.print(Panel(
            f"[bold white]Week {time.week}[/bold white] | [cyan]{MONTHS[time.month]} {time.year}[/cyan]\n"
            f"Money: [bold green]£{state.money}[/bold green] | "
            f"Car: [yellow]{state.player_constructor}[/yellow] | "
            f"Driver: {state.player_driver['name'] if state.player_driver else 'None'}",
            style="on black"
        ))

        # --- NEWS TICKER ---
        if state.news:
            console.print("[bold underline]Recent News:[/bold underline]")
            for item in state.news:
                console.print(f" > {item}")
            console.print("")
            state.news.clear()

        # --- MAIN MENU TABLE ---
        menu = Table(show_header=False, box=None)
        menu.add_column("Option", style="bold cyan")
        menu.add_column("Description")
        
        menu.add_row("1", "View Calendar")
        menu.add_row("2", "Championship Standings")
        menu.add_row("3", "Finances")
        menu.add_row("4", "Garage Management")
        menu.add_row("5", "Driver Market")
        menu.add_row("6", "[bold yellow]Advance Week[/bold yellow]")
        
        console.print(Panel(menu, title="Main Menu", border_style="white"))

        choice = console.input("> ")

        if choice == "1":
            # Check based on week_of_year for recurring calendar
            week_num = time.week_of_year
            evt = race_calendar.get(week_num, "No race this week.")
            
            # Display slightly more info
            txt = f"[bold]{evt}[/bold]" if week_num in race_calendar else evt
            console.print(Panel(txt, title=f"Week {week_num} Event"))
            console.input("[dim]Press Enter...[/dim]")
            
        elif choice == "2":
            table = Table(title="Championship Standings", box=box.SIMPLE)
            table.add_column("Pos", justify="right", style="cyan")
            table.add_column("Driver", style="bold white")
            table.add_column("Team", style="dim")
            table.add_column("Points", justify="right", style="bold yellow")
            
            sorted_points = sorted(state.points.items(), key=lambda x: x[1], reverse=True)
            for i, (name, pts) in enumerate(sorted_points[:10], start=1):
                driver = next(d for d in drivers if d["name"] == name)
                # Highlight player row
                style = "green" if driver['constructor'] == state.player_constructor else "white"
                table.add_row(str(i), f"[{style}]{name}[/{style}]", driver['constructor'], str(pts))
            
            console.print(table)
            console.input("[dim]Press Enter...[/dim]")

        elif choice == "3":
            show_finances(state)
            console.input("[dim]Press Enter...[/dim]")
            
        elif choice == "4":  # Garage menu
            while True:
                console.clear()
                console.print(Panel("[1] View Stats\n[2] Engine Shop\n[3] Staff (WIP)\n[4] Back", title="Garage"))
                sub = console.input("Garage > ")
                if sub == "1":
                    show_garage(state)
                    console.input("Press Enter...")
                elif sub == "2":
                    show_engine_shop(state)
                elif sub == "3":
                    console.print("[yellow]Coming soon![/yellow]")
                    sys_time.sleep(1)
                elif sub == "4":
                    break

        elif choice == "5":
            show_driver_market(state)
            
        elif choice == "6":
            # Costs logic remains identical
            staff_cost = state.garage.staff_count * state.garage.staff_salary
            base_outgoings = state.garage.base_cost + staff_cost
            state.last_week_outgoings = base_outgoings + state.last_week_purchases
            state.money -= base_outgoings
            state.last_week_purchases = 0
            time.advance_week()
            
            # Show a small transition animation
            with console.status("[bold green]Processing week...[/bold green]", spinner="dots"):
                sys_time.sleep(0.5)
        else:
            console.print("[red]Invalid choice.[/red]")
            sys_time.sleep(0.5)


if __name__ == "__main__":
    run_game()