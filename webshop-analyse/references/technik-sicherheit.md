# Technik, Hosting & Sicherheit – passiver Check

Ziel: Shopsystem, Versionen, Hosting und E-Mail-Absicherung ermitteln und mit öffentlich bekannten Sicherheitslücken abgleichen – ausschließlich mit öffentlich abrufbaren Informationen. Nichts aktiv testen: keine Formulare absenden, keine Logins, keine Port- oder Schwachstellenscans, keine Exploit-Versuche, keine Pfade „erraten“, die nicht standardmäßig öffentlich sind. Das Ergebnis dient dem Betreiber zur Absicherung.

## 1. Shopsystem und Plugins erkennen
- Meta-Generator-Tags im Seitenkopf (WebFetch liefert sie als `meta-generator`), z. B. Page-Builder- oder Shopsystem-Namen mit Versionsnummer; Hinweise auf Shopify, Shopware, JTL, WooCommerce, Magento.
- Unterschiedliche Generator-Versionen auf verschiedenen Seiten deuten auf Seiten-Cache oder Beta-Versionen hin – erwähnen.
- WordPress-Plugins: öffentliche `readme.txt` unter `/wp-content/plugins/<slug>/readme.txt` (z. B. `woocommerce`, `elementor-pro`). Das ist eine Standarddatei, kein versteckter Pfad.

## 2. Version sauber bestimmen
Achtung Falle: Das Feld „Stable tag“ in einer readme ist nicht zuverlässig die installierte Version (bei WooCommerce bleibt es z. B. auf der Vorversion stehen, während der Changelog schon die neue Version zeigt).
Vorgehen:
1. Oberste Changelog-Überschrift (Version + Datum) und „Stable tag“ notieren.
2. Mit der readme des offiziellen Release-Tags vergleichen, z. B. `https://raw.githubusercontent.com/woocommerce/woocommerce/<version>/plugins/woocommerce/readme.txt`. Identisch → Version gesichert.
3. Aktuelle Version beim Hersteller nachsehen (Release-Blog, Changelog).
4. Wenn die readme kaum Angaben hat (z. B. nur „Requires …“ und „Tested up to …“), daraus nur vorsichtig ableiten und als „nicht gesichert, im Backend prüfen“ kennzeichnen.

## 3. Hosting
- A-Record per DNS-over-HTTPS: `https://dns.google/resolve?name=<host>&type=A`; NS-Records analog (`type=NS`). Nameserver-Namen und das Feld „Comment“ verraten oft den Hoster.
- Betreiber des IP-Netzes über öffentliche Whois-/IP-Seiten bzw. Websuche nach IP oder Nameserver ermitteln.
- Einordnen: Shared Hosting/Managed/Cloud/SaaS, Standort (DSGVO-relevant).
- Bei gehosteten Shopsystemen (z. B. Shopify) patcht der Anbieter Plattform und Hosting; der Fokus verschiebt sich auf Konten (Zwei-Faktor-Authentifizierung), installierte Apps und E-Mail-Absicherung.

## 4. E-Mail-Absicherung (Domain)
Gefälschte Mails im Namen der Marke sind bei bekannten B2C-Shops oft das realistischste Risiko. Passiv prüfen:
- **SPF:** TXT-Record der Domain (`type=TXT`), Eintrag `v=spf1 …`; auf viele veraltete `include:`-Einträge und auf `+all`/`?all` achten.
- **DMARC:** TXT-Record von `_dmarc.<domain>`. `p=none` heißt: gefälschte Mails werden nicht abgewiesen; Empfehlung schrittweise `quarantine` → `reject`, mit Reporting (`rua=`).
- Optional: DNSSEC, CAA-Record.

## 5. Sicherheitslücken abgleichen
- Websuche nach „<Plugin> vulnerability <Jahr>“, Datenbanken: Patchstack, Wordfence Intelligence, CVE-Seiten.
- Tabelle: Lücke (Art, CVSS, verlinkt) | betroffene Versionen | behoben in | betrifft Kunden? (mit Begründung).
- Bedingungen der Ausnutzbarkeit nennen, soweit öffentlich bekannt und von außen sichtbar (z. B. „nur mit Formular mit Datei-Upload-Feld; Kontaktformular hat keins“). Keine Anleitung zur Ausnutzung wiedergeben.
- Aktiv ausgenutzte Lücken besonders hervorheben.

## 6. Sofortmaßnahmen (Checkliste)
Typisch: Backup, Update (erst Staging), Prüfung auf Kompromittierung (z. B. unbekannte Admins, verdächtige Dateien im betroffenen Upload-Verzeichnis), automatische Sicherheitsupdates, Firewall/Sicherheitsdienst, Cache leeren/keine Betas live, PHP-Version und kommende Mindestanforderungen, Zwei-Faktor-Authentifizierung für alle Admin-Konten, DMARC verschärfen, optional readme-Zugriff sperren (ersetzt keine Updates), Verantwortlichkeit für Updates klären.

## Formulierung
Ergebnissatz zuerst („Der Shop läuft auf X Version Y bei Hoster Z und ist von Lücke … betroffen; Update auf … sofort“), dann Methode in einem Satz („ausschließlich öffentlich abrufbare Dateien und DNS-Daten, nichts aktiv getestet“), dann Tabellen.
