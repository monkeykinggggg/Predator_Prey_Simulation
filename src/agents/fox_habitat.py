from typing import Tuple
import mesa
from importlib import import_module
from random import randint

class FoxHabitat(mesa.Agent):
    """Class representing fox habitat area for reproduction of foxes. It creates new foxes every mating season and is responsible for their initial placement on the grid."""
    def __init__(self, model: mesa.Model, mating_season:int, mating_range: Tuple[int, int]) -> None:
        super().__init__(model.next_id(), model)
        self.initial_mating_season = mating_season
        self.next_mating_season = mating_season    # ile jeszcze krokow trzeba czekac do nastepnego sezonu rozrodczego
        self.mating_range = mating_range        # ile mlodych lisow moze sie urodzic w sezonie rozrodczym (losowana liczba z tego zakresu)

    def create_animals(self) -> None:
        """Function called manually after the agent is created."""
        fox = import_module("src.agents.fox")
        fox_count = sum(1 for a in self.model.scheduler.agents if isinstance(a, fox.Fox)) # okolo polowa populacji do samice ale mimo wszystko tylko 20-40% calej populacji sie rozmnaza
        random_factor = randint(20,50)
        mating_foxes = fox_count * random_factor // 100
        
        # Nawet jeśli procent z małej populacji (np. 2 lisy * 40%) wynosi 0, chcemy, żeby przynajmniej 1 para się rozmnożyła, jeśli są min. 2 lisy
        if fox_count >= 2 and mating_foxes == 0:
            mating_foxes = 1
            
        if mating_foxes > 0:
            total_foxes_to_create = 0
            for _ in range(mating_foxes):
                total_foxes_to_create += randint(self.mating_range[0], self.mating_range[1])
            self.model.num_of_foxes += total_foxes_to_create
            for _ in range(total_foxes_to_create):
                fox.Fox.create(self.model, self)

    @staticmethod
    def create(model: mesa.Model) -> 'FoxHabitat':
        habitat = FoxHabitat(model, **model.fox_habitat_params)
        model.grid.place_agent(habitat, (model.width//4,model.height//4))  # umieszczamy w lewym gornym rogu, zeby byl daleko od bażantów
        model.scheduler.add(habitat)
        return habitat
            
    def step(self) -> None:
        if self.next_mating_season == 0:
            self.next_mating_season = self.initial_mating_season
            self.create_animals()
        else:
            self.next_mating_season -= 1
