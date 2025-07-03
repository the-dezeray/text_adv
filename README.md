# TermA ![License](https://img.shields.io/github/license/the-deezeray/text_adv)

![TermA](/terma-high-resolution-logo-transparent(1).png?raw=true "TermA")

**TermA (Terminal Adventure)** is a rich text-based adventure game built with Python and the Rich library. It features an interactive story system with configurable chapters, sound effects, and a modern terminal interface.

## Demo

https://github.com/the-dezeray/text_adv/assets/demo_vid.mp4

![Fight Demo](/fight_demo.png?raw=true "Combat System Demo")

## Features

- **Rich Terminal Interface**: Beautiful text rendering with colors and formatting using the Rich library
- **Configurable Story System**: YAML-based story files for easy content management
- **Chapter-based Progression**: Start from any chapter with configurable story paths
- **Sound Integration**: Audio cues and effects (can be muted)
- **Tank Mode**: Special gameplay mode for enhanced player capabilities
- **Menu System**: Optional menu interface
- **Debug Mode**: Development tools for testing and debugging

## Requirements

- **Python**: 3.13 or higher
- **UV**: Python package manager (required for dependency management)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/the-dezeray/text_adv.git
cd text_adv
```

### 2. Install Dependencies

The project uses UV for dependency management. Install all required packages:

```bash
uv sync
```

## Usage

### Basic Game Launch

Run the game with default settings (uses `data/gemini_story.yaml` as the default story):

```bash
uv run main.py
```

### Advanced Options

Use the debug script for more control over game parameters:

```bash
python debug.py [options]
```

#### Available Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-c, --chapter` | Start from specific chapter | `python debug.py -c 5` |
| `-s, --story` | Use custom story file | `python debug.py -s "data/custom_story.yaml"` |
| `-m, --mute` | Mute sound effects | `python debug.py -m` |
| `--tank` | Enable tank mode | `python debug.py --tank` |
| `--menu` | Show menu interface | `python debug.py --menu` |
| `--no-menu` | Hide menu interface | `python debug.py --no-menu` |
| `-sub, --subchapter` | Load specific subchapter | `python debug.py -sub "areas_to_explore.yaml"` |
| `-d, --dev` | Development mode (reloads config files) | `python debug.py -d` |
| `-r, --return` | Enable return to previous node | `python debug.py -r` |
| `-e, --event` | Load event from file | `python debug.py -e "event_file.yaml"` |

### Configuration

The game uses several configuration files located in the `data/` directory:

- `gemini_story.yaml` - Main story content (default story file)
- `areas_to_explore.yaml` - Exploration areas
- `config.yaml` - Game configuration
- `entities.yaml` - Game entities
- `items.yaml` - Item definitions
- `weapons.yaml` - Weapon specifications

## Story Format

TermA uses YAML files to define interactive stories. Here's an example of the story format:

```yaml
0:
  location: "The Brink of Awareness"
  text: "A jolt, and you're tumbling into consciousness. Your hand closes around something small and cool on the uneven ground – a [red1]Dimly Glowing Stone[/]. It offers little light, but a faint warmth. Before you can ponder its origin, the world solidifies..."
  choices:
    - text: "Open your eyes fully."
      next_node: 1
      function: "receive_item(item='sword', core=core)"

1:
  location: "The Obsidian Labyrinth - Genesis Point"
  text: "You awaken with a gasp, cold stone beneath you. Jagged obsidian walls pulse with faint, internal light, like veins of molten ore. Strange, sibilant whispers echo, too faint to discern, yet chillingly close. Where are you? How did you get here?"
  choices:
    - text: "Trace the glowing veins deeper into the rock."
      next_node: 2
      function: "apply_effect(effect='cold', duration='medium', core=core, str='you are charmed and cannot resist the cold')"
    - text: "Focus, try to understand the whispers."
      next_node: 3
      function: "skill_check(skill='hp',limit=2, core=core)"

2:
  location: "The Pulsing Vein Tunnels"
  text: "The passage narrows, the air growing warm and metallic. The glowing veins in the obsidian cast dancing shadows. Ahead, you see ancient murals etched into the walls, depicting beings of shadow and light locked in an eternal struggle."
  choices:
    - text: "Examine the murals closely."
      next_node: 4
      function: "explore(area='creek', core=core)"
    - text: "Press on, the murals are just distractions."
      next_node: 5
      function: null
```

### Story Structure

Each story node contains:
- **`location`**: The current location name
- **`text`**: The narrative text (supports Rich formatting like `[red1]text[/]`)
- **`choices`**: Array of player choices with:
  - **`text`**: Choice description
  - **`next_node`**: ID of the next story node
  - **`function`**: Optional function call (can be `null`)

## Development

### Project Structure

```
text_adv/
├── core/           # Core game logic
├── data/           # Configuration and story files
├── objects/        # Game objects and entities
├── ui/             # User interface components
├── util/           # Utility functions
├── tests/          # Test files
└── assets/         # Game assets (images, sounds)
```

### Running Tests

```bash
uv run pytest
```

### Development Mode

For development with automatic file reloading:

```bash
python debug.py -d
```

## Dependencies

Key dependencies include:

- **Rich**: Terminal formatting and UI
- **PyYAML**: YAML file parsing
- **ReadChar**: Keyboard input handling
- **Pygame**: Audio support
- **Google Generative AI**: AI-powered content generation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the terms specified in the LICENSE file.

## Roadmap

### Planned Features

- [ ] Enhanced AI story generation
- [ ] More interactive NPCs
- [ ] Advanced combat system
- [ ] Save/load functionality
- [ ] User-generated content support
- [ ] Multiplayer capabilities

### Current Status

- ✅ Core game engine
- ✅ Rich terminal interface
- ✅ YAML-based story system
- ✅ Sound integration
- ✅ Debug tools
- 🔄 AI generation (disabled, coming soon)

For the latest updates, check the project roadmap at [terma.com/roadmap](http://terma.com/roadmap).
