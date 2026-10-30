---
name: webshop-analyse
description: Umfassende Business-, Website- und SEO-Analyse eines (Online-)Shops oder Unternehmens anhand seiner URL – mit Markt & Wettbewerb, SWOT, UX/Conversion, technischer SEO, passivem Technik- und Sicherheitscheck (Shopsystem-Version, Hosting, E-Mail-Absicherung, bekannte Lücken), deutschen Rechts-Quick-Wins, Keyword-Clustern, Content-, Social-Media- und Google-Ads-Strategie, Vertrieb (Marktplätze, Distributoren), Kostenhebeln und priorisiertem Maßnahmenplan als teilbares Dokument. Verwende diesen Skill immer, wenn jemand eine Website, einen Shop oder eine Firma „analysieren“, „durchleuchten“, „checken“ oder „bewerten“ lassen will, nach SEO-Ideen, Marketing- oder Vertriebsstrategie für eine konkrete URL fragt, eine Business-Analyse, Wettbewerbsanalyse oder einen Website-Audit möchte – auch wenn nur die URL mit „schau dir das mal an“ kommt. Also use for English requests like "analyze this website/shop" or "business and SEO audit for this URL".
---

# Webshop- & Business-Analyse

Ziel ist ein Dokument, mit dem ein Inhaber oder Berater sofort arbeiten kann: klare Befunde mit Belegen, konkrete Empfehlungen, ein priorisierter Plan. Kein Marketing-Blabla, keine erfundenen Zahlen.

Die Analyse ist für deutschsprachige Kunden gebaut (Recht, Förderung, Marktplätze in DE). Liegt der Shop in einem anderen Land, die länderspezifischen Teile (Recht, Förderung, Marktplätze) entsprechend anpassen oder als „nicht geprüft“ kennzeichnen.

## Grundprinzipien

- **Belegen statt behaupten.** Jede Aussage über die Website stammt aus einer tatsächlich abgerufenen Seite; jede Zahl über den Markt (Preise, Gebühren, Versionen, Fristen) aus einer abgerufenen Quelle, die im Dokument verlinkt ist. Was nicht geprüft wurde, wird als „nicht geprüft“ markiert – das ist wertvoller als eine plausible Vermutung, weil der Leser sonst auf Basis falscher Annahmen handelt.
- **Keine erfundenen Kennzahlen.** Suchvolumina, Klickpreise, Budgets, Ziel-Stückkosten oder Umsatzpotenziale nicht schätzen und als Fakt ausgeben. Stattdessen sagen, womit man sie ermittelt (Keyword Planner, Search Console, Angebotsrunde). Grobe Orientierungswerte nur mit Kennzeichnung „ungeprüfte Schätzung“.
- **Aktualität.** Rechtliche Pflichten, Plattformgebühren, Software-Versionen und Sicherheitslücken ändern sich laufend. Vor jeder solchen Aussage per Websuche den aktuellen Stand prüfen – auch wenn man ihn zu kennen glaubt. Die Prüflisten in `references/` tragen ein Stand-Datum; alles danach ist neu zu recherchieren.
- **Passiv bleiben bei Technik und Sicherheit.** Nur öffentlich abrufbare Dateien und Daten lesen (Seitenquelltext-Metadaten, readme.txt von Plugins, DNS). Nichts ausprobieren, keine Formulare absenden, keine Logins, keine Scans, keine Exploits. Der Sicherheitsteil dient dem Betreiber zur Absicherung; er ist für eigene Shops oder Shops von Auftraggebern gedacht. Konkrete Schwachstellen eines Shops gehören ins Dokument für den Betreiber, nicht in öffentliche Kanäle.
- **Keine Rechtsberatung.** Rechtliche Punkte als Hinweise mit Quelle formulieren und auf Anwalt bzw. Rechtstexte-Anbieter verweisen.
- **Sprache und Ton.** Deutsch (bzw. Sprache des Nutzers), sachlich, präzise. Jeder Abschnitt beginnt mit dem Ergebnis in einem Satz, dann Tabellen/Listen. Sätze kurz.

## Ausgabeform

1. **Claude-Dokument (Standard):** Wenn ein Docs-Werkzeug bzw. Docs-Skill verfügbar ist, diesen laden und befolgen: zuerst das Dokument-Gerüst mit allen geplanten Abschnitten als Platzhalter anlegen und öffnen, dann Abschnitt für Abschnitt füllen, während der Nutzer zusieht.
2. **Fallback:** Ohne Docs-Werkzeug eine Markdown-Datei (oder .docx, wenn der Nutzer Word verlangt) mit derselben Struktur erzeugen und dem Nutzer schicken.
3. **Chat-Antwort am Ende: höchstens etwa 120 Wörter.** Ein Satz Gesamturteil, dann die drei wichtigsten Befunde als Stichpunkte mit je einem Satz, optional ein Satz zur wichtigsten Prüfgrenze. Das Dokument trägt den Inhalt; eine lange Chat-Antwort wiederholt es nur und wird nicht gelesen. Keine Aufzählung der Abschnitte, keine Methodenbeschreibung.

