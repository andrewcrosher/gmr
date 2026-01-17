import time as sys_time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from .data import engines, chassis, drivers

# Initialize Rich Console
console = Console()

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


def show_chassis_shop(state):
    console.clear()
    
    # Current Chassis Panel
    if state.current_chassis:
        cha = state.current_chassis
        txt = (
            f"[bold]{cha['name']}[/bold]\n"
            f"Supplier: {cha['supplier']}\n\n"
            f"Durability:  {'[red]▮[/red]' * cha['durability']}{'[dim]▮[/dim]' * (10-cha['durability'])}\n"
            f"Handling:    {'[blue]▮[/blue]' * cha['handling']}{'[dim]▮[/dim]' * (10-cha['handling'])}\n\n"
            f"[italic]{cha['description']}[/italic]"
        )
        console.print(Panel(txt, title="Current Installed Chassis", border_style="blue"))
    else:
        console.print("[red]No chassis installed![/red]")

    # Shop Table
    table = Table(title="Chassis Fabricator Catalogue", box=box.HEAVY_HEAD)
    table.add_column("#", style="dim")
    table.add_column("Name", style="bold")
    table.add_column("Stats (Dur/Hnd)", justify="center")
    table.add_column("Price", justify="right", style="green")
    table.add_column("Description")

    for idx, c in enumerate(chassis, start=1):
        marker = " [bold blue](OWNED)[/bold blue]" if state.current_chassis and c["id"] == state.current_chassis["id"] else ""
        stats = f"D:{c['durability']} H:{c['handling']}"
        table.add_row(str(idx), f"{c['name']}{marker}", stats, f"£{c['price']}", c['description'])

    console.print(table)

    # Buying logic
    choice = console.input("\nEnter [bold cyan]ID[/bold cyan] to buy, or Enter to go back: ").strip()

    if choice == "":
        return

    if not choice.isdigit():
        console.print("[red]Invalid input.[/red]")
        return

    idx = int(choice)
    if idx < 1 or idx > len(chassis):
        console.print("[red]Invalid selection.[/red]")
        return

    selected_chassis = chassis[idx - 1]

    if state.current_chassis and selected_chassis["id"] == state.current_chassis["id"]:
        console.print("[yellow]You already have this chassis installed.[/yellow]")
        return

    price = selected_chassis["price"]
    if price > state.money:
        console.print(f"[bold red]Insufficient Funds![/bold red] Cost: £{price}, You have: £{state.money}")
        return

    # Perform purchase
    state.money -= price
    state.last_week_purchases += price

    state.current_chassis = selected_chassis
    state.car_durability = selected_chassis["durability"]
    state.car_handling = selected_chassis["handling"]

    console.print(f"[bold green]Purchased and installed {selected_chassis['name']}![/bold green]")
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
    chas_name = state.current_chassis['name'] if state.current_chassis else "None"
    
    car_panel = Panel(
        f"Engine:      [bold]{eng_name}[/bold]\n"
        f"Chassis:     [bold]{chas_name}[/bold]\n"
        f"Speed:       [cyan]{state.car_speed}[/cyan]\n"
        f"Acceleration:[cyan]{state.current_engine['acceleration']}[/cyan]\n"
        f"Handling:    [blue]{state.car_handling}[/blue]\n"
        f"Reliability: [green]{state.car_reliability}[/green]\n"
        f"Durability:  [green]{state.car_durability}[/green]",
        title="Car Status",
        border_style="yellow"
    )

    console.print(Panel(info_table, title="Facilities", border_style="blue"))
    console.print(car_panel)
