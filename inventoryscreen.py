from menuinterface import BasicScreen
from menuinterface import StorylineLabel

class InventoryScreen(BasicScreen):
    """Setup the screen for inventory."""

    def on_enter(self, *args):
        self.inventory_layout.add_widget(StorylineLabel(text='Inventory'))