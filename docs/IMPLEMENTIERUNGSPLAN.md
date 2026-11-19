# Umsetzungsplan: kleine europäische EU5-Moddingumgebung

Stand: 04.11.2026 · Status: ausgearbeitete Planung, noch kein spielbarer reduzierter Build.

## 1. Ziel und Erfolgskriterien

Die Mod soll die Zeit zwischen einer Modänderung und ihrem Test im Spiel verkürzen. Dazu entsteht ein künstliches Europa mit **25 unabhängigen Ländern und zehn Startmärkten**. Nicht benötigte Weltbevölkerung, Staaten, Geschichte und Startlogik werden vor der Weltinitialisierung weggelassen. Innerhalb Europas bleiben genügend Wirtschaft, Diplomatie, Regierung, Pops, Armeen und Handel für praktische Modtests erhalten.

Deutschland, Großbritannien, Spanien und Italien sind am ersten Tag bereits vereint. Sie werden direkt im Startsetup angelegt. Das Datum bleibt `1337.4.1`, damit Technologie- und Zeitalterabhängigkeiten zunächst auf ihrem vorhandenen Ausgangspunkt bleiben. Die Ländergrenzen sind ein funktionales Testlayout, keine historische oder moderne Grenzsimulation.

Die erste Version ist erreicht, wenn:

- genau 25 normale spielbare Länder und keine zusätzlichen historischen Kleinstaaten existieren;
- außerhalb des freigegebenen Testgebiets keine aktiven Länder, Pop-Gruppen, Gebäude, Einheiten oder Märkte verbleiben;
- dort auch nach einem Monatswechsel keine impliziten `pop`-/`building`-Länder oder Siedlungen entstehen;
- die zehn vorgesehenen Marktzentren existieren und keine historischen Weltmärkte zusätzlich geladen werden;
- alle 25 Länder gültige Hauptstädte, Eigentum, Regierung, Herrscher und eine nutzbare Wirtschaft besitzen;
- wichtige Modtestansichten funktionieren und Save/Load sowie mindestens zehn simulierte Jahre bestehen;
- wiederholte Messungen eine Verbesserung von New-Game-Ladezeit und Simulationszeit gegenüber der dokumentierten lokalen Referenz zeigen;
- Prozessstart bis Hauptmenü separat gemessen wird; ein unveränderter Wert dort nicht als Verbesserung ausgegeben wird.

Die Zahlen zu Vanilla-Deklarationen und alle offenen Engine-Fragen stehen im [Quellenbefund](QUELLENBEFUND.md). Noch gibt es keine gemessenen Einsparungen.

## 2. Drei Arbeitsstufen mit unterschiedlicher Wirkung

| Stufe | Umsetzung | Erwarteter Nutzen, noch zu messen | Verbleibende Kosten |
| --- | --- | --- | --- |
| A: reduzierte Startwelt | Eigenes Setup, 25 Länder, nur europäische Pops, zehn Märkte, minimale Figuren, keine Startkriege/Verbände | Vor allem Aufbau eines neuen Spiels, Tickdauer und Save-Größe | Weltgeometrie, große allgemeine Datenbanken und Grafikressourcen werden weiter geladen. |
| B: weniger geladene Inhalte | Historische Events/Startskripte gezielt ersetzen, unnötige Instanzen und nur nach Abhängigkeitsprüfung Definitionen entfernen | Zusätzliche Initialisierungs- und mögliche Hauptmenü-Ladeersparnis | Engine, Pflichtdatenbanken, globale Karte und benötigte Assets bleiben. |
| C: kleinere Europakarte | Eigene reduzierte Geometrie und konsistente Kartenressourcen | Potenzial für Kartenladezeit, Speicherbedarf, globale Location-Schleifen und Pathfinding | Hoher Aufwand und größere Entfernung vom Vanilla-Testkontext. |

**Reihenfolge: A vollständig funktionsfähig machen, B messen, C mit kleinem Machbarkeitstest beginnen.** C ist für das Ziel einer maximal kleinen Umgebung vorgesehen, aber keine Voraussetzung, um mit A bereits Modtests zu beschleunigen. Wenn hauptsächlich Prozessstart bis Hauptmenü langsam ist und A/B dort kaum helfen, hat C Vorrang vor weiteren kleinen Scriptoptimierungen.

## 3. Konkrete Zielwelt

Die bearbeitbare Quelle ist [config/scenario.json](../config/scenario.json). Sie enthält die 25 Tags, geprüfte Hauptstadt-IDs, Herkunft der Tags und Gebietsbeschreibungen. Noch fehlen die vollständige Location-Zuordnung und generierte Spieldateien.

