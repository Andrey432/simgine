from engine.api.objects import DataObject


class Spawner(DataObject):
    def __init__(self, obj_prefab=None):
        super().__init__()

    def update(self, timedelta: float) -> None:
        events = self.engine.gui_events()
        print(events)
