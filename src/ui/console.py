'''Handle displaying and printing on screen'''
from rich.table import Table
from rich.padding import Padding
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich import box
from rich.console import Group, group
from rich.spinner import Spinner
from ui.options import Option

class Console:
    """
    A class to represent the console user interface.
    Attributes
    ----------
    core : object
        The core object that contains the main logic and data of the application.
    layout : None
        Placeholder for the layout of the console.
    table : None
        Placeholder for the table to be displayed in the console.
    Methods
    -------
    refresh():
        Refreshes the console display with updated content.
    build_table():
        Builds and returns a table with the current options.
    get_renderable(option, style, left_padding):
        Returns a renderable object based on the option type.
    """
        """
        Constructs all the necessary attributes for the Console object.
        Parameters
        ----------
        core : object
            The core object that contains the main logic and data of the application.
        """
        """
        Refreshes the console display with updated content.
        """
        """
        Builds and returns a table with the current options.
        Returns
        -------
        Table
            A table object populated with the current options.
        """
        """
        Returns a renderable object based on the option type.
        Parameters
        ----------
        option : object
            The option object containing the details to be rendered.
        style : str
            The style to be applied to the renderable object.
        left_padding : int
            The amount of left padding to be applied to the renderable object.
        Returns
        -------
        Renderable
            A renderable object based on the option type.
        """
    def __init__(self, core):
        self.core = core
        self.layout = None
        self.table = None
        

    def refresh(self):
        table = self.build_table()
        content = Group(
            Align(align='center', renderable=Spinner("toggle")),
            Padding(table, pad=(0, 0, 0, 0))
        )
        self.core.interface['main'].update(content)
        self.core.love.update(self.core.interface)

    def build_table(self):
        core = self.core
        self.table = Table(
            expand=True, caption=" -", show_edge=False, show_header=False,
            style='bold red1', box=box.ROUNDED
        )
        self.table.add_column(justify="center")

        options = core.options[:9] if len(core.options) > 9 else core.options
        selectable_options = [option for option in options if option.selectable]

        if all(not option.selected for option in selectable_options):
            if options:
                core.selected_option = 0
                if selectable_options:
                    selectable_options[0].selected = True

        for option in options:
            style = "none"
            left_padding = 0

            if option.selected:
                if option.preview:
                    option.preview()
                style = "bold green"
                left_padding += 5

            renderable = self.get_renderable(option, style, left_padding)
            self.table.add_row(Align(renderable, align="left"))

        return self.table

    def get_renderable(self, option, style, left_padding):
        if option.type == 'header':
            return _dialogue_text(option.text, style)
        elif option.type == "entity_profile":
            return get_player_display(option)
        else:
            return _option_button(option.text, style, left_padding=left_padding)

@group()
def get_player_display(option):
    yield _dialogue_text(option.text, 'none')
    yield Rule(style='bold red')

def _dialogue_text(text, style):
    return Padding(text, pad=(2, 0, 0, 0))

def _option_button(text, style, top_padding=0, right_padding=0, bottom_padding=0, left_padding=0):
    return Padding(
        Panel(text, width=20, border_style=style),
        pad=(top_padding, right_padding, bottom_padding, left_padding)
    )

def _display_player_weapons(player):
    pass

def _display_alternative():
    pass

def show_player_actions(player):
    _display_player_weapons(player)
    _display_alternative()
