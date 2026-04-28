import mesa
from .agents import *
from .model import SimulationModel



def fox_pheasant_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Pheasant:
        portrayal["Shape"] = 'src/resources/pheasant.png'
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Fox:
        portrayal["Shape"] = 'src/resources/fox.png'
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Pheromone:
        value = max(0, min(1, agent.value))
        shades_of_yellow = [
            "#FFFF99",  
            "#FFD700",  
            "#FFFF00",  
            "#FFD700",  
            "#DAA520",  
            "#FFA500"   
        ]
        index = int(value * (len(shades_of_yellow) - 1))

        portrayal["Color"] = [shades_of_yellow[index]]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Sound:
        shades_of_pink = [
            "#CF296B",
            "#EB3B75",
            "#F06292",
            "#F48FB1",
            "#FCE4EC"
        ]
        portrayal["Color"] = [shades_of_pink[agent.r - 1]]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal

canvas_element = mesa.visualization.CanvasGrid(fox_pheasant_portrayal, 20, 20, 720, 720)

model_params = {
    "title": "Simulation Parameters",
    "iterations": 100,
    "initial_fox": mesa.visualization.NumberInput("Initial Fox Population", value=10),
    "initial_pheasant": mesa.visualization.NumberInput("Initial Pheasants Population", value=10),
    "initial_wheat": mesa.visualization.NumberInput("Initial Wheat Amount", value=10),
    
    "fox_lifetime": mesa.visualization.NumberInput("Fox Lifetime", value=4),
    "fox_consumption": mesa.visualization.NumberInput("Fox Consumption", value=1),
    "fox_sound_force": mesa.visualization.NumberInput("Initial Sound Force", value=10),
    "fox_mating_season": mesa.visualization.NumberInput("Fox Mating Season Duration", value=40),
    "fox_mating_range": mesa.visualization.NumberInput("Fox Mating Range", value=5),
    
    "initial_wheat_frequency": mesa.visualization.NumberInput("Initial Wheat Frequency", value=2),
    
}

server = mesa.visualization.ModularServer(
    SimulationModel,
    visualization_elements=[canvas_element],
    name="Pheasant Fox Simulation",
    model_params=model_params,
    port=8888
)