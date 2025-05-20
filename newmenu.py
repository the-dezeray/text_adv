from rich.console import Console, ConsoleRenderable, Group
from rich.panel import Panel
from rich.align import Align
from rich.padding import Padding
from rich.text import Text
from rich.layout import Layout
from rich.live import Live
from rich.spinner import Spinner # Added import
import time
from typing import Optional, Callable, List, Any

# --- Placeholder for your existing classes ---
class CustomRenderable:
    def __init__(self, text: str = "", func: Optional[Callable[[], Any]] = None, next_node=None, type: str = "", icon: str = "", description: str = "", h_allign: str = "left"):
        self.text = text
        self.func = func
        self.next_node = next_node
        self.type = type
        self.icon = icon
        self.description = description
        self.h_allign = h_allign
        self.selected = False
        self.style: str = ""

    def __rich_console__(self, console: Console, options: Any) -> ConsoleRenderable:
        return self.render(console=console)

    def render(self, style: str = "", left_padding: int = 0, core: Optional[Any] = None, console: Optional[Console] = None) -> ConsoleRenderable:
        return Text(f"{self.icon} {self.text}")

class Core:
    def __init__(self):
        self.console = Console(record=True)
        self.current_selection = 0
        self.menu_options: List[MenuOption] = []
        self.game_layout = self.create_layout()
        self.active_status: Optional[ConsoleRenderable] = None # For spinner/status messages

    def _transition_layout(self, layout_name: str):
        # Removed: with self.console.status(...)
        # Prints will be captured by the main Live display
        self.console.print(f"[dim sky_blue1]Attempting transition to {layout_name}...[/dim sky_blue1]")
        time.sleep(1.0) # Simulate work
        self.console.print(f"[bold cyan]Transitioning to {layout_name}...[/bold cyan]")
        if layout_name == "INGAME" and any(opt.text == "Continue" and opt.selected for opt in self.menu_options):
            self.console.print("Resuming game...")
        elif layout_name == "NEWGAME" and any(opt.text == "New game" and opt.selected for opt in self.menu_options):
            self.console.print("Starting a new adventure!")
        elif layout_name == "SETTINGS":
            self.console.print("Opening settings menu...")
        elif layout_name == "ABOUTUS":
            self.console.print("Displaying information about us...")
        time.sleep(0.5) # More simulated work
        self.console.print(f"[bold green]{layout_name} loaded successfully![/bold green]")
        time.sleep(0.5) # Pause to see the final message from print

    def TERMINATE(self):
        # Removed: with self.console.status(...)
        self.console.print("[bold red]Preparing to exit game...[/bold red]")
        time.sleep(1.5) # Simulate saving progress, cleanup
        self.console.print("[bold red]Exited cleanly. (Message from TERMINATE method)[/bold red]")
        raise KeyboardInterrupt # Simulate exit for Live display

    def create_layout(self) -> Layout:
        layout = Layout(name="root")
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=5), # Original footer size
            Layout(name="status_bar", size=1) # New dedicated layout for status messages/spinner
        )
        layout["main"].split_row(
            Layout(name="menu_panel", ratio=1),
            Layout(name="description_panel", ratio=2),
        )
        layout["footer"].split_row(
            Layout(name="version_info", ratio=1),
            Layout(name="updates_info", ratio=1)
        )
        return layout

    def update_layout(self):
        self.game_layout["header"].update(Align.center(Text("MY AWESOME TERMINAL GAME", style="bold magenta underline")))

        menu_renderables = []
        selected_description = ""
        for i, option in enumerate(self.menu_options):
            option.selected = (i == self.current_selection)
            menu_renderables.append(option.render(core=self))
            if option.selected:
                selected_description = option.description

        self.game_layout["menu_panel"].update(
            Panel(Group(*menu_renderables), title="[bold blue]Main Menu[/]", border_style="blue", padding=(1,1))
        )
        self.game_layout["description_panel"].update(
            Panel(Align.center(Text(selected_description, style="italic yellow"), vertical="middle"), title="[bold blue]Details[/]", border_style="blue", padding=(2,2), height=len(menu_renderables) * 3 + 2)
        )

        GAME_VERSION = "v0.1.0-alpha"; RECENT_UPDATES = " Last Update: 2025-05-16\n- Added awesome menu!\n- Fixed a bug with flying teapots."
        VERSION_ICON = ""; UPDATES_ICON = ""

        version_title = Text("Version", style="bold dim"); version_text = Text(f"{VERSION_ICON} {GAME_VERSION}", style="dim cyan")
        self.game_layout["version_info"].update(Padding(Group(Align.left(version_title), Align.left(version_text)),(1,2)))

        updates_title = Text("Updates", style="bold dim"); updates_text = Text(f"{UPDATES_ICON} Recent Updates:\n{RECENT_UPDATES}", style="dim cyan")
        self.game_layout["updates_info"].update(Padding(Group(Align.left(updates_title), Align.left(updates_text)), (1,2)))

        # Update status bar
        if self.active_status:
            self.game_layout["status_bar"].update(Align.center(self.active_status))
        else:
            self.game_layout["status_bar"].update("") # Clear the status bar when no active status

        return self.game_layout

