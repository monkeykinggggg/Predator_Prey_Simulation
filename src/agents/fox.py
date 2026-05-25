import mesa
import importlib
import numpy as np
from typing import Tuple
from enum import Enum
from .animal import Animal
from .sound import Sound, Direction
from .pheromone import Pheromone
from random import choice
from .fox_habitat import FoxHabitat


class State(Enum):
    SNEAKING = 1
    WALKING = 2
    SPRINTING = 3

class Fox(Animal):

    def __init__(self,
                 model,
                 lifetime=4,    # how many steps the fox can live with current energy
                 consumption=1, # how many units of energy are needed per step
                 speed=2,       # 2 grids per model step
                 trace=2,       # how many steps the fox leaves the sound trace
                 smelling_range=5,   # grids in which the fox can smell pheasants pheromones
                 sneak_speed=1,   # speed when the fox is sneaking
                 sprint_speed=3   # speed when the fox is sprinting
                 ):
        super().__init__(model, lifetime, consumption, speed, trace, smelling_range)
        self.smelling_range = self.noticing_range
        self.attack_range = 1
        self.view_range = 5
        self.sneak_speed = sneak_speed
        self.sprint_speed = sprint_speed
        
        self.state = State.WALKING
        self.hunting = False
        self.focused_prey = None

    @staticmethod
    def create(model: mesa.Model, home: FoxHabitat):
        """Create a new fox near habitat location."""
        fox = Fox(model, **model.fox_params)
        # Spawn near habitat with small random offset
        x = home.pos[0] + model.random.randrange(-1, 2)
        y = home.pos[1] + model.random.randrange(-1, 2)
        # Keep within grid bounds
        x = max(0, min(model.width - 1, x))
        y = max(0, min(model.height - 1, y))
        model.grid.place_agent(fox, (x, y))
        model.scheduler.add(fox)
        
    def smell(self) -> dict:
        """Smell pheromones in smelling range"""
        neighbors = self.model.grid.get_neighbors(self.pos,moore=True,include_center=False,radius=self.smelling_range)
        smell = {neighbor.pos: neighbor.value for neighbor in neighbors if type(neighbor) is Pheromone}
        return smell

    def kill(self) -> None:
        """Kills focused pheasant."""
        phsnt = importlib.import_module("src.agents.pheasant")
        pheasants_here = [agent for agent in self.model.grid[self.pos] if type(agent) is phsnt.Pheasant]
        if len(pheasants_here)>0:
            for pheasant in pheasants_here:
                pheasant.remove()
                self.lifetime += self.consumption * 20      # uwaga! dodajemy 20 jednostek podstawowej energii
            self.focused_prey = None
            self.hunting = False    # przestajemy polowac aktualnie
    
    
    def go_in_direction(self, direction: Tuple[int, int]) -> None:
        """Moves fox in specified direction."""
        match self.state:
            case State.SPRINTING:
                speed = self.sprint_speed
            case State.SNEAKING:
                speed = self.sneak_speed
            case _:
                speed = self.speed

        dx = direction[0] - self.pos[0]
        dy = direction[1] - self.pos[1]
        direction = np.array([dx, dy], dtype=float)
        direction /= np.linalg.norm(direction)
        if direction[1] > np.sin(22.5 / 180):
            dy = min(dy, speed)
        elif direction[1] < -np.sin(22.5 / 180):
            dy = max(dy, -speed)
        else:
            dy = 0

        if direction[0] > np.cos(67.5 / 180):
            dx = min(dx, speed)
        elif direction[0] < -np.cos(67.5 / 180):
            dx = max(dx, -speed)
        else:
            dx = 0

        self.model.grid.move_agent(self, (self.pos[0] + dx, self.pos[1] + dy))
        self.kill()
        
            
    def get_pheasants_in_specific_range(self, search_range: int) -> list:
        """Returns list of pheasants in specified range."""
        phsnt = importlib.import_module("src.agents.pheasant")
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=search_range)
        pheasants = [agent for agent in neighbors if type(agent) is phsnt.Pheasant]
        return pheasants
    
    def hunt(self) -> None:
        """Moves fox according to his surroundings."""
        if self.focused_prey and self.focused_prey.pos:
            dist = max(abs(self.pos[0]-self.focused_prey.pos[0]), abs(self.pos[1]-self.focused_prey.pos[1]))
            if dist <= self.view_range:
                if dist <= self.attack_range:
                    self.state = State.SPRINTING
                else:
                    self.state = State.SNEAKING
                self.go_in_direction(self.focused_prey.pos)
                return
            # czuje ale nie widzi bazanta, wiec usuwamy go z celownika
            self.focused_prey = None    # stracilismy z oczu bazanta
        else:   # moze nie mamy zadnego sfocusowanego, ale w zasiegu wzroku jest inny niesfocusowany bazant
            pheasants_to_attack = self.get_pheasants_in_specific_range(self.attack_range)
            pheasants_to_sneak = self.get_pheasants_in_specific_range(self.view_range)
            if pheasants_to_attack:
                self.focused_prey = choice(pheasants_to_attack)
                self.state = State.SPRINTING
                self.go_in_direction(self.focused_prey.pos)
                return

            if pheasants_to_sneak:
                self.focused_prey = choice(pheasants_to_sneak)
                self.state = State.SNEAKING
                self.go_in_direction(self.focused_prey.pos)
                return

        self.state = State.WALKING
        smell = self.smell()    # ogolnie podazamy za zapachami 
        if smell:
            heuristic = max(smell, key=smell.get)
            self.go_in_direction(heuristic)
        else:
            self.random_move()


    def make_noise(self):
        """Creates noise around current position."""
        force = self.trace
        match self.state:
            case State.SNEAKING:    # if it's sneaking it makes smalles noice then when walking or sprinting
                force = 1
            case State.SPRINTING:
                force = 20
            case _:
                pass
        for ngh in self.model.grid.get_neighborhood(self.pos, moore=True):
            dx = (ngh[0] > self.pos[0]) - (ngh[0] < self.pos[0])
            dy = (ngh[1] < self.pos[1]) - (ngh[1] > self.pos[1])
            Sound.create_sound(self.model, ngh, 1, Direction.get((dx, dy)), True, force)    

    def should_die(self) -> bool:
        """Check if the fox should die due to old age or starvation."""
        energy_cost = self.consumption
        match self.state:
            case State.SPRINTING:
                energy_cost *= 3  # Running costs 3x more
            case State.SNEAKING:
                energy_cost *= 1.5  # Careful movement costs 1.5x
        self.lifetime -= energy_cost    # energy cost on each step
        # print(f'lifetime{self.lifetime}')
        return self.lifetime <= 0
    
    def step(self) -> None:
        """Fox step. It can hunt or move randomly."""
        if self.should_die():   # dying bc out of energy
            self.remove()
            return
        self.hunt()
        # print(f'state{self.state}')
        self.make_noise()   # but always makes noise when moves