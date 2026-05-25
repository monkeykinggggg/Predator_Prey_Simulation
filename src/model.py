from typing import Any
import mesa
from .agents import *
from .agents.fox_habitat import FoxHabitat
from .agents.pheasant_habitat import PheasantHabitat
from .agents.wheat_factory import WheatFactory
from math import floor

class SimulationModel(mesa.Model):
    """Model simulating the interaction between foxes and pheasants in a grid environment."""

    def __init__(self, 
                initial_wheat:int,
                initial_fox:int,
                initial_pheasant:int,
                
                # liczba klatek ile trwa rok, zwierzeta proporcjonalnie maja ustawiana maksymalna dlugosc zycia oraz czestotliwość okresów godów i produkcji jedzenia na podstawie tej jednostki
                year_unit: int, 
                # podstawowa jednostka zuzycia energii, na podstawie ktorej ustawiana jest konsumpcja energii przez lisy i bażanty na zwyczajne egzystowanie(metabolizm), bez polowania, sprintow itd
                base_consumption_unit: int,
                
                # przedzial ile mlodych zwierzat moze sie urodzic w sezonie rozrodczym (losowana liczba z tego zakresu)
                fox_mating_range: tuple = (3,5), # 3-5 na osobnika
                pheasant_mating_range: tuple = (5,12), #  5-12 z samicy
                
                iterations: int = 100,
                *args: Any,
                **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.width = 80
        self.height = 80
        self.grid = mesa.space.MultiGrid(self.width, self.height, False)

        self.iterations = iterations

        self.num_of_pheasants = initial_pheasant
        self.num_of_foxes = initial_fox
        self.num_of_wheat = initial_wheat
        
        self.fox_params={
            "lifetime": year_unit * 5,
            "consumption": base_consumption_unit * 2,
            
        }
        self.pheasant_params={
            "lifetime": year_unit * 3,
            "consumption": base_consumption_unit * 1,
        }
        self.fox_habitat_params={
            "mating_season": year_unit * 1,
            "mating_range": (fox_mating_range[0], fox_mating_range[1])
        }
        self.pheasant_habitat_params={
            "mating_season": year_unit * 1,
            "mating_range": (pheasant_mating_range[0], pheasant_mating_range[1])
        }
        self.food_factory_params={
            "food_frequency": floor(year_unit * 0.8),
            "food_lifetime": floor(year_unit * 0.8),
            "food_amount": 1
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

        WheatFactory(self, frequency=self.food_factory_params["food_frequency"], food_lifetime=self.food_factory_params["food_lifetime"], food_amount=self.food_factory_params["food_amount"])

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
            
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Lisy": lambda m: sum(1 for agent in m.scheduler.agents if type(agent) is Fox),
                "Bażanty": lambda m: sum(1 for agent in m.scheduler.agents if type(agent) is Pheasant),
                "Pszenica": lambda m: sum(1 for agent in m.scheduler.agents if type(agent) is Wheat),
            }
        )
        self.running = True

    def step(self):
        self.datacollector.collect(self)
        self.scheduler.step()

    def run_model(self):
        for _ in range(self.iterations):
            self.step()