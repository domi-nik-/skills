# webshop-analyse

*A Claude Agent Skill (German) that turns a shop or company URL into a sourced business, website and SEO analysis with a prioritised action plan — tailored to the German market.*

Ein [Claude Agent Skill](https://support.claude.com/en/articles/12512176-what-are-skills), der aus einer Shop- oder Firmen-URL eine belegte Business-, Website- und SEO-Analyse mit priorisiertem Maßnahmenplan macht – zugeschnitten auf deutsche Shops.

Ergebnis ist ein teilbares Dokument (Claude-Dokument, sonst Markdown/Word) mit bis zu 17 Abschnitten:

Executive Summary · Unternehmensprofil & Sortiment · Markt, Zielgruppen & Wettbewerb · SWOT · Website (UX, Conversion, Vertrauen) · Technische & On-Page-SEO · Technik, Hosting & Sicherheit · Rechtliche Quick-Wins · Keyword-Cluster · Content-Ideen · Social Media · Google Ads · Marktplätze & Distributoren · Kostenhebel · Weitere Ideen · Maßnahmenplan · Quellen

## Was den Skill ausmacht

- **Belegt statt geschätzt:** Jede Zahl (Preise, Gebühren, Versionen, Fristen) kommt aus einer abgerufenen, verlinkten Quelle. Suchvolumina, Klickpreise oder Budgets werden nicht erfunden; Ungeprüftes wird als „nicht geprüft“ markiert.
- **Passiver Sicherheitscheck:** Shopsystem- und Plugin-Versionen, Hosting und E-Mail-Absicherung (SPF/DMARC) werden nur aus öffentlich abrufbaren Dateien und DNS-Daten ermittelt und mit bekannten Sicherheitslücken abgeglichen – ohne Scans, Logins oder Formular-Tests.
- **Deutsche Rechtslage:** Prüfliste u. a. zu OS-Plattform, DDG, Greenwashing-Verboten (EmpCo), Widerrufsbutton, Garantielabel, GPSR, WEEE, Barrierefreiheit.
- **Wächst im Gespräch:** Ergänzungen („bau noch Social Media ein“, „lohnt sich Amazon?“) werden als Abschnitt eingefügt; Summary, SWOT und Maßnahmenplan werden nachgezogen.

## Beispiele

- *„Bitte mach eine Businessanalyse und Webseiten-Analyse inkl. SEO-Ideen für https://www.example-shop.de“*
- *„Schau dir mal https://www.example-shop.de an – lohnen sich Amazon und Co., und wie steht's um Technik und Sicherheit?“*
- *„Nur SEO und Content für https://www.example-shop.de, bitte kurz.“*

Eine vollständige Analyse dauert erfahrungsgemäß 20–30 Minuten, weil viele Seiten abgerufen und Quellen geprüft werden. Mit eingeschränktem Umfang geht es deutlich schneller.

## Inhalt

```
webshop-analyse/
├── SKILL.md                      # Ablauf, Grundprinzipien, Ausgabeform
└── references/
    ├── abschnitte.md             # was in jeden der 17 Abschnitte gehört
    ├── technik-sicherheit.md     # passiver Technik-, Hosting- und Sicherheitscheck
    ├── recht-de.md               # rechtliche Prüfliste Deutschland (mit Stand-Datum)
    └── vertrieb.md               # Marktplätze, Distributoren, Händlergewinnung
```

## Installation

Siehe [Installationsanleitung im Repo-README](../README.md#how-to-install-a-skill). Fertige `.skill`-Dateien gibt es auf der [Releases-Seite](https://github.com/domi-nik-/skills/releases), sobald ein Release getaggt ist.

Der Skill nutzt Websuche und Webseitenabruf; beides muss in Claude aktiviert sein.

## Grenzen und Hinweise

- **Keine Rechtsberatung.** Die Rechtsliste trägt ein Stand-Datum und veraltet; der Skill weist Claude an, jeden Punkt vor Verwendung neu zu recherchieren. Rechtliche Punkte immer von Anwalt oder Rechtstexte-Anbieter prüfen lassen.
- **Nur für eigene Shops oder im Auftrag.** Der Sicherheitsteil ist für Betreiber und deren Berater gedacht. Gefundene Schwachstellen gehören in das Dokument für den Betreiber, nicht in öffentliche Kanäle.
- **Keine internen Daten.** Ohne Zugriff auf Analytics, Search Console oder Umsatzzahlen bleiben Ladezeiten, Rankings und Umsatzpotenziale ungemessen – das steht dann so im Dokument.
- **Deutschland-Fokus.** Für Shops in anderen Ländern werden Recht, Förderung und Marktplätze angepasst oder als „nicht geprüft“ gekennzeichnet.

## Lizenz

[MIT](./LICENSE)
