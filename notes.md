tick = one discrete time step in the simulation ( equivalent to 1 frame)


Pheasant: Uses get_neighbors() → returns agent objects
Pheromone: Uses get_neighborhood() → returns cell positions

Sound:
edge=True  Is on the outer edge, spawn perpendiculars to expand the wave"
edge=False  Is already interior, just keep moving forward"


Model
multigrid - pozwalamy na wiele agentów na jednym polu, bo musza się zjadać

```
def step(self):
        self.scheduler.step()

    def run_model(self):
        for _ in range(self.iterations):
            self.step()
```
metoda step powoduje że na każdy agencie również wykonuje się metoda step

Przykład użycia:
```
python3 main.py
```
Żeby uruchomić określoną ilość iteracji

Do zaimplementowania:
System energii
Mechanizm umierania