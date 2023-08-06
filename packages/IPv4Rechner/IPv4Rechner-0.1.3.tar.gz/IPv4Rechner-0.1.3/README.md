# IPv4 Umrechner Pip

Vielen dank für das Installieren und Intreresse an dem IPv4 pip!

Dieses Pip stellt euch eine Klasse zur verfügung welche euch die IP umrechnen kann.

---

## Nutzung

Um die Umrechenfunktionen nutzen zu können, musst du einfach nur:

    from IPv4Rechner import * 
    
machen.

Eine Ip adresse wird dem Rechner nun so Übergeben:

variablen_name = IPv4(Deine IP mit CIDR als String)

---

## Funktionen

Es können nun alle IP Adressen abgefragt werden indem wir die all() Funktion nutzen:

    variablen_name.all()

Bei dieser Variante bekommen wir ein Tupple zurück welcher die IP adressen in Folgender Reihenfolge enthält:

* Netz ID
* Erste IP
* Letzte IP
* Brodcast
* Maske



Desweiteren können auch einzelne Werte abgefragt werden:

    variablen_name.bc()

Gibt den Brodcast zurück

    variablen_name.id()

Gibt die Netz ID zurück

    variablen_name.mask()

Gibt die Netz Maske zurück

    variablen_name.first()

Gibt die Erste IP Adresse des Hostnetzwerkes zurück

    variablen_name.last()

Gibt die Letzte IP Adresse des Hostnetzwerkes zurück

---

## Bekannte Fehler

Aktuell sind keine Fehler bekannt. Sollten fehler auftreten erstelle bitte ein [Issuse auf GitHub](https://github.com/comiker91/ipv4rechner/issues "Issuse melden")

## Version

Version 1.0