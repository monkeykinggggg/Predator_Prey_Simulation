from typing import Tuple
import mesa
from importlib import import_module
from random import randint

class PheasantHabitat(mesa.Agent):
    """Class representing fox habitat area for reproduction of foxes. It creates new foxes every mating season and is responsible for their initial placement on the grid."""
    def __init__(self, model: mesa.Model, mating_season:int = 30, mating_range: Tuple[int, int] = (1,5)) -> None:
        super().__init__(model.next_id(), model)
        self.initial_mating_season = mating_season
        self.next_mating_season = mating_season
        self.mating_range = mating_range

    def create_animals(self) -> None:
        """Function called manually after the agent is created."""
        fox = import_module("src.agents.fox")
        number_of_foxes_to_create = randint(self.mating_range[0], self.mating_range[1])
        self.model.num_of_foxes += number_of_foxes_to_create
        for _ in range(number_of_foxes_to_create):
            fox.Fox.create(self.model, self)

    @staticmethod
    def create(model: mesa.Model) -> 'FoxHabitat':
        habitat = FoxHabitat(model, **model.fox_habitat_params)
        x = model.random.randrange(model.width)
        y = model.random.randrange(model.height)
        model.grid.place_agent(habitat, (x,y))
        model.scheduler.add(habitat)
        return habitat
            
    def step(self) -> None:
        if self.next_mating_season == 0:
            self.next_mating_season = self.initial_mating_season
            self.create_animals()
        else:
            self.next_mating_season -= 1