| Land | Tag | Hauptstadt-ID | Zusammenlegung / Abgrenzung |
| --- | --- | --- | --- |
| Frankreich | FRA | `paris` | Französische Kleinstaaten und Bretagne integrieren; Elsass/Lothringen französisch. |
| Portugal | POR | `lisbon` | Eigenständig; keine Kolonien. |
| Spanien | SPA | `madrid` | Kastilien, Aragon, Navarra, Granada und Balearen; Portugal ausnehmen. |
| Großbritannien | GBR | `london` | England, Schottland, Wales und Hebriden; keine kontinentalen Besitzungen. |
| Irland | IRE | `dublin` | Ganze Insel, keine englischen Enklaven. |
| Niederlande | NED | `amsterdam` | Holland/Friesland und explizit abgegrenzter nördlicher Brabant-Anteil. |
| Belgien | BEL | `brussels` | Flandern, Wallonien, Südbrabant und Luxemburg. |
| Deutschland | GER | `berlin` | Deutsche Staaten vereinigen; die separat geführten Nachbarn ausschließen. |
| Schweiz | SWI | `bern` | Schweizer Gebiete zusammenfassen. |
| Österreich | HAB | `vienna` | Österreichische Areas, Tirol und Slowenien; ohne Böhmen/Ungarn. |
| Italien | ITA | `rome` | Halbinsel, Kirchenstaat, Venedig/Genua, Sizilien, Sardinien, Korsika und Savoyen vereinen. |
| Dänemark | DAN | `kobenhavn` | Denmark-Area; Holstein deutsch, Skåne schwedisch. |
| Norwegen | NOR | `oslo` | Norwegische Gebiete, Island/nördliche Inseln; kein Grönland. |
| Schweden | SWE | `stockholm` | Schweden/Skåne; finnische Gebiete abtrennen. |
| Finnland | FIN | `abo` | Finnische Areas; Karelien über explizite Grenzliste. |
| Polen | POL | `krakow` | Polnische Gebiete, Preußen/Schlesien, Red Ruthenia und Podolia. |
| Böhmen | BOH | `prague` | Böhmen und Mähren. |
| Ungarn | HUN | `pest` | Ungarische Areas und Slowakei; kein Siebenbürgen. |
| Litauen | LIT | `vilnius` | Litauen/Samogitien und westlicher ruthenischer Testblock. |
| Livland/Baltikum | LIV | `riga` | Estnische und lettische Gebiete als ein Teststaat. |
| Russland | RUS | `moscow` | Russian-Region und östliche Ruthenia-Areas; keine asiatischen Besitzungen. |
| Rumänien | RMN | `bucharest` | Walachei, Moldau und Siebenbürgen. |
| Serbien/Südslawischer Testblock | SER | `belgrad` | Serbien, Bosnien, Kroatien, Slawonien und Albanien vereinfachen. |
| Bulgarien | BUL | `tarnovo` | Bulgaria/Macedonia. |
| Griechenland | GRE | `constantinople` | Griechische Gebiete und europäische Thrace; kein Anatolien. |

Der Kirchenstaat wird in Italien integriert. Falls katholische Kernfunktionen ohne päpstlichen Staat Fehler erzeugen, werden zuerst die betreffenden Funktionen im Testprofil angepasst. Ein zusätzliches Land darf nicht unbemerkt aus der Zielzahl werden; ein nachweislich unverzichtbarer Sonderfall wäre als bewusste Änderung des Rosters zu dokumentieren.

## 4. Exakte Gebietszuordnung statt Annexion nach Tags

Das neue Eigentum wird aus **Geographie**, nicht aus dem bisherigen Besitzer abgeleitet. Dadurch verliert etwa England seine französischen Gebiete an Frankreich und Venedig seine griechischen Besitzungen an Griechenland. Ein schlichtes `ENG + SCO -> GBR` würde diese Grenze nicht herstellen.

1. `in_game/map_data/definitions.txt` und `location_templates.txt` einlesen; tatsächliche Verschachtelung und die Land-/Wasser-/Wasteland-Klassifizierung prüfen. Nicht allein anhand von `_area`-Namensendungen klassifizieren.
2. Für das Testgebiet zunächst `scandinavian_region`, `north_german_region`, `south_german_region`, `great_britain_region`, `ireland_region`, `france_region`, `iberia_region`, `italy_region`, `carpathia_region`, `baltic_region`, `ruthenia_region`, `russian_region` und `balkan_region` freigeben.
3. Aus `north_atlantic_islands_region` nur Island und die benötigten nördlichen Inseln ergänzen. `greenland_area`, Kaukasus-, Ural- und Steppenregionen sowie sämtliche übrigen Kontinente ausnehmen. Kola-/Karelienanteile innerhalb Skandinaviens bewusst FIN/RUS zuordnen.
4. Benötigte europäische Seegebiete und verbundene Hafenrouten gesondert freigeben. Seegebiete erhalten keinen Landeigentümer. Azoren/Madeira/Kanaren und außereuropäische Enklaven zunächst ausnehmen.
5. Datei `config/ownership_rules.json` anlegen: pro Land Regions-/Area-Regeln; Ausnahmen auf Provinz- oder Location-Ebene. Für Brabant, Luxemburg, Savoyen, Korsika, Karelien, Schleswig und baltische Grenzfälle explizite Listen pflegen.
6. Priorität verbindlich machen: Location-Ausnahme vor Provinz vor Area vor Region. Gleichrangige Mehrfachzuordnung ist ein Fehler; keine stillschweigende „letzte Regel gewinnt“-Logik.
7. Daraus `artifacts/ownership.csv` erzeugen: `location,province,area,region,target_tag,rule_id`. Jede behaltene besiedelbare Landlocation muss genau einen Besitzer haben. Wasser und bestehende Wastelands nicht versehentlich vergeben. Die Hauptstadt muss zum zugehörigen Land gehören.
8. Visuelle politische Karte gegen diese Zuordnung prüfen. Erst anschließend Startdaten erzeugen.

