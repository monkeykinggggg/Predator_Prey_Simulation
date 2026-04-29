from typing import Any
import mesa
from .agents import *
from .agents.fox_habitat import FoxHabitat
from .agents.pheasant_habitat import PheasantHabitat
from .agents.wheat_factory import WheatFactory

class SimulationModel(mesa.Model):
    """Model simulating the interaction between foxes and pheasants in a grid environment."""

    def __init__(self, 
                initial_wheat:int,
                initial_fox:int,
                initial_pheasant:int,
                
                fox_lifetime: int,
                fox_consumption: int,
                fox_mating_season: int,
                fox_mating_range: int,
                
                pheasant_lifetime: int,
                pheasant_consumption: int,
                pheasant_mating_season: int,
                pheasant_mating_range: int,

                food_frequency: int,
                food_lifetime: int,
                
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
            "lifetime": pheasant_lifetime,
            "consumption": pheasant_consumption,
        }
        self.fox_habitat_params={
            "mating_season": fox_mating_season,
            "mating_range": (1, fox_mating_range)
        }
        self.pheasant_habitat_params={
            "mating_season": pheasant_mating_season,
            "mating_range": (1, pheasant_mating_range)
        }
        self.food_factory_params={
            "food_frequency": food_frequency,
            "food_lifetime": food_lifetime
        }
        


        self.scheduler = mesa.time.BaseScheduler(self)
        
        # Create fox habitat first so it exists when baby foxes reference it
        self.fox_habitat = FoxHabitat.create(self)
        
        # Create pheasant habitat at different location
        self.pheasant_habitat = PheasantHabitat.create(self)
        while self.pheasant_habitat.pos == self.fox_habitat.pos:
            # If they spawned at same location, move pheasant habitat
            self.grid.remove_agent(self.pheasant_habitat)
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(self.pheasant_habitat, (x, y))

        WheatFactory(self, frequency=self.food_factory_params["food_frequency"], food_lifetime=self.food_factory_params["food_lifetime"])

        for _ in range(self.num_of_foxes):
            fox = Fox(self, lifetime=self.fox_params["lifetime"], consumption=self.fox_params["consumption"])
            self.scheduler.add(fox)

            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(fox, (x, y))

        for _ in range(self.num_of_pheasants):
            pheasant = Pheasant(self, lifetime=self.pheasant_params["lifetime"], consumption=self.pheasant_params["consumption"])
            self.scheduler.add(pheasant)

            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(pheasant, (x, y))

        for _ in range(self.num_of_wheat):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            Wheat.create(self, (x, y), food_lifetime=self.food_factory_params["food_lifetime"])
            
        self.running = True

    def step(self):
        self.scheduler.step()

    def run_model(self):
        for _ in range(self.iterations):
            self.step()