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
        portrayal["Layer"] = 2
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Fox:
        portrayal["Shape"] = 'src/resources/fox.png'
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
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
        portrayal["Layer"] = 1
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
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1
    
    elif type(agent) is Wheat and not agent.eaten:
        portrayal["Shape"] = "src/resources/wheat.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal

canvas_element = mesa.visualization.CanvasGrid(fox_pheasant_portrayal, 80, 80, 880, 880)

class SpacerElement(mesa.visualization.TextElement):
    def render(self, model):
        return "<div style='height: 40px;'></div>"

spacer = SpacerElement()

chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Lisy", "Color": "#CF296B"},
        {"Label": "Bażanty", "Color": "#FFD700"},
        {"Label": "Pszenica", "Color": "#134F13"}
    ]
)

model_params = {
    "title": "Simulation Parameters",
    "initial_fox": mesa.visualization.NumberInput("Inicjalizacyjna Populacja lisów", value=4),
    "initial_pheasant": mesa.visualization.NumberInput("Inicjalizacyjna Populacja bażantów", value=4),
    "initial_wheat": mesa.visualization.NumberInput("Inicjalizacyjna Populacja pszenicy", value=5),

    "year_unit": mesa.visualization.NumberInput(
        "Jednostka roku<br><small>(wykorzystywana do długości życia zwierząt oraz okresów rozrodczych)</small>", 
        value=5
    ),
    "base_consumption_unit": mesa.visualization.NumberInput(
        "Jednostka zużycia energii<br><small>(wykorzystywana do metabolizmu)</small>", 
        value=0.25
    ),
}

server = mesa.visualization.ModularServer(
    SimulationModel,
    visualization_elements=[canvas_element, spacer, chart_element],
    name="Pheasant Fox Simulation",
    model_params=model_params,
    port=8888
)