`ownership.csv` ist das konkrete Prüfergebnis der ersten Implementierungsphase. Die Tabelle oben definiert noch keine lückenlosen Grenzen.

## 5. Eigenes Setup und korrekte Dateiersetzung

### Bevorzugter Weg: eigener Bookmark und eigener Setup-Ordner

`main_menu/common/bookmarks/00_bookmarks.txt` im Mod unter demselben relativen Dateipfad gezielt ersetzen und nur einen eigenen Testbookmark mit `setup_folder = "setup/eu5env"` anbieten. Unter `main_menu/setup/eu5env/` ausschließlich die minimalen Managerdaten erzeugen. Die beobachtete `setup_folder`-Syntax stammt aus der Installation; die komplette Lade- und Auswahlwirkung muss ein früher Starttest bestätigen.

Kein `include` auf vollständige 1337-Dateien, keine nachgelagerte Weltlöschung. Nur freigegebene kleine Vorlagen verwenden und ihre transitiven Includes prüfen. `main_menu/common/scenarios/00_scenarios.txt` ebenfalls ersetzen: nur Startvorschläge für existierende Zielstaaten und den eigenen Bookmark. Sonst könnte die Länderauswahl noch auf Kastilien, Neapel oder einen alten Bookmark zeigen.

### Rückfallweg: belegte Dateien vollständig überschreiben

Falls das eigene Setup im Spiel nicht sauber isoliert wird, jeden betroffenen relativen Pfad aus `main_menu/setup/1337/` im Mod vollständig ersetzen; einschließlich der zusätzlichen DLC-Dateinamen. Die virtuelle Dateisystem-Reihenfolge und tatsächlich eingelesenen Dateien im Log überprüfen.

Eine zusätzliche Datei `zz_eu5env_countries.txt` entfernt keine vorher geladenen Einträge. Ebenso löscht ein im Mod leer angelegtes Verzeichnis nicht die Vanilla-Dateien. Eine etwaige Ordnerersetzung nur verwenden, wenn Syntax und Verhalten dieser EU5-Version konkret belegt wurden; keine aus EU4/CK3 übernommene `replace_path`-Annahme.

Für `setup/countries` zuerst nur die fehlenden Zieldefinitionen ergänzen. Unbenutzte Vanilla-Prototypen dürfen in A zunächst weiter als Definitionen geladen werden, solange sie nicht instanziiert werden. B untersucht eine vollständige Verkleinerung dieser Datenbank einschließlich ihrer Referenzen und technischen Sondertags.

## 6. Eingriffe je vorhandenem Setup-Bereich

Die Dateinamen in der Tabelle sind die gelesenen Quelldateien unter `main_menu/setup/1337/`. Der Generator schreibt deren notwendige Teilmengen in das eigene Setup, statt die Weltdateien zu übernehmen.

