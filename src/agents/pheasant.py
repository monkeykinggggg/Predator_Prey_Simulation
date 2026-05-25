from .pheromone import Pheromone
from .animal import Animal
import mesa
from enum import Enum
from .wheat import Wheat
from .sound import Sound
import numpy as np

distance = lambda p1, p2: np.linalg.norm(np.array(p1) - np.array(p2))

class PheasantStatus(Enum):
    NORMAL = 0
    SPRINTING = 1
    FROZEN = 2

class Pheasant(Animal):
    def __init__(self,
        model,
        lifetime=4,
        consumption=5,
        speed=6,
        trace=4,
        hearing_range=5,
        sprint_speed=8,
        sprint_duration=2,
        sprint_cool_down=2,
        sprint_distance=3,
        freeze_distance=3,
        freeze_duration=2
    ):
        super().__init__(model, lifetime, consumption, speed, trace, hearing_range)
        self.hearing_range = hearing_range
        self.view_range = 4
        self.sprint_speed = sprint_speed
        self.sprint_duration = sprint_duration
        self.sprint_cool_down = sprint_cool_down
        self.sprint_distance = sprint_distance
        self.freeze_distance = freeze_distance
        self.freeze_duration = freeze_duration
        self.status = PheasantStatus.NORMAL
        self.iteration = 0
        self.cool_down_iteration = 0

    @staticmethod
    def create(model: mesa.Model, home):
        """Create a new pheasant near habitat location."""
        pheasant = Pheasant(model, **model.pheasant_params)
        # Spawn near habitat with small random offset
        x = home.pos[0] + model.random.randrange(-1, 2)
        y = home.pos[1] + model.random.randrange(-1, 2)
        # Keep within grid bounds
        x = max(0, min(model.width - 1, x))
        y = max(0, min(model.height - 1, y))
        model.grid.place_agent(pheasant, (x, y))
        model.scheduler.add(pheasant)


    def eat_food(self) -> None:
        """Eat food at current position."""
        agents_at_pos = self.model.grid[self.pos]
        wheat_here = [agent for agent in agents_at_pos if type(agent) is Wheat and not agent.eaten]
        if wheat_here:
            food = wheat_here[0]
            food.eat_food()
            self.lifetime += self.consumption * 10  # dodajemy energii 10 krotnosc podstawowej energii
    
    def listen(self) -> dict:
        """Listen to the sound in the hearing range."""
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=self.hearing_range)
        sound = {neighbor.pos: neighbor.force for neighbor in neighbors if type(neighbor) is Sound}
        return sound
    
    def check_threats(self) -> float:
        """Check if there are any foxes nearby and return closest distance."""
        from .fox import Fox
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=self.view_range)
        threats = [distance(neighbor.pos, self.pos) for neighbor in neighbors if type(neighbor) is Fox]
        return 0 if len(threats) < 1 else min(threats)
    
    def escape_movement(self) -> tuple:
        """Find safest direction away from sound/threats."""
        sound = self.listen()
        current_speed = self.sprint_speed if self.status == PheasantStatus.SPRINTING else self.speed
        
        next_moves = self.model.grid.get_neighborhood(self.pos, moore=True, radius=current_speed)
        
        # Find moves with least sound
        sound_values = [sound.get(move, 0) for move in next_moves]
        if sound_values:
            min_sound = min(sound_values)
            next_moves = [move for move in next_moves if sound.get(move, 0) == min_sound]
        
        return self.random.choice(next_moves) if next_moves else self.random_move()
    
    def leave_trace(self) -> None:
        """
        Leave a trace of pheromone/trace for fox.
        """
        neighbors = self.model.grid.get_neighbors(self.pos, False, True, 0) # not include center, include diagonals, radius 0
        neighbors = [neighbor for neighbor in neighbors if type(neighbor) is Pheromone]

        if len(neighbors) == 0:
            Pheromone.create(self.model, self.pos, self.trace)  # create a new pheromone at the curr pos if no present
        else:
            pheromone = neighbors[0]    # updating the first one pheromone, refreshing the scent
            pheromone.value = self.trace    # initial weight value of the pheromone

    def step(self) -> None:
        if self.lifetime <= 0:
            self.remove()
            return
        
        energy_cost = self.consumption
        if self.status == PheasantStatus.SPRINTING:
            energy_cost *= 4
        elif self.status == PheasantStatus.FROZEN:
            energy_cost *= 0.5
            
        self.lifetime -= energy_cost
        threats = self.check_threats()
        
        match self.status:
            # Too close threat: freeze and don't move
            case PheasantStatus.FROZEN if threats > self.sprint_distance and self.cool_down_iteration == 0:
                self.iteration = 1
                self.status = PheasantStatus.SPRINTING
                pos = self.escape_movement()
                self.model.grid.move_agent(self, pos)
            
            case PheasantStatus.FROZEN if self.iteration < self.freeze_duration:
                self.iteration += 1
            
            case PheasantStatus.FROZEN:
                self.status = PheasantStatus.NORMAL
                self.model.grid.move_agent(self, self.escape_movement())
            
            # Close threat: start sprinting
            case PheasantStatus.NORMAL if self.cool_down_iteration == 0 and 0 < threats < self.sprint_distance:
                self.iteration = 1
                self.status = PheasantStatus.SPRINTING
                pos = self.escape_movement()
                self.model.grid.move_agent(self, pos)
            
            # Distant threat: freeze
            case PheasantStatus.NORMAL if threats > self.freeze_distance:
                self.iteration = 1
                self.status = PheasantStatus.FROZEN
            
            # Normal: eat and explore
            case PheasantStatus.NORMAL:
                self.eat_food()
                self.random_move()
            
            # Sprinting: keep running
            case PheasantStatus.SPRINTING if self.iteration < self.sprint_duration:
                self.iteration += 1
                pos = self.escape_movement()
                self.model.grid.move_agent(self, pos)
            
            # Sprint finished: cooldown
            case PheasantStatus.SPRINTING:
                self.status = PheasantStatus.NORMAL
                self.cool_down_iteration = self.sprint_cool_down
                pos = self.escape_movement()
                self.model.grid.move_agent(self, pos)
        
        # Decrease cooldown
        if self.cool_down_iteration > 0:
            self.cool_down_iteration -= 1
        
        self.leave_trace()