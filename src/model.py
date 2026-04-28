from typing import Any
import mesa
from .agents import *
from .agents.fox_habitat import FoxHabitat

class SimulationModel(mesa.Model):
    """Model simulating the interaction between foxes and pheasants in a grid environment."""

    def __init__(self, 
                initial_wheat:int,
                initial_fox:int,
                initial_pheasant:int,
                fox_sound_force: int,
                
                fox_lifetime: int,
                fox_consumption: int,
                fox_mating_season: int,
                fox_mating_range: int,
                
                iterations: int = 100,
                *args: Any,
                **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.width = 20
        self.height = 20
        self.grid = mesa.space.MultiGrid(self.width, self.height, False)

        self.iterations = iterations

        self.num_of_pheasants = initial_pheasant
        self.num_of_foxes = initial_fox
        self.num_of_wheat = initial_wheat
        self.fox_params={
            "lifetime": fox_lifetime,
            "consumption": fox_consumption,
            
        }
        self.pheasant_params={
            "lifetime": 3,
            "consumption": 1,
        }
        self.fox_habitat_params={
            "mating_season": fox_mating_season,
            "mating_range": (1, fox_mating_range)
        }
        


        self.scheduler = mesa.time.BaseScheduler(self)
        
        # Create habitat first so it exists when baby foxes reference it
        self.fox_habitat = FoxHabitat.create(self)

        for _ in range(self.num_of_foxes):
            fox = Fox(self, lifetime=self.fox_params["lifetime"], consumption=self.fox_params["consumption"])
            self.scheduler.add(fox)

            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(fox, (x, y))

        for _ in range(self.num_of_pheasants):
            pheasant = Pheasant(self)
            self.scheduler.add(pheasant)

            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(pheasant, (x, y))

        self.running = True

    def step(self):
        self.scheduler.step()

    def run_model(self):
        for _ in range(self.iterations):
            self.step()