| Quelldatei | Konkrete Behandlung |
| --- | --- |
| `02_core.txt` | Notwendige Manager und frühe Institutionen bewahren; Geburtsorte außerhalb der Testwelt gezielt auf gültige europäische Testorte umstellen oder Institution konsistent deaktivieren. Alter und Pflichtwerte erhalten. |
| `03_markets.txt` | Nur zehn geplante `add_market`-Einträge erzeugen. |
| `04_dynasties.txt` | Nur neue kleine Herrscherfamilien und tatsächlich referenzierte Dynastien. |
| `04_religious_orders.txt` | Keine historischen Orden instanziieren; notwendige Abhängigkeiten prüfen. |
| `05_characters.txt` | Eigene minimale Herrscher/Erben statt Weltgenealogie; keine toten Ahnenketten. |
| `06_pops.txt` | Nur behaltene Landorte; Gruppen wie in Abschnitt 7 reduzieren. Außerhalb keine `define_pop`-Einträge. |
| `07_cities_and_buildings.txt` | Europäische Städte/Gebäude filtern, wichtige Arbeitsplätze bewahren; Eigentümer von Gebäude- und ausländischen Besitzungen bereinigen. |
| `08_institutions.txt` | Location-Einträge filtern; Konsistenz zum Institutionenmanager sichern. |
| `09_roads.txt` | Nur Kanten mit zwei freigegebenen Endpunkten. |
| `10_countries.txt` | Genau 25 Startländer aus neuen Eigentumslisten; direkte `own_control_core`-Zuordnung, keine fremden Kontrollen, Enklaven oder Bürgerkriegsreste. |
| `11_art.txt` | Keine historischen Kunstwerke im ersten Minimalsetup; Features später über gezielte Testdaten prüfbar machen. |
| `12_diplomacy.txt` | Keine historischen Vasallen, Personalunionen, Ehen, Bündnisse und Beziehungen zu entfernten Ländern. |
| `13_religion.txt` | Die Datei enthält hier einen `building_manager`: religiöse Gebäude/Besitzländer ausdrücklich prüfen, nicht bloß Religionen löschen. |
| `14_development.txt` | Notwendige allgemeine Entwicklungsregeln behalten; außereuropäische Ortsregeln entfernen. Nicht versehentlich ganz Europa ohne Entwicklung starten lassen. |
| `15_international_organizations.txt` | Keine HRE-, Hanse-, Clan- oder Unionsinstanzen initialisieren. Typdefinitionen erst nach Prüfung entfernen. |
| `16_wars.txt` | Keine historischen Kriegs- oder Bürgerkriegsinstanzen. |
| `18_opinions.txt`, `20_rivals.txt` | Historische Beziehungen weglassen; reguläre Diplomatie bleibt funktionsfähig. |
| `19_diseases.txt` | Keine vorgegebenen Seuchenausbrüche. Krankheiten/Neuausbrüche in einem ruhigen Profil separat kontrollieren. |
| `21_locations.txt` | Nur notwendige europäische Ortsmodifikatoren; keine verbleibenden Außenweltreferenzen. |
| `22_situations.txt` | Keine historischen Situationsstarts. Auch spätere automatische Aktivierung sperren. |
| `23_colonies.txt` | Keine kolonialen Ansprüche; Finnland/Nordskandinavien erhalten direkt den Zielbesitzer. |
| `24_town_rights.txt` | Nur notwendige Rechte innerhalb der Testwelt; fremde Begünstigte entfernen. |
| `25_area_preferences.txt` | Keine historischen Kolonisierungsaufträge oder Ländererweiterungen übernehmen. |
| `26_ai_personalities.txt` | Nur gültige Zielstaaten und einfache vorhandene KI-Persönlichkeiten. |
| `27_armies.txt` | Historische Kriegseinheiten weglassen; kleine neue Testarmeen und ausgewählte Flotten erzeugen. |
| DLC-Setup | Zwei gefundene D009-Dateien und spätere DLC-Erweiterungen beim Isolationsnachweis berücksichtigen. |

Die Reihenfolge muss die tatsächlichen Abhängigkeiten einhalten: Definitionen und Dynastien vor ihren Referenzen, Eltern/Partner vor benötigten Charakterverweisen, Eigentümer vor nachgelagerten Besitzabhängigkeiten. Encoding am aktuellen Loader prüfen; die Offline-Referenz nennt UTF-8 ohne BOM für Startsetup und UTF-8 mit BOM für Länder/Vorlagen. Lokalisierungsdateien im EU5-Format mit korrektem Sprachkopf und BOM schreiben.

## 7. Pops und Wirtschaft klein, aber für Tests brauchbar halten

**Primärer Hebel ist die Zahl der Pop-Gruppen.** Dieselben 50.000 Gruppen mit einem Zehntel ihrer Einwohnerzahl sind noch dieselben 50.000 zu verwaltenden Gruppen; eine lineare Tickersparnis ist daraus nicht ableitbar.

Für `core` zunächst pro Location identische Kombinationen aus Pop-Typ, Kultur und Religion zusammenfassen und die Bevölkerungsmenge summieren. Außerhalb des Testgebiets alle Gruppen weglassen. Als zweiter, separat messbarer Schritt pro Location eine dominante Kultur und Religion für das gewöhnliche Testsetup verwenden, aber unterschiedliche Berufsgruppen und soziale Schichten bewahren. Optional ausgewählte kleine Minderheiten an wenigen dokumentierten Testorten behalten, damit Kultur-/Religionsoberflächen prüfbar bleiben.

Nicht alle Orte ausschließlich mit Bauern füllen: Adel, Klerus, Bürger und produktive Stadtbevölkerung sind für Regierung, Steuern und Produktion relevant. Selten benötigte Funktionen erhalten kleine bewusst angelegte Testfälle statt globaler Komplexität. Einwohnerzahl zunächst nicht pauschal reduzieren; sonst ändern sich Nahrung, Beschäftigung, Nachfrage und Rekrutierung gleichzeitig.

**Marktzentren:** `london`, `paris`, `lisbon`, `sevilla`, `lubeck`, `venice`, `stockholm`, `krakow`, `moscow`, `constantinople`. Zehn ist ein fester erster Versuch, kein bewiesenes Optimum. Länder dürfen sich Märkte teilen; wir erzwingen keinen Markt pro Land. Ein `add_market` weist nicht automatisch alle gewünschten Länder diesem Markt zu.

