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

The project uses `pytest` for testing.

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
