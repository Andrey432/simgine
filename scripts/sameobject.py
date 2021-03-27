from engine.api.objects import GameObject


class SameObject(GameObject):
    def __init__(self, health, hungry, thirst, energy, speed):
        super().__init__()

        self.health = health
        self.hungry = hungry
        self.thirst = thirst
        self.energy = energy
        self.speed = speed

    def update(self, timedelta: float) -> None:
        pass