Im Spiel Zugang, tatsächliche Zugehörigkeit, Marktattraktion, Hafenverbindungen und Handel nach einem Tag/Monat/Jahr prüfen. Besonders Portugal, Norwegen, Finnland, Livland und die russischen Randgebiete müssen erreichbar bleiben. Das unveränderte Vanilla-Setup kommentiert Oslo bereits mit Zugangsproblemen bei Bergen: Zentrumsauswahl deshalb nicht nur nach geografischer Schönheit treffen.

Kein zusätzlicher versteckter Weltmarkt für exotische Waren. Stattdessen notwendige Produktionsketten prüfen und fehlende Inputs in einem klar dokumentierten `economy_fixture` an wenigen europäischen Testorten bereitstellen oder für den Testzweck unnötige Nachfrage gezielt reduzieren. Waren-, Gebäude- und Produktionsmethoden-Definitionen zunächst behalten. Ein leerer globaler Warenkatalog würde gerade die zu testenden Mods verfälschen.

Arbeitsbudget als erste Implementierungshypothese: höchstens 10.000 erzeugte `define_pop`-Blöcke und 100 manuell angelegte Startfiguren. Nach exakter Gebietszuordnung auf realistische Mindestbedürfnisse prüfen; diese Budgets sind keine gemessenen Laufzeitwerte.

## 8. Außenwelt wirklich stilllegen

Außerhalb Europas nur Eigentum zu löschen ist unzureichend. Dort könnten unorganisierte Pop-Länder, religiöse Gebäude, Märkte, autonome Einheiten oder neue Kolonien weiter existieren bzw. entstehen.

Für A:

1. Sämtliche entsprechenden Startinstanzen weglassen, einschließlich direkter `type = pop`, `building`, `army` und `location`-Länder.
2. Beobachten, ob Engine oder Startskripte Ersatzländer/Pops erzeugen. Runtime-Objektzahlen und Logs sind entscheidend, nicht nur unser generierter Text.
3. Ausgeschlossene Landorte bei Bedarf im mod-eigenen `location_templates.txt` auf eine anhand der Installation und eines kleinen Prototyps geprüfte Wasteland-Klassifizierung umstellen. Die vollständige Datei korrekt überschreiben; Geometrie-IDs in A erhalten. Kein unbelegtes `enabled = no` oder erfundenes Define einsetzen.
4. Kolonisierung, Exploration, Migration und Ereignisse in ausgeschlossene Gebiete für das Testprofil sperren. Geeignete Regel-/Trigger-Einstiegspunkte vor Umsetzung nachweisen. Binnenkolonisierung Nordskandinaviens ebenfalls berücksichtigen.
5. Nach Monat 1 und Jahr 1 prüfen, dass außerhalb keine Instanzen, Marktzonen oder Außenwelthandelsrouten zurückgekehrt sind. Danach zehn Jahre prüfen.

Ein einziges großes „Restwelt“-Land mit weiter existierenden Pops wäre kein Ersatz für diese Reduktion. Auch unsichtbare/fogged-out Gebiete werden dadurch nicht als abgeschaltet angenommen.

## 9. Startlogik und dauerhaft laufende Inhalte reduzieren

In B die tatsächlichen Aufrufketten von `in_game/common/on_action/` untersuchen, beginnend bei `_hardcoded.txt` und dem vorhandenen `on_game_start`. Historische Setups, Ausgangskriege, Situationsstarts, Organisationsgründungen, Erbfolgen, Diplomatie und Kolonisationsaufträge entfernen, die der neuen Welt widersprechen oder die Kleinstaaten wieder erzeugen.

Wirtschaft, Beschäftigung, Marktabgleich, normale Regierung, Militär und für die zu testende Mod benötigte On-Actions bleiben erhalten. Kein pauschales Leeren des gesamten On-Action-Verzeichnisses; das könnte Initialisierungen zerstören und eine scheinbar schnelle, aber defekte Testwelt erzeugen.

Events zuerst an den tatsächlichen Aufrufen reduzieren. `trigger = { always = no }` in einer bereits geladenen Datei verhindert ihren Parser-/Dateizugriff nicht. Für kürzere Datenladezeiten müssen Dateien über nachgewiesene Ersetzung aus der geladenen Datenmenge herausfallen; alle Referenzen auf entfernte Event-IDs, Scripted Effects und Variablen werden dabei aufgelöst.

Start ohne Situationen/Organisationen heißt nicht, dass deren spätere Aktivierung verhindert ist. Aktivierungsbedingungen und Pulse deshalb gesondert prüfen. Formable-Entscheidungen für die bereits vereinten Länder und historische Wiederherstellungsereignisse so behandeln, dass sie nicht versehentlich Länder aufspalten. Technische Engine-Sondertags wie `DUMMY`, `PIR` und `MER` nur nach eigenem Nachweis anfassen; sie zählen getrennt von den 25 normalen Ländern.

