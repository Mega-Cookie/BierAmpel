# lf7g3
Dokumentation der Projekarbeit im Lernfeld 7 der Gruppe 3

# Kühlbox mit Bierampel
## Wir brauchen:
Eine Kühlbox -> Müsste ich noch haben.
Drucksensoren am Boden -> Ist genug Bier da:
https://www.amazon.de/Menschlichen-Gewichtungssensor-Verst%C3%A4rker-Dehnungsmessger%C3%A4t-Badezimmerwaage/dp/B07FMN1DBN

Temparatursensor in der Kühlbox -> Ist das Bier kalt:
https://www.amazon.de/Temperatursensor-ENOPYO-Wasserdichte-Temperaturf%C3%BChler-Temperaturkabel/dp/B0DPKHDMHH

Helligkeitssensor in der Kühlbox -> Ist die Box offen:
https://www.amazon.de/DollaTek-Digitales-Intensit%C3%A4tssensormodul-Fotowiderstand-Photowiderstand/dp/B07DJ4WQV5

Eine kleine Ampel aus LEDs -> ist Bier zum Trinken Bereit? -> LEDs in den nötigen Farben habe ich.
Alarm Buzzer -> Ist die Box zu Lange offen? -> Buzzer habe ich. (Alternativ Lautsprecher am RPi spielt einen Alarmton ab)


## Umsetzung
Der Temperatur- und Luffeuchtigkeitssensor von Mierwald für die Umgebung -> Ist Bierwetter?

DIe Sensoren können an einen Arduino (habe ich) angeschlossen werden.
Aus den Sensoren kann die Temperatur und der Menge an Bier (Gewicht/Gewicht einer Bierdose) ermittelt werden.
Die ganzen Daten werden im RPi gesammelt und steuern die Ampel.

Da wir die Daten ja über MQTT senden sollen, können wir mit Uptime-Kuma Benachrichtugungen verschicken, wenn das Bier alle oder zu warm ist.

Damit hätten wir alle Anforderungen erfüllt.

Den Code Packe ich auf GitHub. Wenn ihr einen Account habt, kann ich euch dafür freischalten.

## Kosten
| Posten         | Summe |
|:---------------|-------|
|Gewichtssensor  |  7,89€|
|Temperatursensor|  4,99€|
|Lichtsensor     |  4,99€|
|+--------------–|-------|
|Gesamt          | 17,96€|