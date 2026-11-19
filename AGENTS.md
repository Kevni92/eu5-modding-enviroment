# eu5-modding-enviroment

Die globale `../AGENTS.md` gilt zusätzlich.

- Zweck: kleine, schnelle EU5-Testwelt für Modentwicklung. Kein historischer Overhaul.
- Aktueller Stand: Planung und lesendes Quellenaudit. Keine ausführbare Performance-Reduktion vorhanden.
- Vor Implementierung `docs/IMPLEMENTIERUNGSPLAN.md` und `docs/QUELLENBEFUND.md` lesen.
- Länder- und Marktziele stehen in `config/scenario.json`. Die Gebietsbeschreibungen sind noch keine vollständige Location-Zuordnung.
- Spieldateien ausschließlich lesen. Generatoren dürfen nur in dieses Mod-Verzeichnis schreiben; Installationsdateien, andere Mods, Saves und Playsets bleiben unangetastet.
- Eigentum, Pops, Märkte und Charaktere im Setup reduzieren, bevor die Welt erzeugt wird. Keine weltweite Annexions-/Löschschleife als Performance-Lösung.
- Strukturierte EU5-Dateien mit einem Parser bearbeiten, der Kommentare, Strings, wiederholte Schlüssel, anonyme Listen und Includes berücksichtigt. Regex allein ist kein Setup-Generator.
- Ein neuer Dateiname oder ein leerer Mod-Ordner entfernt keine Vanilla-Einträge. Überschreibungen, Ordnerersetzung, Includes und DLC-Beiträge explizit prüfen.
- Länderdefinitionen, aktive Startländer und technische Sonderländer getrennt zählen; `type = pop` und `type = building` berücksichtigen.
- Messwerte niemals aus Dateigrößen oder Eintragszahlen ableiten. Kaltstart, Warmstart, neues Spiel und Simulation getrennt ausweisen.
- Kartenverkleinerung ist ein eigener Meilenstein. Eine leere Weltkarte bleibt eine Weltkarte.
- Jede Aussage als Quellenbefund, Planungsentscheidung, Hypothese oder Laufzeitergebnis kennzeichnen. Versionsmaske erst nach Prüfung des konkreten Spielbuilds festlegen.
- Spielnavigation und visuelle Verifikation gemäß `../.docs/eu5_screenshot_verification.md` und `../.docs/eu5_shortcuts.md`.