Nach jeder entfernten Inhaltsgruppe neu laden, Fehlerlogs prüfen und eine Messung durchführen. Inhalte ohne nachweisbaren Nutzen oder mit unnötigem Kompatibilitätsverlust nicht weiter ausdünnen.

## 10. Eigene kleine Europakarte für weitergehende Startup-Reduktion

Eine leere Welt auf der vorhandenen 16.384 × 8.192-Karte bleibt eine große Karte mit knapp 28.600 Location-Templates. Globale Schleifen, Geometrie, Kartenbilder und Ressourcen können weiter Kosten verursachen. C untersucht daher eine tatsächliche Verkleinerung.

Zunächst ein separat rücknehmbarer Kartenprototyp mit einem kleinen Ausschnitt, wenigen Locations und einem Land. Erst bei erfolgreichem Start, Save/Load und validen Land-/Seewegen auf das 25-Länder-Europa erweitern. Keine feste Bildgröße festlegen, bevor Engine-Anforderungen und Ressourcenauflösungen geprüft sind.

Gemeinsam und konsistent bearbeiten:

- `map_data/default.map`, `locations.png`, `definitions.txt`, `location_templates.txt` und `rivers.png`;
- `adjacencies.csv`, `ports.csv`, `generated_locators_port.txt` und die erforderliche Neuerzeugung von `nodes.dat` mit einem belegten Werkzeug;
- Höhen-/Terrain-Daten, Wasser, Küsten, Locator-Positionen, Städte, Flüsse, Kartenobjekte, Splines und Surround-/Flatmap-Ressourcen, soweit im installierten Kartenstapel beteiligt;
- Koordinaten, Kartenumbruch (`wrap_x`), Äquatorposition sowie außerhalb liegende Zölle/Vulkane aus `default.map`;
- Named Locations, Scripted Geography, Institutionsgeburtsorte, Religionen/heilige Orte, Szenarien, Events und alle verbliebenen Verweise auf entfernte Locations.

Ein bloßer Bildausschnitt bei unveränderten übrigen Dateien ist keine konsistente Karte. Die noch vorhandenen europäischen Location-IDs nach Möglichkeit erhalten, um Modtests nicht unnötig zu entkoppeln. Anschließend prüfen, ob optionales Zusammenlegen europäischer Locations weiteren Nutzen bringt; das verändert Testrealismus und ist eine gesonderte Entscheidung.

**Entscheidung nach Prototyp:** Gibt es ein reproduzierbares Verfahren für gültige Nodes/Küsten/Ports und einen messbaren Lade-/Speichervorteil, C fertigstellen. Andernfalls dokumentiert A/B als erste nutzbare Version liefern und den konkreten Kartenblocker festhalten. Eine Kamerabegrenzung darf nicht als Kartenverkleinerung ausgegeben werden.

## 11. Generator und geplante Projektstruktur

Aktuell existieren Konfiguration, Audit, Metadaten und Dokumentation. Folgende Dateien werden erst in den Implementierungsphasen angelegt:

```text
config/ownership_rules.json          # eindeutige Geographieregeln
config/content_policy.json           # erlaubte Instanzen/Events/Startaktionen
tools/generate_setup.py              # Parser, Include-Auflösung, Generator
tools/validate_setup.py              # Referenz-/Eigentums-/Budgetprüfungen
main_menu/common/bookmarks/00_bookmarks.txt
main_menu/common/scenarios/00_scenarios.txt
main_menu/setup/eu5env/*.txt          # minimaler erzeugter Startdatensatz
in_game/setup/countries/eu5env_formed.txt
main_menu/localization/german/eu5env_l_german.yml
main_menu/localization/english/eu5env_l_english.yml
artifacts/ownership.csv
artifacts/build_manifest.json        # Inputhashes, erzeugte Dateien, Objektzahlen
benchmarks/runs/<run-id>/            # Messwerte, Logs, Screenshots
```

Generator-Eigenschaften:

- Kommentar- und String-sicherer Parser mit wiederholten Schlüsseln, Listen und nachvollziehbarer Include-Auflösung; das vorhandene Auditwerkzeug reicht dafür ausdrücklich nicht aus.
- Ausschließlich lesender Zugriff auf die Spielinstallation; Ausgabe nur innerhalb dieser Mod. Kein Kopieren des gesamten Spiels und kein Löschen aus der Installation.
- Deterministische Ausgabe, feste Sortierung und identische Hashes bei gleichen Inputs/Konfigurationen. Zeitstempel nur im Manifest, nicht in allen generierten Spieldateien.
- Vor dem Schreiben Zielpfade prüfen; nur selbst erzeugte Dateien aus dem eigenen Manifest ersetzen/aufräumen, handgepflegte Moddateien bewahren.
- Erst in ein Staging-Verzeichnis generieren, validieren, danach die eigenen Ausgabedateien übernehmen. Fehlgeschlagene Generierung darf den letzten funktionsfähigen Stand nicht zerstören.
- Bei geänderter Quellstruktur oder fehlenden IDs abbrechen und einen konkreten Bericht schreiben. Keine unbekannten Länder oder Orte stillschweigend weglassen.

