# eu5-modding-enviroment

Eine kleine europäische Testwelt für schnellere EU5-Modentwicklung: **25 große Länder, zehn Startmärkte, vereinte Staaten und eine außerhalb des Testgebiets leere Simulation.**

**Stand am 04.11.2026: Mod-Gerüst und ausgearbeiteter Umsetzungsplan angelegt. Die Performance-Reduktion ist noch nicht implementiert und wurde nicht im Spiel gemessen.** Das Aktivieren dieses Gerüsts verändert aktuell keine Spieldaten. Der Ordnername entspricht bewusst der gewünschten Schreibweise `eu5-modding-enviroment`.

## Einstieg

- [Konkreter Umsetzungsplan](docs/IMPLEMENTIERUNGSPLAN.md): Zielwelt, Eingriffe je Datei, Generator, Meilensteine, Messverfahren und Abnahme.
- [Geprüfte lokale Quellen und technische Grenzen](docs/QUELLENBEFUND.md).
- [Länder, Hauptstädte und Märkte als Konfiguration](config/scenario.json).
- [Reproduzierbares Quellenaudit mit Dateihashes](docs/source_inventory.json).
- [Arbeitsliste](docs/CHECKLISTE.md).
- [Vorlage für spätere Messläufe](benchmarks/template.csv).

## Getroffene Planungsentscheidungen

Startdatum bleibt `1337.4.1`; historische Staatenzersplitterung entfällt. Deutschland, Großbritannien, Spanien, Italien, die Niederlande und weitere Formationen existieren direkt beim Start. Alle 25 Länder starten unabhängig und ohne Kriege. Wirtschaft, Pops, Regierung, Diplomatie und Armeen bleiben für Modtests verfügbar.

Zunächst wird ein eigenes minimales Startsetup auf der bestehenden Karte erzeugt. Dadurch müssen außereuropäische Länder, Pops und Geschichte gar nicht erst als Startwelt aufgebaut werden. Danach werden unnötige Startskripte und Inhalte schrittweise entfernt. Eine tatsächlich kleinere Europakarte ist ein eigener, aufwendigerer Meilenstein für zusätzliche Kartenlade- und Speichereinsparungen.

Nur Länder zusammenzulegen, die Bevölkerungszahl durch zehn zu teilen oder den Rest der Welt einem einzelnen Dummy-Land zu geben, erfüllt dieses Ziel nicht ausreichend.

## Audit erneut ausführen

Vom gemeinsamen Mod-Workspace aus:

```powershell
python .\eu5-modding-enviroment\tools\audit_vanilla.py --game-root 'C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis V\game'
```

Das Werkzeug liest die Installation und aktualisiert ausschließlich `docs/source_inventory.json` in dieser Mod. Es zählt wörtliche Deklarationen, ohne Includes und die virtuelle Dateisystem-Reihenfolge aufzulösen; es ist kein Setup-Generator und kein Benchmark.

Die Metadaten verwenden vorläufig `supported_game_version = "*"`, weil keine verlässlich ausgelesene semantische Spielversion vorliegt. Das ist ein Platzhalter für das inhaltslose Gerüst; der erste ausführbare Build erhält eine konkret geprüfte Versionsmaske. Die Mod wurde keinem Playset hinzugefügt und nicht veröffentlicht.