## Ablauf

### 1. Website erfassen

Folgende Seiten abrufen (WebFetch), jeweils mit gezieltem Prompt nach Title, Meta-Description, H1/H2, Textmenge, Preisen, CTAs, Vertrauenselementen, Auffälligkeiten:

- Startseite
- eine Kategorie-/Übersichtsseite
- 1–2 Produkt- bzw. Leistungsseiten (Topprodukt zuerst)
- Über uns / Philosophie / Unternehmensseite
- Blog/News (Aktualität: Datum der Beiträge)
- Impressum (Rechtsform, Sitz, Verantwortliche, Hinweise wie OS-Plattform, TMG/DDG)
- AGB und Widerrufsbelehrung (Stand-Datum, veraltete Verweise, Widerrufsbutton)
- Kontakt (Formularfelder – relevant für Sicherheit)

Achte auf Widersprüche (z. B. unterschiedliche Mailadressen, Du/Sie-Mix, widersprüchliche FAQ-Aussagen, Tippfehler, leere Links „#“, veraltetes Copyright, alle Blogposts mit gleichem Datum, Debug-Texte oder Platzhalter im Shop) – solche Details machen die Analyse glaubwürdig und konkret.

### 2. Recherche

- **Unternehmen:** weitere Domains, Großhandelsprofile, Messen, B2B-Referenzen, Presse (Eigentümer, Umsatzentwicklung).
- **Wettbewerb:** Preisanker je Segment (Massenware, Marktplatz-Importe, Premium-Marken) mit verlinkter Quelle; wo sinnvoll Grundpreise (€/kg, €/Stück) vergleichen.
- **Rechtslage:** aktuelle Pflichten prüfen – siehe `references/recht-de.md`.
- **Technik & Sicherheit:** passiver Check – siehe `references/technik-sicherheit.md`.
- **Vertrieb:** aktuelle Gebühren der relevanten Marktplätze und passende Distributoren/Händler – siehe `references/vertrieb.md`. Vorher prüfen, ob der Shop dort schon präsent ist; dann geht es um Steuerung, nicht um Einstieg.

Recherche und Schreiben verzahnen: ein Abschnitt, sobald sein Material da ist – nicht erst alles sammeln.

### 3. Dokumentstruktur

Die Abschnitte und was in sie gehört, stehen in `references/abschnitte.md`. Lies die Datei, bevor du das Gerüst anlegst. Standard-Reihenfolge:

1. Executive Summary (Kernbefund + Top-5-Hebel)
2. Unternehmensprofil & Geschäftsmodell (inkl. Sortiment/Preise-Tabelle)
3. Markt, Zielgruppen & Wettbewerb
4. SWOT
5. Website-Analyse: UX, Conversion, Vertrauen, Content
6. Technische & On-Page-SEO-Analyse
7. Technik, Hosting & Sicherheit
8. Rechtliche Quick-Wins
9. SEO-Strategie & Keyword-Cluster
10. Content-Ideen
11. Social-Media-Strategie
12. Google Ads
13. Vertrieb: Marktplätze & Distributoren
14. Kostenhebel (Herstellung, Varianten, Versand, Shopsystem)
15. Weitere Ideen (Schutzrechte, Produkt, Service, Förderung)
16. Priorisierter Maßnahmenplan (Phasen, Abhängigkeiten, KPIs, offene Fragen)
17. Quellen & Methodik

Wenn der Nutzer den Umfang einschränkt („nur SEO“) oder nur eine schnelle Einschätzung will, nur die passenden Abschnitte anlegen – das spart viel Zeit. Abschnitte ohne verwertbares Material nicht aufblähen – ein Satz „nicht ermittelbar, weil …“ genügt.

### 4. Abschluss-Review

Bevor du fertig meldest, das Dokument einmal als kritischer Außenstehender lesen:

- Passt die Executive Summary noch zu allen Abschnitten (besonders nach Ergänzungen)?
- Tauchen Maßnahmen aus allen Abschnitten im Maßnahmenplan auf, mit sinnvoller Reihenfolge (Sicherheit und Recht zuerst)?
- Sind alle Zahlen belegt oder als Schätzung markiert, alle Quellen verlinkt?
- Gibt es Doppelungen oder Widersprüche zwischen Abschnitten?

### 5. Nachträge im Gespräch

Nutzer ergänzen oft Themen („bau noch Social Media ein“, „was ist mit Amazon?“, „wie senken wir die Produktionskosten?“). Dann:

- neuen Abschnitt an der logisch passenden Stelle einfügen (vor dem Maßnahmenplan),
- Executive Summary, SWOT, Maßnahmenplan und Quellen nachziehen, damit das Dokument in sich stimmig bleibt,
- im Chat kurz die Kernaussage nennen, nicht den Abschnitt wiederholen.

Unklare Begriffe (Tippfehler, verwechselte Produktnamen) freundlich auflösen und die Annahme im Chat nennen, nicht im Kundendokument.
