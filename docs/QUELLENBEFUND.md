# Quellenbefund und Machbarkeit

Stand: 04.11.2026. Grundlage ist die **hier installierte EU5-Dateibasis**, keine Behauptung über eine unveränderte aktuelle Steam-Veröffentlichung.

## 1. Prüfbasis

Installationswurzel:

```text
C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis V
```

Alle nachfolgenden Spielpfade sind relativ zu deren Unterordner `game/`. Im lesbaren Steam-Appmanifest steht Build-ID `26377361`. `loading_screen/caesar_branch.txt` enthält `develop`, `caesar_rev.txt` enthält `42f8b31e`. Das bestehende `logs/setup.log` nennt einen anderen Exe-Gitstand; daraus wird keine verifizierte Versionsnummer abgeleitet. Maßgeblich für spätere Tests sind der dann tatsächlich gestartete Build, sein Checksum und das Playset.

Die lokale Bookmark-Datei enthält außerdem einen auskommentierten 1658-Testbookmark und zusätzliche Kommentare. Die Installation wird deshalb ausdrücklich nicht als bytegleich mit sauberem Vanilla behandelt. Das Audit hält SHA-256-Werte der untersuchten Textdateien fest. Bei einem späteren Update oder einer bereinigten Installation erneut ausführen und Befunde vergleichen.

## 2. Aktuelle Setup-Struktur

`main_menu/common/bookmarks/00_bookmarks.txt` setzt:

```text
bookmark_1337 = {
    start_date   = 1337.4.1
    end_date     = 1836.12.31
    setup_folder = "setup/1337"
}
```

Das untersuchte Startsetup liegt unter **`main_menu/setup/1337/`**. Länderprototypen liegen unter `in_game/setup/countries/`; Vorlagen unter `main_menu/setup/templates/`. Ältere Anleitungen mit `setup/start` passen daher nicht unverändert auf diese Installation.

Es gibt 26 TXT-Dateien im 1337-Basissetup mit zusammen 10.704.136 Bytes, rund 10,21 MiB. Weniger Setup-Text bedeutet nicht automatisch entsprechend weniger gesamte Ladezeit: Karte, Texturen, Shader, Lokalisierung und Datenbanken sind weitere Kosten.

## 3. Gezählt, nicht als Laufzeitmessung interpretiert

Die Werte stammen aus [source_inventory.json](source_inventory.json); Kommentare und Klammerung wurden beim Zählen berücksichtigt. Includes werden nicht expandiert.

| Quelle | Statischer Befund | Bedeutung für die Planung |
| --- | ---: | --- |
| `main_menu/setup/1337/10_countries.txt` | 2.351 verschiedene Länderblöcke | Nicht gleichbedeutend mit 2.351 aktiven normalen KI-Staaten. |
| Direkte `type`-Felder dieser Länderblöcke | 453 `pop`, 150 `building`, 33 `army`, 3 `location`; 1.712 ohne direktes `type` | Unorganisierte Bevölkerung, Gebäude- und Armeeländer dürfen bei der Reduktion nicht übersehen werden; ohne Typfeld ist keine Laufzeitklassifizierung bewiesen. |
| `03_markets.txt` | 123 `add_market`-Deklarationen | Zehn gezielt ausgewählte Startmärkte statt weltweiter Initialisierung. |
| `06_pops.txt` | 51.530 `define_pop`-Blöcke | Weniger Gruppen und weniger bewohnte Locations sind der Ansatz; kleinere `size` allein reduziert die Gruppenzahl nicht. |
| `06_pops.txt` | 28.570 Location-Blöcke, auch leere | Kein Beleg für 28.570 bewohnte Landorte. |
| `05_characters.txt` | 7.770 Charakterblöcke | Lebende Figuren und Vorfahren werden zusammen gezählt; kleine neue Herrscherfamilien statt vollständiger Weltgenealogie. |
| `04_dynasties.txt` | 1.286 Dynastieblöcke | Nur wirklich referenzierte Dynastien in den neuen Startdaten erzeugen. |
| `15_international_organizations.txt` | 53 direkte Manager-Unterblöcke | Starts von HRE, Verbänden usw. gesondert ersetzen. |
| `16_wars.txt` | 15 direkte Manager-Unterblöcke | Keine Startkriege aus dem historischen Setup übernehmen. |
| `in_game/setup/countries/*.txt` | 2.354 Definitions-Tags einschließlich technischer Tags | Definitionen und instanziierte Startländer getrennt behandeln. |
| `in_game/map_data/location_templates.txt` | 28.573 Location-Template-Blöcke | Die Kartendatenbank bleibt trotz leerer Startwelt groß. |
| `in_game/map_data/locations.png` | 16.384 × 8.192 Pixel | Unveränderte Geometrie wird durch politische Zusammenlegung nicht kleiner. |

