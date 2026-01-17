import random
import time as sys_time
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich import box

from .config import POINTS_TABLE, PRIZE_MONEY, CONSTRUCTOR_SHARE, ERA_RELIABILITY_MULTIPLIER
from .data import drivers, constructors, race_calendar
from .ui import console
from .mechanics import calculate_driver_performance

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
        performance, did_finish, failure_reason = calculate_driver_performance(d, state, constructors)

        if not did_finish:
            state.news.append(
                f"[red]{d['name']} ({d['constructor']}) retired ({failure_reason}).[/red]"
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
