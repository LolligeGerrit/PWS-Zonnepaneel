# PWS-Zonnepaneel
*Een profielwerkstuk van 4 VWO leerlingen op het Griftland College.*
***

In deze repository staat alle code die gebruikt is bij ons pws over draaiende zonnepanelen. De code runt op een Raspberry Pi 4b (2gb), en moet ervoor zorgen dat de opbrengst van 4 zonnepanelen wordt bijgehouden, hiervoor worden stroom- en spanningsmeters gebruikt. Ook worden, door middel 3 relais, twee motoren aangestuurd die elk een zonnepaneel laten draaien.

## Bestanden & functies
### [main.py](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/main/main.py)
Het bestand waaruit alle andere bestanden worden aangeroepen.
- [`make_dir()`](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/bdd85e04ab0c849ad3ada186bf3aaa13d022998c/main.py#L27) - Maak een map als deze niet bestaat.
- [`normalize()`](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/bdd85e04ab0c849ad3ada186bf3aaa13d022998c/main.py#L35) - Een simpele normalisatie functie.

### [sunposition.py](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/main/sunposition.py)
Een bestand waarmee de berekeningen voor de positie van de zon worden gedaan. (zonspositie_old is de oude versie)
- [`getSunLoc()`](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/bdd85e04ab0c849ad3ada186bf3aaa13d022998c/sunposition.py#L20) - Locatie van de zon berekenen op een datum en locatie.
- [`get_season_angle()`](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/bdd85e04ab0c849ad3ada186bf3aaa13d022998c/sunposition.py#L97) bereken de seizoenshoek van een dag op een locatie.

### [message_service.py](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/main/message_service.py)
Een bestand waarmee er berichten vanuit de code naar de makers kan worden gestuurd.
- [`send_message()`](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/bdd85e04ab0c849ad3ada186bf3aaa13d022998c/message_service.py#L8) - Stuur een bericht naar aangewezen personen.

### [data_collectie.py](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/main/data_collection.py)
Een bestand waarmee data wordt. Deze wordt gebruikt tijdens de meetperiode.
- [`multiplexer_disall()`](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/bdd85e04ab0c849ad3ada186bf3aaa13d022998c/data_collection.py#L19) - Zet alle kanalen van de multiplexer uit.
- [`multiplexer_solo()`](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/bdd85e04ab0c849ad3ada186bf3aaa13d022998c/data_collection.py#L25) - Zet één kanaal van de multiplexer aan, de rest wordt uitgezet.
- [`read_sensors()`](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/bdd85e04ab0c849ad3ada186bf3aaa13d022998c/data_collection.py#L33) - Verzamel data van alle sensors.
- [`collect_data()`](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/bdd85e04ab0c849ad3ada186bf3aaa13d022998c/data_collection.py#L51) - Verzamel data van alle sensors en sla deze op in `./data/pws_data.txt`.

### [motor_controller.py](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/main/motor_controller.py)
Een bestand waarmee de motor wordt aangestuurd.
- [`switch_on()`](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/bdd85e04ab0c849ad3ada186bf3aaa13d022998c/motor_controller.py#L20) - Zet een relay aan of uit.
- [`switch_flow()`](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/bdd85e04ab0c849ad3ada186bf3aaa13d022998c/motor_controller.py#L67) - Schakel relais 1 en 3 aan/uit ten opzichte van hun huidige waarde. Dit wordt gebruikt om de plus- en minpool om te draaien.
- [`get_sun_percentage()`](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/bdd85e04ab0c849ad3ada186bf3aaa13d022998c/motor_controller.py#L86) - Bereken het percentage van de zonsdag (tijd dat de zon op is) dat al voorbij is.
- [`get_sun_times()`](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/bdd85e04ab0c849ad3ada186bf3aaa13d022998c/motor_controller.py#L103) - Krijg de zonsopkomst en ondergangs tijden van een dag.
- [`control_motor()`](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/bdd85e04ab0c849ad3ada186bf3aaa13d022998c/motor_controller.py#L112) - Beweeg de motor wanneer nodig.

### [daily_recap.py](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/main/daily_recap.py)
Een bestand wat de totale opbrengst van de dag berekend, en deze naar de gebruikter stuurd.
- [`send_daily_recap()`](https://github.com/LolligeGerrit/PWS-Zonnepaneel/blob/bdd85e04ab0c849ad3ada186bf3aaa13d022998c/daily_recap.py#L9) - Bereken de totale opbrengst en het maximale vermogen (alle opstellingen samen) van de dag, en stuur deze naar de gebruiker. Omdat dit bericht steeds rond `21:00` wordt verstuurd, wordt het ook gebruikt als indicatie dat de opstelling nog goed functioneerd.

### [tca9548a.py](https://github.com/IRNAS/tca9548a-python) <br>

Een bestand waarmee de multiplexer wordt aangestuurd.

***

## Gebruikte packages
- datetime
- time
- requests
- asyncio
- math
- [julian](https://github.com/dannyzed/julian)
- [ina260](https://github.com/jveitchmichaelis/ina260)
- [Adafruit_CircuitPython_ADS1x15](https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15)
- [matplotlib](https://github.com/matplotlib/matplotlib)

***

*Tijdens het schrijven van deze code is de tool "Github Copilot" gebruikt.*