## 4. Länder und Märkte tatsächlich nachgeschlagen

Alle 25 geplanten Hauptstädte und alle zehn Marktorte aus [scenario.json](../config/scenario.json) existieren in der lokalen `location_templates.txt`.

Die zehn Tags **SPA, GBR, IRE, NED, BEL, GER, ITA, RUS, RMN und GRE** existieren in `in_game/common/formable_countries/00_formable_countries.txt`, haben aber **keinen eigenen obersten Definitionsblock** in den untersuchten `in_game/setup/countries/*.txt`. Der konkrete Startaufbau muss für sie also Länderdefinition, Name, Farbe, Flagge und Regierung prüfen bzw. ergänzen. Ein Formable-Eintrag ist kein vollständiges Startland.

Die übrigen 15 Ziele besitzen solche Länderdefinitionen. Insbesondere heißt Österreich hier **HAB**, Dänemark **DAN**, Rumänien **RMN**. `ROM` bezeichnet einen anderen Formable; `RUT` ist in der Kaukasus-Datei Rutul und wäre kein geeigneter erfundener Ruthenien-Tag. Geprüfte Orts-IDs sind beispielsweise `kobenhavn`, `bucharest`, `belgrad` und `abo`.

## 5. Beiträge außerhalb der Hauptdateien

Das Audit findet zusätzliche Setup-Dateien:

- `dlc/D009_across_the_pillars/main_menu/setup/1337/25_d009_town_rights.txt`
- `dlc/D009_across_the_pillars/main_menu/setup/1337/27_d009_cities_and_buildings.txt`

Ein eigener Setup-Ordner muss im Spiel darauf geprüft werden, ob diese 1337-Beiträge ausgeschlossen bleiben. Beim Überschreiben des Vanilla-Ordners wären sie ausdrücklich mitzubehandeln. Aktivierte DLCs werden vom statischen Audit nicht ermittelt.

Weitere relevante Quellen sind `in_game/common/on_action/_hardcoded.txt` und `ai_personalities_setup.txt`, `in_game/common/situations/`, `in_game/events/`, `main_menu/common/scenarios/00_scenarios.txt`, `in_game/map_data/default.map` und die Topographien unter `in_game/common/topography/00_default.txt`.

## 6. Was belegt ist und was noch offen bleibt

**Belegt:** Die Ausgangsdaten sind in getrennte Startmanager aufgeteilt. Länder besitzen explizite Eigentumslisten, Pops eigene Location-Einträge, Märkte eine explizite Zentrumsliste. Ein eigenes konsistentes Setup ist dadurch ein konkreter Ansatzpunkt. Die Geographie unterscheidet Europa sowie Unterregionen und Areas; sie muss nicht aus Ländernamen erraten werden.

**Geplant:** Nur 25 normale Startländer instanziieren, außereuropäische Simulationsdaten weglassen, wenige eigene Figuren und Märkte erzeugen und historische Startabläufe unterbinden.

**Noch experimentell zu prüfen:** additive bzw. ersetzende Wirkung der jeweiligen Loader, eigene Bookmark-Auswahl, implizite Pop-/Ländererzeugung, leere verpflichtende Manager, DLC-Überlagerung, autoerzeugte Märkte, Kolonisierbarkeit leerer Locations und konkrete Folgen einer Wasteland-Umstellung. Aus der bloßen Existenz von `flatland_wasteland` folgt noch kein verifizierter globaler Abschalter.

**Ungeprüft:** sämtliche Geschwindigkeitsgewinne, RAM-Ersparnis, Langzeitstabilität, Save/Load und aktive Kompatibilität mit anderen Mods. Beim Audit lief kein erkennbarer EU5-Prozess. Es wurden keine Laufzeitdaten erzeugt und keine Spielsitzung bedient.

## 7. Dokumentationslage

Die offiziellen Wiki-Seiten [Setup modding](https://eu5.paradoxwikis.com/Setup_modding), [Mod structure](https://eu5.paradoxwikis.com/Mod_structure) und [Map modding](https://eu5.paradoxwikis.com/Map_modding) wurden am 04.11.2026 zum Gegenprüfen angefragt; der Abruf lieferte HTTP 401. Ihre aktuellen Inhalte konnten nicht verifiziert werden.

Als ergänzende, zeitlich nicht verifizierte Referenz wurde die vorhandene Offlinekopie unter `../../Halved Employment/docs/offline-wiki/` gelesen. Sie beschreibt unter anderem additive Setup-Manager und Encoding-Unterschiede, nennt aber noch `setup/start`. Konkrete Pfade und Syntax des Plans richten sich deshalb nach den **lokal gelesenen Spieldateien**. Die Offlinekopie ersetzt keine Laufzeitprüfung.
