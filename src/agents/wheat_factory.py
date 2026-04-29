import mesa
import numpy as np
from .wheat import Wheat


class WheatFactory(mesa.Agent):
    def __init__(self, model: mesa.Model, food_amount: int = 4, frequency: int = 10, food_lifetime: int = 350):
        """Class responsible for creating food for Pheasants."""
        super().__init__(model.next_id(), model)
        self.food_amount: int = food_amount
        self.iteration = 0
        self.frequency = frequency
        self.model.scheduler.add(self)
        self.food_lifetime = food_lifetime

    def step(self) -> None:
        """Create number of food in given frequency."""
        self.iteration += 1
        if self.iteration == self.frequency:
            self.iteration = 0
            for _ in range(self.food_amount):
                # w losowym miejscu rosnie pszenica z okreslona zainicjowana dlugoscia zycia
                x = self.model.random.randrange(self.model.width)
                y = self.model.random.randrange(self.model.height)
                Wheat.create(self.model, (x,y), self.food_lifetime)