# --- MenuOption and menu_items_list are unchanged ---
class MenuOption(CustomRenderable):
    def __init__(self, icon: str, text: str, description: str, **kwargs):
        super().__init__(text=text, icon=icon, description=description, **kwargs)
        if 'h_allign' not in kwargs:
            kwargs['h_allign'] = "left"
        self.type = "menu"

    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None) -> ConsoleRenderable:
        icon_str = str(self.icon) if self.icon else ""
        text_str = str(self.text) if self.text else "Unnamed Option"
        display_text = f"{icon_str} {text_str}" if icon_str else text_str

        if self.selected:
            self.style = "bold #50FA7B"
            prefix = "❱ "
            return Panel(
                Align.left(f"[{self.style}]{prefix}{display_text}[/{self.style}]"),
                border_style=self.style,
                expand=False,
                padding=(0,1)
            )
        else:
            self.style = "dim #F8F8F2"
            prefix = "  "
            return Padding(Align.left(f"[{self.style}]{prefix}{display_text}[/{self.style}]"), (0, 1, 0, 1 + len("❱ ")))


def menu_items_list(core_instance: Core) -> List[MenuOption]:
    options = [
        MenuOption(icon="󰐊", text="Continue", description="Resume your last saved game.", func=lambda: core_instance._transition_layout("INGAME"), type="menu"),
        MenuOption(icon="", text="New game", description="Start a fresh journey.", func=lambda: core_instance._transition_layout("NEWGAME"), type="menu"),
        MenuOption(icon="", text="Settings", description="Adjust game settings.", func=lambda: core_instance._transition_layout("SETTINGS"), type="menu"),
        MenuOption(icon="", text="About us", description="Learn about the creators.", func=lambda: core_instance._transition_layout("ABOUTUS"), type="menu"),
        MenuOption(icon="", text="Leave", description="Exit the game.", func=lambda: core_instance.TERMINATE(), type="menu"),
    ]
    return options

if __name__ == "__main__":
    game_core = Core()
    game_core.menu_options = menu_items_list(game_core)

    with Live(game_core.update_layout(), console=game_core.console, refresh_per_second=10, screen=True, transient=True) as live:
        action_triggered_for_new_game_demo = False
        try:
            while True:
                current_option_obj = game_core.menu_options[game_core.current_selection]
                should_call_func = False
                is_terminate_action = False

                # Determine if a function should be called for demo purposes
                if not action_triggered_for_new_game_demo and current_option_obj.text == "New game":
                    should_call_func = True
                    action_triggered_for_new_game_demo = True # Mark "New game" demo action as done
                elif current_option_obj.text == "Leave": # Always trigger "Leave" when selected
                    should_call_func = True
                    is_terminate_action = True

                if should_call_func and current_option_obj.func:
                    action_description = current_option_obj.text
                    spinner_message_text = f"Processing '{action_description}'..."
                    if is_terminate_action:
                        spinner_message_text = "Shutting down..."

                    # Set and display spinner in the status_bar
                    game_core.active_status = Group(Spinner("dots", style="medium_purple2"), Text(f" {spinner_message_text}", style="medium_purple2"))
                    live.update(game_core.update_layout())
                    time.sleep(0.05) # Brief pause to ensure spinner renders before blocking func

                    current_option_obj.func() # Execute the function (it might sleep or raise KeyboardInterrupt)

                    # If func completed (wasn't TERMINATE that raised KI)
                    if not is_terminate_action:
                        game_core.active_status = Text(f"Action '{action_description}' completed.", style="bold spring_green2")
                        live.update(game_core.update_layout())
                        time.sleep(1.0) # Show completion message
                        game_core.active_status = None # Clear status for next cycle
                        live.update(game_core.update_layout()) # Explicitly update to clear
                else:
                    # Default update if no function was called in this iteration
                    live.update(game_core.update_layout())

                # Cycle selection (if not terminated)
                time.sleep(1.5)
                game_core.current_selection = (game_core.current_selection + 1) % len(game_core.menu_options)

        except KeyboardInterrupt:
            # This catches Ctrl+C or the KI from core.TERMINATE()
            # active_status might still be the spinner if TERMINATE was called.
            # The prints from TERMINATE itself would have appeared on the console.
            if game_core.active_status:
                 final_status_message = Text.assemble(game_core.active_status, Text(" -> Interrupted.", style="bold red"))
                 game_core.console.print(Align.center(final_status_message)) # Print to console buffer

            game_core.active_status = None # Clear status before final message
            live.console.print(Align.center("\n[bold red]Exiting menu demo (Keyboard Interrupt).[/bold red]"))
            time.sleep(0.1) # Allow Rich to render final messages
        finally:
            game_core.active_status = None # Ensure status is cleared
            # Live display stops automatically on exiting the 'with' block
            # screen=True and transient=True handle cleanup.
            pass