# BierAmpel

[![Build Nuitka Binary](https://github.com/Mega-Cookie/BierAmpel/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/Mega-Cookie/BierAmpel/actions/workflows/build.yml)

Dokumentation der Projekarbeit im Lernfeld 7 der Gruppe 3

## Gruppemitglieder
- Ahmed
- Ben
- Kevin
- Lucas
- Michael
- Zenon

## Wir brauchen:
1. Eine Kühlbox 
    - Müsste ich noch haben.

1. Drucksensoren am Boden 
    - Ist genug Bier da
    - [Amazon](https://www.amazon.de/Menschlichen-Gewichtungssensor-Verst%C3%A4rker-Dehnungsmessger%C3%A4t-Badezimmerwaage/dp/B07FMN1DBN)

1. Temparatursensor in der Kühlbox 
    - Ist das Bier kalt
    - [Amazon](https://www.amazon.de/Temperatursensor-ENOPYO-Wasserdichte-Temperaturf%C3%BChler-Temperaturkabel/dp/B0DPKHDMHH)

1. Helligkeitssensor in der Kühlbox 
    - Ist die Box offen
    - [Amazon](https://www.amazon.de/DollaTek-Digitales-Intensit%C3%A4tssensormodul-Fotowiderstand-Photowiderstand/dp/B07DJ4WQV5)

1. Eine kleine Ampel aus LEDs 
    - Ist Bier zum Trinken Bereit?
    - LEDs in den nötigen Farben habe ich.
    - Gehäuse kann ich drucken.
        - [Printables](https://www.printables.com/model/420231-traffic-light-for-arduino-ampel-fur-arduino)

1. Alarm Buzzer 
    - Ist die Box zu Lange offen? 
    - Buzzer habe ich. 
        - Alternativ Lautsprecher am RPi spielt einen Alarmton ab.


## Umsetzung
Der Temperatur- und Luffeuchtigkeitssensor von Mierwald für die Umgebung -> Ist Bierwetter?

DIe Sensoren können an einen Arduino (habe ich) angeschlossen werden.
Aus den Sensoren kann die Temperatur und der Menge an Bier (Gewicht/Gewicht einer Bierdose) ermittelt werden.
Die ganzen Daten werden im RPi gesammelt und steuern die Ampel.

Da wir die Daten ja über MQTT senden sollen, können wir mit Uptime-Kuma Benachrichtugungen verschicken, wenn das Bier alle oder zu warm ist.

Damit hätten wir alle Anforderungen erfüllt.

Den Code Packe ich auf GitHub. Wenn ihr einen Account habt, kann ich euch dafür freischalten.

Die LDE-Ampel druck ich im 3D-Drucker
## Kosten
| Posten         |     Summe |
|:---------------|----------:|
|Gewichtssensor  |      7,89€|
|Temperatursensor|      4,99€|
|Lichtsensor     |      4,99€|
|**Gesamt**      | **17,96€**|

## Nutzung
./BierAmpel --boker \<MQTT broker IP\> --port \<MQTT broker port\> --user \<MQTT User\> --pass \<MQTT Password\> --serial \<Serial Port\>