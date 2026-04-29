# Predator_Prey_Simulation

Parametry agentów: (zwierzęta)
lifetime: int - długość życia (ile ticków)
consumption: int - energia potrzebna na jedna klatkę
speed: int - prędkość z jakim porusza się dany osobnik (będzie tutaj podział na gatunek)
**trace**: int - intensywność feromonów/odgłosów (bażant słyszy lisa a lis wyczuwa bażanta)
view_range: int - szerokość widoczności


Zapach:
value = trace od zwierzęcia
evaporation_rate
diffusion_rate
Najpierw 40% wyparowywuje, potem nastepuje dyfucja z feromonowami sąsiadów, czyli wzmacniamy przy skupisku bażantów.

Dżwięk:
Klasa przedstawiająca fale dźwiękowe. 
force - 
r - promień
direction - w jakim kierunku się porusza
edge - na początku True, tylko początkowe, rzeczywiście centralnee punkty na początku fali tworzą rozprzestrzenianie się prostopadłe na boki, każda nowa cząsteczka jest aktualnym Edge. Dzięki temu uzyskuje 'sferyczny' wygląd fali



Co udało mi się na dzisiaj zrobić:
Bażanty poruszają się losowo a lisy: wyczują bażanta, to idą za nim inaczej losowo.
Lisy produkują dźwięk, który później bażanty będą wykrywać.
Bażanty produkują zapach, który później lisy będą mogły czuć.
Śledzenie bażanta przez lisa - znajduje najmnocniejszą woń.

## Co dodalam od poprzedniego razu

fox_lifetime i fox_consumptio np. ustawmy 4 i 1 ( czyli po 4 klatkach znikna wszystkie dla samych foxow w gridzie) 

Pokazać że lis zmienia stan pomiędzy WALKING, SPRINT i SNEAK ( skrada sie, idzie, biegnie w zaleznosci od odleglosci do bazanta) - różnice w prędkościach, czyli najpierw 2 potem sneak po 1 i potem attack 3, dodatkowo bardziej sie meczy gdy nie chodzi 

Pokazać, że lisy sie rozmnazają

Zboże, które co jakiś czas rośnie, samo z sb ma okres życia.

Zboże zjadane przez bażanta.



