# GMR

A text-based Formula 1 management simulation game built in Python, featuring a modern CLI dashboard.

## Description

GMR (Grand Management Racing) is a retro-style Formula 1 management simulator where you take on the role of a team manager in the early days of motorsport. Build your garage, hire drivers, upgrade your cars, and compete in championships while managing finances and navigating the challenges of racing.

**Now enhanced with `Rich`:** The game features a full dashboard UI with color-coded data, live race simulation bars, and organized menus.

## Features

- **Rich CLI Interface**: Modern terminal UI with live progress bars, color-coded tables, and clear panels.
- **Time Progression**: Realistic weekly advancement through months and years.
- **Race Calendar**: Compete in a series of Grand Prix events with proper scoring.
- **Driver Management**: Hire and manage drivers with unique skills and consistency ratings.
- **Car Upgrades**: Upgrade engines and chassis with real performance impacts.
- **Financial Management**: Track income, expenses, and maintain your team's budget.
- **Championship Standings**: Compete for constructors' and drivers' championships.

## Installation

### Prerequisites

- Python 3.8 or higher recommended
- **Important:** A terminal that supports ANSI colors (e.g., VS Code Terminal, Windows Terminal, or Git Bash).

### Setup

1. Clone the repository:
   ```powershell
   git clone [https://github.com/andrewcrosher/gmr.git](https://github.com/andrewcrosher/gmr.git)
   cd gmr
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Usage

Run the game from the command line:

```powershell
python main.py
```

Follow the on-screen menus to manage your team, view standings, upgrade your car, and compete in races.

## Development

This project is primarily developed on Windows using PowerShell.

### Running Tests

The project is set up to use `pytest`, though no tests are currently implemented.

```powershell
pytest
```

### Project Structure

- `main.py`: Entry point script
- `gmr/`: Game package source code
  - `app.py`: Main application loop and setup
  - `race.py`: Race logic and simulation
  - `mechanics.py`: Game mechanics and calculations
  - `ui.py`: UI rendering with Rich
  - `models.py`: Data models (GameState, etc.)
  - `data.py`: Static game data (Drivers, Engines, etc.)
  - `config.py`: Configuration constants
- `requirements.txt`: Python dependencies
- `README.md`: This file

## Changelog

### v0.6 — Next Targets (early notes)
*Not built yet, but logically next in line*
- Chassis stat system mirroring engines
- Car performance as engine + chassis + driver
- Weather & circuit effects
- Random events (injury, sponsor offers, parts failing)
- Scouting, contracts, driver salary
- Garage promotions (customer → works team)

### v0.5 — Upgrades Become Real
*Player choice finally matters*
- Engine shop implemented
  - View install & compare multiple engines
  - Prices enforced
  - Money deducted only once, not every week
  - Outgoings recorded correctly
  - Car stats update to match engine
- Engine stats expanded
  - Speed
  - Reliability
  - Acceleration
  - Heat tolerance
  - Displayed consistently in shop UI and garage
- Driver Market added
  - Independent roster of hireable drivers
  - Enzoni drivers restricted (already contracted)
  - Hiring updates team assignment and race performance
- Race loop hardened
  - Race only triggers once per race week
  - Menus no longer "repeat" events or reassign points
- *First moment the player genuinely builds a team instead of just watching a simulation.*

### v0.4 — Systems Stabilised & Reality Added
*Gameplay logic tightened, economy stops lying*
- DNF logic fixed — retired drivers no longer wrongly earn points
- Finances reflect the real world
  - Running costs deducted weekly
  - Prize money and weekly spending tracked accurately
- Garage menu added
  - View chassis/engine basics
  - Status flags for future development
- Finances UI improved
  - Outgoings annotated
  - Earnings summarised
  - Constructor income tracked over time
- *This made the game feel like a real management sim instead of random numbers.*

### v0.3 — Foundations (pre-session recap)
*Core systems established*
- Weekly time progression (weeks → months → years)
- Baseline race calendar and scoring
- Basic driver & constructor roster
- Rudimentary car inherited from player's father
- Money drains weekly from garage upkeep
- Simple race simulation with reliability/skill variance
- Championship standings reset at season end
- Menu-driven UI loop with calendar, standings, finances
- *Solid skeleton. Playable end-to-end loop, but everything relied on magic values and placeholders.*