# Predator_Prey_Simulation
Wildlife simulation which aims to mimic real-world predator-prey scenarios where the environment is inhabited by pheasants, foxes, and wheat.

## Features & Mechanics
This model extends classical predator-prey dynamics with advanced grid-based spatial features:
- **Sensory Systems:** Foxes leave sound waves that propagate through the grid, while pheasants leave pheromone traces for predators to follow.
- **Dynamic States:** 
  - **Foxes** adapt their movement by `SNEAKING` when prey is near or `SPRINTING` to catch it.
  - **Pheasants** react to threats by freezing (`FROZEN`) or escaping (`SPRINTING`), which heavily impacts their metabolic energy drain.
- **Realistic Energy & Reproduction:** The simulation accounts for realistic lifespans, breeding seasons (dependent on population size), and energy consumption based on animal actions.

## How to run
You need to sync dependencies via the `uv` tool and run the mesa server:
```bash
uv sync
uv run mesa runserver
```
The simulation should be accessible on [http://localhost:8888](http://localhost:8888/). 
Set up the parameters in the sidebar (or leave defaults), press `Reset` to apply changes, and click the `Start` button to run the animation. You can also run the simulation step by step using the `Step` button.

## Configurable Parameters
- **Initial Populations:** Adjust the starting number of foxes, pheasants, and wheat.
- **Year Unit:** Controls how many frames constitute a single "year", directly scaling maximum lifespan limits and mating season frequency.