## 12. Umsetzung in überprüfbaren Meilensteinen

| Schritt | Konkretes Ergebnis | Voraussetzung / Abnahme |
| --- | --- | --- |
| M0 – Befund und Gerüst | Dieser Plan, 25er-Roster, Audit und Quellhashes | Erledigt; keine Laufzeitfreigabe daraus ableiten. |
| M1 – Messreferenz und Loader-Probe | Separates Testplayset, Referenzmessung, eigener Bookmark mit minimalem Testsetup | Tatsächlich geladenen Setup-Pfad zeigen; keine übernommenen globalen Instanzen; bestehende Nutzersaves unangetastet. |
| M2 – Grenzen und Länder | Vollständige `ownership.csv`, zehn ergänzte Länderdefinitionen, 25 Startländer | Jede freigegebene Landlocation genau einmal vergeben; alle Hauptstädte gehören dem richtigen Land. |
| M3 – Bevölkerung und Wirtschaft | Gefilterte/vereinfachte Pops, Städte, Infrastruktur, zehn Märkte, minimale Figuren | Wirtschaft und Marktverbindungen nach Tag/Monat nutzbar; keine ungültigen Referenzen. |
| M4 – Außenwelt und Startlogik | Keine aktiven Außenweltinstanzen; keine historischen Kriege/Verbände/Situationen | Kontrollen nach Start/Monat/Jahr; keine wiederkehrenden Fehlerlogs. |
| M5 – Erste nutzbare Version A | Stabiler Core-Build, UI-/Diplomatie-/Militärtests, Save/Load, Zehnjahreslauf | Vergleichsmessungen zeigen nutzbare Verbesserung bei New Game und Simulation. |
| M6 – Inhaltsreduktion B | Nur nachweislich unnötige Daten/Scriptaufrufe entfernt | Jede Eingriffsgruppe einzeln gemessen; benötigte Modfunktionen bestehen. |
| M7 – Kartenprototyp C | Kleiner valider Ausschnitt und dokumentierter Generierungsweg | Karte, Nodes, Häfen, Wege, Save/Load funktionieren; Wirkung separat gemessen. |
| M8 – Europakarte und Abschluss | Auf 25 Länder ausgeweitete kleine Karte oder konkret dokumentierter Kartenblocker | Keine offenen Referenzen; Regressionstests und Messvergleich; Versionsmaske konkretisieren. |

**Nächste konkrete Arbeit ist M1**, danach M2. Keine große Kartenkonvertierung beginnen, bevor Loader-Isolation und Messbasis funktionieren.

## 13. Messverfahren: Startup und Simulation auseinanderhalten

Vier Zeiten separat führen:

1. **Prozessstart → Hauptmenü bedienbar.** Erfasst Engine-/Asset-/Datenladeanteile. Nicht einfach „Launcher klicken“ bis irgendwann ins Spiel messen.
2. **Neues Spiel starten → pausierte Spielwelt bedienbar.** Identische Auswahl und dokumentierter Startzeitpunkt; Aufbau des neuen Setups isolieren.
3. **Save laden → pausierte Spielwelt bedienbar.** Nur eigene Teststände, weil New Game und Save/Load unterschiedliche Kosten haben.
4. **365 Tage simulieren.** Gleiche Geschwindigkeit, Kamera/Zoom, ausgewähltes Land und Grafiksettings; zusätzlich mehrere Jahre zur Erfassung langsamer Monats-/Jahreswechsel.

Vergleichsreihen: lokale Referenz ohne diese Mod, A, A+B, später A+B+C. Danach gezielter Vergleich „Umgebung + zu testende Mod“. In allen Reihen nur die ausdrücklich vorgesehenen Mods; andere Overhauls nicht unbemerkt mitlaufen lassen. DLCs und Betrieb mit/ohne Debug-Modus separat ausweisen.

Mindestens einen Warmup und fünf verwertbare Wiederholungen pro Konfiguration und Phase. Reihenfolge abwechseln, damit Cache- und Temperaturzustände nicht systematisch nur einer Variante helfen. Gleicher Build, gleiche Einstellungen, Netzteil-/Energieprofil, keine parallelen Installationen. Debug-/Profiler-Läufe diagnostisch nutzen, normale Leistung separat ohne zusätzliche Debuglast messen.

**Kaltstart** nur so benennen, wenn der Cache-/Neustartzustand kontrolliert wurde; ansonsten „erster Start der Sitzung“. **Warmstart** separat nach geladenen Caches. Keine Cacheverzeichnisse oder bestehenden Saves zum Messen löschen. Die tatsächlich getestete Ausgangskonfiguration und bekannte lokale Installationsänderungen dokumentieren.

