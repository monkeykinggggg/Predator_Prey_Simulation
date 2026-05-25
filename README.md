# Predator_Prey_Simulation

### TODO
Naprawić zachowanie bażantów
Mapa - ta sama inicjalizacja, mozna lepiej porownac parametry i wykresy
Wykres każdego gatunku agentów
Dlugosc zycia jako jeden parametr (zeby te proporcje byly bardziej realistyczne)
Poprawic UI
Dokumentacja



Parametr: jednostka długości życia:

Pszenica 
Pszenica jest rośliną jednoroczną, więc jej „życie” trwa zwykle jeden sezon wegetacyjny.

Typowe wartości:
od zasiania do obumarcia:
około 4–8 miesięcy
zależnie od odmiany (ozima/jara) i klimatu
Możesz przyjąć w symulacji:
młoda pszenica: 0–30% życia
dojrzała: 30–80%
obumierająca / gotowa do zbioru: 80–100%

https://www.britannica.com/plant/wheat


Bażant zwyczajny
W naturze:
średnia długość życia:
zwykle 1–3 lata
wiele osobników ginie wcześniej przez:
drapieżniki
zimę
choroby
polowania

https://animaldiversity.org/accounts/Phasianus_colchicus/


Bażant zjada pszenicę na każdym etapie jej życia. Chętnie kosztuje ziarna, kiełki, młodą pszenicą jak i nawet czasem obumarłą, więc faza wzrostu pszenicy nie ma znaczenia w symulacji. Bażant w naszej symulacji nie ma inego źródła pokarmu, więc naawet gdy pszenica jest niedojrzała, pożywia się nią.

Lis rudy
W naturze:
średnia długość życia:
około 2–5 lat
wysoka śmiertelność młodych


Realistyczny maksymalny wiek w naturze: 5 lat

W symulacji jako parametr podajemy maksymalny wiek życia w naturze. (czyli dopiero potem nasze czyniki w postaci zjadających zmniejszają długość życia)




## rozmnazanie
Pszenica
Rozmnaza się raz pod koniec życia (czyli co długość życia pszenicy, powstają nowe)

Bażant
Bażanty:
rozmnażają się sezonowo,
zwykle:
1 raz w roku
okres lęgowy:
wiosna / początek lata

Samica:
składa:
około 8–15 jaj - wykluwa się około 80% jaj, czyli średnio rozmnaża się ostatecznie o 5-12 w sezonie lęgowym z jednej samicy

Lis
Lisy:
rozmnażają się:
zwykle 1 raz w roku
młode rodzą się wiosną
Miot:
zwykle:
4–6 młodych


WAZNE!: jezeli dany gatunek wymrze to juz go nie odżywamy, kończymy z nim a jednocześnie kończymy z symulacją - jest to na tyle żadki przypadek, że możemy pominąć elemnt odżywania gatunku. Sama testująć symulację na różnych konfiguracjach parametrów, nie udało mi się dostać takiej sytuacji