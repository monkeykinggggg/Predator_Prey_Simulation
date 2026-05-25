import mesa
import numpy as np
from .wheat import Wheat


class WheatFactory(mesa.Agent):
    def __init__(self, model: mesa.Model, food_amount: tuple[int, int], frequency: int, food_lifetime: int):
        """Class responsible for creating food for Pheasants."""
        super().__init__(model.next_id(), model)
        self.food_amount: tuple[int, int] = food_amount
        self.iteration = 0
        self.frequency = frequency
        self.model.scheduler.add(self)
        self.food_lifetime = food_lifetime

    def step(self) -> None:
        """Create number of food in given frequency."""
        self.iteration += 1
        if self.iteration == self.frequency:
            self.iteration = 0
            wheat_count = sum(1 for a in self.model.scheduler.agents if isinstance(a, Wheat))//2 # okolo polowa populacji do damskie osobniki
            if wheat_count > 0:
                total_new_wheat = self.model.random.randint(self.food_amount[0], self.food_amount[1]) * wheat_count
                for _ in range(total_new_wheat):
                    # w losowym miejscu rosnie pszenica z okreslona zainicjowana dlugoscia zycia
                    x = self.model.random.randrange(self.model.width)
                    y = self.model.random.randrange(self.model.height)
                    Wheat.create(self.model, (x,y), self.food_lifetime)