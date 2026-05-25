from typing import Tuple
import mesa
from importlib import import_module
from random import randint

class PheasantHabitat(mesa.Agent):
    """Class representing pheasant habitat area for reproduction of pheasants. It creates new pheasants every mating season and is responsible for their initial placement on the grid."""
    def __init__(self, model: mesa.Model, mating_season:int, mating_range: Tuple[int, int]) -> None:
        super().__init__(model.next_id(), model)
        self.initial_mating_season = mating_season
        self.next_mating_season = mating_season
        self.mating_range = mating_range

    def create_animals(self) -> None:
        """Function called manually after the agent is created."""
        pheasant = import_module("src.agents.pheasant")
        pheasant_count = sum(1 for a in self.model.scheduler.agents if isinstance(a, pheasant.Pheasant)) # okolo polowa populacji do samice ale to 20-40% bedzie sie rozmnazac
        random_factor = randint(20,50)
        mating_pheasants = (pheasant_count * random_factor) // 100
        
        # Nawet jeśli procent z małej populacji wychodzi 0, wymuszamy 1 rozmnazajacego sie jesli sa chociaz 2 bazanty
        if pheasant_count >= 2 and mating_pheasants == 0:
            mating_pheasants = 1
            
        if mating_pheasants > 0:
            total_pheasants_to_create = 0
            for _ in range(mating_pheasants):
                total_pheasants_to_create += randint(self.mating_range[0], self.mating_range[1])
            self.model.num_of_pheasants += total_pheasants_to_create
            for _ in range(total_pheasants_to_create):
                pheasant.Pheasant.create(self.model, self)

    @staticmethod
    def create(model: mesa.Model) -> 'PheasantHabitat':
        habitat = PheasantHabitat(model, **model.pheasant_habitat_params)
        mw = model.width
        mh = model.height
        model.grid.place_agent(habitat, (3*mw//4, 3*mh//4))  # umieszczamy w prawym dolnym rogu, zeby byl daleko od lisow
        model.scheduler.add(habitat)
        return habitat
            
    def step(self) -> None:
        if self.next_mating_season == 0:
            self.next_mating_season = self.initial_mating_season
            self.create_animals()
        else:
            self.next_mating_season -= 1
