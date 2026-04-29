from typing import Tuple
import mesa

class Wheat(mesa.Agent):
    def __init__(self, model: mesa.Model, lifetime:int = 350) -> None:
        """Class responsible for feeding Pheasants."""
        super().__init__(model.next_id(), model)
        self.lifetime: int = lifetime
        self.eaten: bool = False

    def step(self) -> None:
        """Performs a single of agent."""
        if self.lifetime <= 0 or self.eaten:
            self.model.grid.remove_agent(self)
            self.model.scheduler.remove(self)
        else:
            self.lifetime -= 1  # standardowo zycie zmniejszamy o jeden

    def eat_food(self) -> None:
        """Changes the parameter eaten to True."""
        self.eaten = True

    @staticmethod
    def create(model: mesa.Model, pos: Tuple[int, int], food_lifetime: int) -> None:
        """Creates hare food. Used by food factory."""
        pheasants_food = Wheat(model, food_lifetime)
        model.grid.place_agent(pheasants_food, pos)
        model.scheduler.add(pheasants_food)