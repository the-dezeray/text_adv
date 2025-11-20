from ui.options import CustomRenderable
class dada(CustomRenderable):
    def __init__(self, text: str, selected: bool = False):
        super().__init__(text, selected)
        self.text = text
        self.selected = selected