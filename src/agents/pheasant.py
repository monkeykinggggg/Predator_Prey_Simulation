from .pheromone import Pheromone
from .animal import Animal
import mesa
from enum import Enum

class PheasantStatus(Enum):
    NORMAL = 0
    SPRINTING = 1
    NO_MOVEMENT = 2

class Pheasant(Animal):
    def __init__(self,
        model,
        lifetime=4,
        consumption=5,
        speed=6,
        trace=4,
        view_range=350
    ):
        super().__init__(model, lifetime, consumption, speed, trace, view_range)

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
        self.random_move()
        self.leave_trace()