from .pheromone import Pheromone
from .animal import Animal

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