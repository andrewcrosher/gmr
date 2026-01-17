import time as sys_time
from rich.panel import Panel
from rich.table import Table
from rich import box

from .models import GameTime, GameState
from .data import engines, chassis, race_calendar, drivers, reset_drivers
from .config import MONTHS
from .ui import (
    console, 
    show_finances, 
    show_engine_shop, 
    show_chassis_shop, 
    show_driver_market, 
    show_garage,
    upgrade_garage
)
from .race import run_race
from .mechanics import process_random_events
from .storage import save_game, load_game

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
    while True:
        name = console.input("[bold yellow]Enter the name of your racing company: [/bold yellow]").strip()
        if name:
            state.player_constructor = name
            break
        console.print("[red]Name cannot be empty.[/red]")

    # Garage starting state
    state.garage.level = 0
    state.garage.base_cost = 80
    state.garage.staff_count = 1
    state.garage.staff_salary = 20

    # Starting engine and chassis
    starting_engine = next(e for e in engines if e["id"] == "dad_old")
    state.current_engine = starting_engine

    starting_chassis = next(c for c in chassis if c["id"] == "dad_old_chassis")
    state.current_chassis = starting_chassis

    state.car_speed = starting_engine["speed"]
    state.car_reliability = starting_engine["reliability"]
    state.car_durability = starting_chassis["durability"]
    state.car_handling = starting_chassis["handling"]

    # Player driver is None for now
    state.player_driver = None

    console.print(f"\n[bold green]Welcome to {state.player_constructor}! Your journey begins...[/bold green]\n")
    sys_time.sleep(1.5)


# ------------------------------
# MAIN LOOP
# ------------------------------
def run_game():
    time = GameTime()
    state = GameState()
    
    console.clear()
    
    # Start Menu
    console.print(Panel.fit("[bold white]GMR - Grand Management Racing[/bold white]", style="bold red"))
    console.print("[1] New Game")
    console.print("[2] Load Game")
    choice = console.input("> ")
    
    if choice == "2":
        reset_drivers()
        loaded_state, loaded_time = load_game()
        if loaded_state:
            state = loaded_state
            time = loaded_time
            console.print("[green]Game Loaded Successfully![/green]")
            sys_time.sleep(1)
        else:
            console.print("[red]No save found or load failed. Starting new game...[/red]")
            sys_time.sleep(1.5)
            reset_drivers()
            setup_player(state)
            state.reset_championship()
    else:
        reset_drivers()
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
        menu.add_row("7", "Save Game")
        menu.add_row("8", "Exit Game")
        
        console.print(Panel(menu, title="Main Menu", border_style="white"))

        choice = console.input("> ")

        if choice == "1":
            # Check based on week_of_year for recurring calendar
            week_num = time.week_of_year
            evt = race_calendar.get(week_num)
            
            if evt:
                txt = f"[bold]{evt['name']}[/bold]\nType: {evt['type']}"
            else:
                txt = "No race this week."
            
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
                console.print(Panel("[1] View Stats\n[2] Engine Shop\n[3] Chassis Shop\n[4] Staff (WIP)\n[5] Upgrade Facility\n[6] Back", title="Garage"))
                sub = console.input("Garage > ")
                if sub == "1":
                    show_garage(state)
                    console.input("Press Enter...")
                elif sub == "2":
                    show_engine_shop(state)
                elif sub == "3":
                    show_chassis_shop(state)
                elif sub == "4":
                    console.print("[yellow]Coming soon![/yellow]")
                    sys_time.sleep(1)
                elif sub == "5":
                    upgrade_garage(state)
                elif sub == "6":
                    break

        elif choice == "5":
            show_driver_market(state)
            
        elif choice == "6":
            # Costs logic
            staff_cost = state.garage.staff_count * state.garage.staff_salary
            driver_salary = state.player_driver.get("salary", 0) if state.player_driver else 0
            
            base_outgoings = state.garage.base_cost + staff_cost + driver_salary
            state.last_week_outgoings = base_outgoings + state.last_week_purchases
            state.money -= base_outgoings
            state.last_week_purchases = 0
            time.advance_week()
            
            # Show a small transition animation
            with console.status("[bold green]Processing week...[/bold green]", spinner="dots"):
                sys_time.sleep(0.5)
                
            # Trigger Random Events
            events = process_random_events(state)
            if events:
                state.news.extend(events)
        
        elif choice == "7":
            save_game(state, time)
            console.print("[bold green]Game Saved![/bold green]")
            sys_time.sleep(1)
            
        elif choice == "8":
            console.print("Thanks for playing!")
            break
            
        else:
            console.print("[red]Invalid choice.[/red]")
            sys_time.sleep(0.5)
