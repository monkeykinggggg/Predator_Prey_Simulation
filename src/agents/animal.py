from abc import ABC, abstractmethod 
import mesa


class Animal(mesa.Agent, ABC):
    """Animal interface"""

    def __init__(
        self,
        model: mesa.Model,
        lifetime: int,
        consumption: int,
        speed: int,
        trace: int,
        noticing_range: int = None
    ):
        super().__init__(model.next_id(), model)
        self.lifetime = lifetime    
        self.consumption = consumption  
        self.speed = speed  
        self.trace = trace  
        self.noticing_range = noticing_range


    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.pos}"

    @abstractmethod
    def step(self) -> None:
        """
        An Animal step. Any kind of behaviour.
        """
        pass

    def random_move(self) -> None:
        """
        Step one cell in any allowable direction form Moore neighberhood.
        """
        # True means that the agent can move diagonally
        next_moves = self.model.grid.get_neighborhood(self.pos, True)
        next_move = self.random.choice(next_moves)
        self.model.grid.move_agent(self, next_move)
    
    def remove(self) -> None:
        """
        Remove the animal from the grid and the scheduler.
        """
        self.model.grid.remove_agent(self)
        self.model.scheduler.remove(self)