Median und Spannweite ausweisen, dazu Peak Working Set/Private Bytes soweit zuverlässig erfasst, Save-Größe, erzeugte/aktive Länder, Pop-Gruppen, Märkte und Einheiten. Prozessspeicher gleichartig messen; Dateigröße ist kein RAM-Verbrauch. Änderungen der Tickzeit nicht allein der Länderzahl zuschreiben: auch Pops und Kriege wurden verändert. Zusätzliche isolierte Vergleichsläufe nur für offene Ursachenfragen.

Anfangsziele für die Planung: **mindestens 30 % kürzere New-Game-Ladezeit und 50 % weniger Zeit für 365 Tage Simulation** gegenüber der dokumentierten Referenz. Diese Schwellen sind gewünschte Abnahmewerte, keine Vorhersage. Nach der Baseline begründet anpassen, falls die Engine einen großen unveränderlichen Anteil hat. Für Prozessstart bis Hauptmenü keinen Prozentgewinn vor Messung versprechen.

[benchmarks/template.csv](../benchmarks/template.csv) enthält nur Spaltenköpfe und keine erfundenen Messwerte. Belege, Logs und Screenshots werden je Lauf daneben abgelegt.

## 14. Validierung und visuelle Abnahme

Vor dem ersten Start statisch prüfen: ausgeglichene Struktur, aufgelöste Includes, gültige Tags/Orte/Kulturen/Religionen/Dynastien, Referenzreihenfolge, vollständig eindeutiges Eigentum, keine ausgeschlossenen Instanzen, zehn Märkte und kein Verweis auf gelöschte Ziele. Anfangsbudgets aus Abschnitt 7 überprüfen und jede Überschreitung begründen.

Im Spiel mit einem **neuen eigenen Teststand** beginnen. Über das Playset und die sichtbare Auswahl belegen, dass der eigene Bookmark aktiv ist. Politische Europakarte und Außenwelt, Frankreich/Deutschland/Großbritannien/Italien, Wirtschafts- und Marktansicht prüfen. Danach exemplarisch die kleinen Randstaaten Portugal, Norwegen, Finnland und Livland. Wirtschaft, Pops, Bau, Regierung, Charaktere, Diplomatie und Militär öffnen; exemplarische Handels-/Truppenbewegung nur im Teststand ausführen.

Märkte und Außenwelt nach Tag 1, Monat 1 und Jahr 1 erneut zählen. Save unter neuem Namen anlegen und laden. Mindestens zehn Jahre simulieren; bei ruhig erwartetem Verlauf automatische Neuerzeugung von Staaten, Märkten und Organisationen beobachten. Kriegstests gesondert ausführen, damit sie die ruhige Performance-Reihe nicht vermischen.

Fehlerlogs mit einer zuvor archivierten Referenz vergleichen: keine neuen Parse-/Missing-ID-Fehler, kein periodischer Scope-Fehlerspam, keine Crash-Schleifen. Bestehende Fehler als solche kennzeichnen und nicht pauschal dieser Mod zurechnen.

Für jegliche Navigation gelten [Screenshot-Verifikation](../../.docs/eu5_screenshot_verification.md) und [EU5-Shortcuts](../../.docs/eu5_shortcuts.md): vor jeder Eingabe aktuellen sichtbaren Zustand prüfen, danach erneut screenshotten. Vorhandene Nutzersaves und laufender ungesicherter Fortschritt werden nicht überschrieben oder verworfen. Endbericht nennt Build, Playset, Land, Datum, Profil, Messverfahren und die tatsächlich gezeigten Screenshots.

## 15. Kompatibilität und Grenzen der Testaussage

GUI-, Wirtschafts- und allgemeine Scriptmods sind das vorrangige Einsatzgebiet. Historische Missionen, weltweite Handelsnetze, Kolonial- und Regionsmods benötigen ggf. den größeren Referenzdatensatz. Die Umgebung ersetzt keinen abschließenden Test in der Welt, für die eine Mod veröffentlicht wird.

Mit anderen Setup-/Bookmark-/Karten-Overhauls sind gezielte Integrationen nötig. Ladepriorität im verwendeten Modsystem prüfen und tatsächlich überschreibende Dateien auflisten; keine pauschale Regel „immer zuletzt laden“ ohne Nachweis. Ein separates `quiet`-Profil darf Kriege/Seuchen für UI-Messungen begrenzen, muss seine Eingriffe aber offenlegen und die normale `core`-Simulation erhalten.

Performance-Schalter wie „KI komplett aus“, weltweite unendliche Vorräte oder täglich wiederholte Reparaturschleifen gehören nicht in das Standardprofil. Sie können Probleme verbergen und erzeugen unrepräsentative Modtests. Der Kern der Optimierung bleibt eine kleine, konsistente Welt, die von Anfang an weniger Objekte und weniger historische Sonderlogik benötigt.
