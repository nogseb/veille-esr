#!/usr/bin/env python3
"""Build the source-controlled ESR watch into a portable static website."""
import csv
import html
import json
import shutil
import hashlib
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
DATA = json.loads((ROOT / "content/editions.json").read_text(encoding="utf-8"))
AXES = {axis["id"]: axis for axis in DATA["axes"]}
EDITIONS = sorted(DATA["editions"], key=lambda item: item["date"], reverse=True)
SITE = DATA["site"]
BASE = SITE["url"]
POLICY = DATA["editorialPolicy"]
TIMING = {"week": "Actualité de la fenêtre", "context": "Contexte hors période", "observation": "Dispositif observé"}


def esc(value):
    return html.escape(str(value), quote=True)


def arrow():
    return '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none"><path d="M5 19 19 5M5 5h14v14" stroke="currentColor" stroke-width="1.7"/></svg>'


def external(url, label, css=""):
    if not url.startswith("https://"):
        raise ValueError(f"Invalid source URL: {url}")
    return f'<a class="{esc(css)}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)}{arrow()}<span class="sr-only"> (nouvel onglet)</span></a>'


def prefix(route):
    return "../" * len([part for part in route.split("/") if part]) or "./"


def asset(path, name):
    version = hashlib.sha256((ROOT / "assets" / name).read_bytes()).hexdigest()[:10]
    return f"{path}assets/{name}?v={version}"


def shell(route, title, description, body, active="edition", edition=None):
    p = prefix(route)
    nav = [("edition", "", "La veille"), ("archives", "archives/", "Archives"),
           ("axes", "axes/", "Les 8 axes"), ("sources", "sources/", "Sources"),
           ("methode", "methode/", "La méthode")]
    nav_links = []
    for key, path, label in nav:
        current = ' aria-current="page"' if key == active else ""
        nav_links.append(f'<a href="{p}{path}"{current}>{label}</a>')
    links = "".join(nav_links)
    canonical = BASE + route
    robots = '<meta name="robots" content="noindex">' if route == "404/" else ""
    social_image = BASE + asset("", "social.png")
    return f'''<!doctype html>
<html lang="fr" data-theme="dark">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} — TBS Education</title><meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">{robots}
<meta name="theme-color" content="#111410">
<script src="{asset(p, 'theme-init.js')}"></script>
<meta property="og:type" content="website"><meta property="og:site_name" content="Veille Concurrents & ESR">
<meta property="og:title" content="{esc(title)} — TBS Education"><meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}"><meta property="og:image" content="{social_image}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)} — TBS Education">
<meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{social_image}">
<link rel="icon" type="image/svg+xml" href="{asset(p, 'favicon.svg')}"><link rel="stylesheet" href="{asset(p, 'styles.css')}">
<link rel="stylesheet" href="{asset(p, 'theme.css')}">
<script src="{asset(p, 'app.js')}" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Aller au contenu</a>
<header class="site-header"><div class="header-inner">
<a class="wordmark" href="{p}" aria-label="Veille Concurrents et ESR, accueil"><span class="brand-symbol" aria-hidden="true"></span><span>VEILLE<span class="wordmark-small">CONCURRENTS & ESR</span></span></a>
<nav id="navigation" aria-label="Navigation principale">{links}</nav>
<div class="header-actions"><button class="theme-toggle" type="button" data-theme-toggle aria-pressed="true" aria-label="Activer le mode clair" hidden><svg class="theme-sun" aria-hidden="true" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.6"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.4 1.4M17.6 17.6 19 19M5 19l1.4-1.4M17.6 6.4 19 5" stroke="currentColor" stroke-width="1.6"/></svg><svg class="theme-moon" aria-hidden="true" viewBox="0 0 24 24" fill="none"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4 8.5 8.5 0 1 0 20 14.5Z" stroke="currentColor" stroke-width="1.6"/></svg><span class="theme-label">Clair</span></button><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="navigation">Menu <span aria-hidden="true">+</span></button></div>
<span class="org">TBS Education</span>
</div></header>
<main id="main">{body}</main>
<footer class="site-footer"><div class="footer-inner"><div><span class="footer-brand">VEILLE CONCURRENTS & ESR</span><p>Surveiller largement. Publier peu. Décider mieux.</p></div><div class="footer-links"><a href="{p}methode/">Méthode & limites</a><a href="https://veilleiaweb.digital/" target="_blank" rel="noopener noreferrer">La veille IA & Web {arrow()}</a><a href="https://nogues.app/">nogues.app {arrow()}</a></div></div><div class="footer-bottom"><span>TBS Education · Prototype éditorial sourcé</span><span>Sans cookies de suivi · Sans mesure d’audience</span></div></footer>
</body></html>'''


def filter_controls(items, label):
    tabs = '<button type="button" class="filter-button is-active" data-filter="all" aria-pressed="true">Tous</button>'
    tabs += "".join(f'<button type="button" class="filter-button" data-filter="{esc(axis["id"])}" aria-pressed="false">{esc(axis["short"])}</button>' for axis in items)
    return f'<div class="filter-bar" role="group" aria-label="{esc(label)}">{tabs}</div>'


def card(signal, number):
    axis = AXES[signal["axis"]]
    source = signal["sources"][0]
    sources = external(source["url"], source["publisher"], "source-link")
    source_details = "".join(f'<li>{external(source["url"], source["name"])}<span>{esc(source["type"])} · {esc(source["date"])}</span></li>' for source in signal["sources"])
    dark = " outside-card" if signal["axis"] == "horschamp" else ""
    heading = '<span class="outside-label">REGARD HORS ESR</span>' if dark else ""
    timing = signal["timing"]
    verdict = f'<p class="editorial-verdict"><strong>Notre lecture</strong> · {esc(signal["verdict"])}</p>' if signal.get("verdict") else ""
    analysis = ""
    if signal.get("analysis"):
        paragraphs = "".join(f'<section><h4>{esc(item["title"])}</h4><p>{esc(item["text"])}</p></section>' for item in signal["analysis"])
        analysis = f'<details class="proof-details analysis-details"><summary>Lire le décryptage critique <span aria-hidden="true">+</span></summary><div class="details-content"><p class="analysis-notice">Appréciation éditoriale · ne mesure pas les résultats de l’établissement.</p>{paragraphs}</div></details>'
    return f'''<article class="signal-card{dark}" data-axis="{esc(signal["axis"])}" id="signal-{esc(signal["id"])}">
<div class="card-top"><span class="axis-label">{esc(axis["number"])} — {esc(axis["name"])}</span><span class="intent">{esc(signal["label"])}</span></div>
{heading}<h3>{esc(signal["title"])}</h3><div class="timing-line"><span class="timing-badge timing-{timing}">{TIMING[timing]}</span><span>{esc(signal["dateLabel"])}</span></div><p class="signal-fact">{esc(signal["fact"])}</p>
<div class="implication"><span>POUR TBS EDUCATION</span><p>{esc(signal["implication"])}</p></div>
{verdict}
<div class="card-bottom"><span class="proof-label">{esc(signal["status"])}</span>{sources}</div>
{analysis}
<details class="proof-details"><summary>Dates, sources & limites <span aria-hidden="true">+</span></summary><div class="details-content"><p class="source-date">{esc(signal["dateLabel"])}</p><p>{esc(signal["limits"])}</p><ul>{source_details}</ul></div></details>
</article>'''


def edition_body(edition, permanent=False):
    signals = edition["signals"]
    main_signals = [signal for signal in signals if signal["axis"] != "horschamp"]
    outside = [signal for signal in signals if signal["axis"] == "horschamp"]
    sources_count = len({source["url"] for signal in signals for source in signal["sources"]})
    featured_signal = next(signal for signal in signals if signal["id"] == edition["featuredSignal"])
    source = featured_signal["sources"][0]
    label = "ARCHIVE · " if permanent else ""
    controls = filter_controls(DATA["axes"], "Filtrer les signaux par axe")
    cards = "".join(card(signal, i) for i, signal in enumerate(main_signals, 1))
    cards += "".join(card(signal, len(main_signals) + i) for i, signal in enumerate(outside, 1))
    actions = "".join(f'''<article class="action-card"><span class="action-number">0{i}</span><div><span class="action-horizon">{esc(action["horizon"])} · À VALIDER</span><h3>{esc(action["title"])}</h3><p class="action-owner">{esc(action["owner"])}</p><p><strong>Livrable attendu</strong> · {esc(action["result"])}</p></div></article>''' for i, action in enumerate(edition["actions"], 1))
    coverage = "".join(f'<li><strong>{esc(AXES[key]["name"])}</strong><span>{esc(value)}</span></li>' for key, value in edition.get("coverage", {}).items())
    timing_summary = " · ".join(f'{sum(signal["timing"] == key for signal in signals)} {name}' for key, name in [("week", "actualités de la fenêtre"), ("context", "sujets de contexte"), ("observation", "dispositifs observés")])
    action_heading = {0: "Aucune suite à engager par défaut.", 1: "Une piste. Pas un engagement.", 2: "Deux pistes. Pas deux engagements.", 3: "Trois pistes. Pas trois engagements."}[len(edition["actions"])]
    return f'''<section class="hero container">
<div class="edition-meta"><span class="live-dot" aria-hidden="true"></span><span>{label}{esc(edition["status"]).upper()} · {esc(edition["dateLabel"])} </span><span class="meta-period">Fenêtre {esc(edition["period"])}</span></div>
<div class="hero-grid"><div class="hero-title"><p class="eyebrow">TBS EDUCATION / RADAR HEBDOMADAIRE</p><h1>CONCURRENCE.<br>SECTEUR.<br><span>DÉCISIONS.</span></h1><p class="hero-subtitle">L’essentiel de ce qui change.<br>Et ce que nous pouvons en faire.</p></div>
<aside class="featured"><span class="featured-kicker">LE SIGNAL À RETENIR · {TIMING[featured_signal["timing"]].upper()}</span><p class="featured-number">{esc(edition["featuredFact"])}</p><h2>{esc(edition["featuredTitle"])}</h2><p class="featured-note">{esc(edition["featuredNote"])}</p><div class="featured-bottom"><span>{esc(edition["featuredLabel"])}</span>{external(source["url"], source["publisher"])}</div></aside></div>
<div class="edition-strip"><div><strong>{len(signals):02d}</strong><span>signaux sélectionnés</span></div><div><strong>{len(edition["actions"]):02d}</strong><span>suites proposées</span></div><div><strong>{edition["readingMinutes"]:02d}<small> min</small></strong><span>pour lire l’essentiel</span></div><div><strong>{sources_count:02d}</strong><span>sources consultables</span></div></div>
</section>
<section class="summary-box container" aria-labelledby="summary-title"><div><p class="eyebrow">LE POINT DE DÉPART</p><h2 id="summary-title">L’essentiel<br>en 30 secondes.</h2></div><p>{esc(edition["intro"])}</p></section>
<section class="signals-section container" data-filter-scope aria-labelledby="signals-title"><div class="section-head"><div><p class="eyebrow">UNE SÉLECTION, PAS UNE REVUE DE PRESSE</p><h2 id="signals-title">Ce qui mérite votre attention.</h2></div><span class="section-counter" data-result-count aria-live="polite">{len(signals)} signaux</span></div><p class="timing-summary">{esc(timing_summary)}. Les sujets antérieurs et non datés ne sont pas présentés comme des nouveautés.</p>{controls}<div class="signals-grid">{cards}</div><div class="empty-state" hidden><span class="empty-mark" aria-hidden="true">—</span><h3>Aucun signal retenu sur cet axe.</h3><p>La sélection est volontairement courte. Ce n’est pas une preuve d’absence d’actualité.</p><a href="{('../..' if permanent else '.')}/axes/">Comprendre le périmètre des huit axes {arrow()}</a></div></section>
<section class="actions-section container" aria-labelledby="actions-title"><div class="section-head"><div><p class="eyebrow">DE LA VEILLE À LA SUITE UTILE</p><h2 id="actions-title">{action_heading}</h2></div><span class="section-tag">PROPOSITIONS À ARBITRER</span></div><div class="actions-grid">{actions}</div><p class="fine-print">Pilotes, données et disponibilité à confirmer. Aucun suivi d’actions antérieures n’est simulé pour cette édition test.</p></section>
<section class="coverage-box container"><details><summary><span>Ce que couvre — et ne couvre pas — cette édition</span><span aria-hidden="true">+</span></summary><p>{esc(edition["notice"])}</p><ul>{coverage}</ul><p>Les {len(signals)} signaux incluent le regard hors ESR ; celui-ci n’est pas nécessairement une nouveauté de semaine.</p></details></section>
<div class="edition-footer container"><span>Publication : {esc(edition["dateLabel"])} · Europe/Paris</span><div><button type="button" class="text-button" data-print>Imprimer cette édition</button><a href="{('../..' if permanent else '.')}/editions/{esc(edition["id"])}/">Lien permanent {arrow()}</a></div></div>'''


def page_intro(kicker, title, intro):
    return f'<section class="page-intro container"><p class="eyebrow">{esc(kicker)}</p><h1>{title}</h1><p>{esc(intro)}</p></section>'


def archives_body():
    cards = "".join(f'''<a class="archive-card" href="../editions/{edition["id"]}/"><div><span class="archive-date">{esc(edition["dateLabel"])}</span><span class="archive-status">{esc(edition["status"])}</span></div><h2>{esc(edition["title"])}</h2><p>Fenêtre {esc(edition["period"])} · {len(edition["signals"])} signaux · {len(edition["actions"])} suites</p><span class="archive-cta">Lire l’édition {arrow()}</span></a>''' for edition in EDITIONS)
    return page_intro("LA MÉMOIRE DE LA VEILLE", "Les éditions.<br><span>Sans perdre le fil.</span>", "Retrouver chaque sélection dans son contexte, avec sa période, ses sources et ses limites.") + f'<section class="container archive-grid">{cards}</section><p class="container fine-print archive-note">Une seule édition est publiée à ce stade. Aucune archive antérieure n’a été créée artificiellement.</p>'


def axes_body():
    cards = "".join(f'''<article class="axis-card"><span class="axis-number">{esc(axis["number"])}</span><h2>{esc(axis["name"])}</h2><p>{esc(axis["description"])}</p><div class="axis-question">{esc(axis["question"])}</div></article>''' for axis in DATA["axes"])
    return page_intro("LE PÉRIMÈTRE", "Sept regards sur l’ESR.<br><span>Un pas de côté.</span>", "Les axes structurent la collecte, pas huit rubriques à remplir. Un sujet garde un axe principal ; les autres dimensions restent des tags.") + f'<section class="container axes-grid">{cards}</section>' + '''<section class="container editorial-note"><h2>Des frontières claires.</h2><div class="boundary-grid"><div><h3>Offre ≠ acquisition</h3><p>Ce qui est proposé et selon quelles conditions, d’un côté. La manière d’attirer et de faire progresser vers la candidature, de l’autre.</p></div><div><h3>Marque ≠ réputation</h3><p>La promesse et sa démonstration, d’un côté. Les reconnaissances et la trajectoire institutionnelle, de l’autre.</p></div><div><h3>International ≠ marché</h3><p>Le mouvement d’un établissement sur une destination, d’un côté. Les évolutions des flux ou règles sectorielles, de l’autre.</p></div></div></section>'''


def method_body():
    return page_intro("LA MÉTHODE", "Moins de bruit.<br><span>Plus de discernement.</span>", "Une veille utile distingue le fait, notre lecture et la suite possible. Le décryptage critique est une appréciation éditoriale, pas une preuve de performance.") + '''<section class="container method-grid"><article class="method-card"><span>01 / COLLECTER</span><h2>Partir des sources.</h2><p>Établissements, institutions, prestataires, partenaires étrangers et supports publics. Une source d’agence documente une contribution revendiquée, pas un ROI.</p></article><article class="method-card"><span>02 / QUALIFIER</span><h2>Garder les bonnes dates.</h2><p>Date de publication, événement, période des données et consultation ne sont pas interchangeables. Trois statuts restent visibles : actualité de la fenêtre, contexte hors période, dispositif observé. Une échéance active ne transforme pas une ancienne annonce en nouveauté. Une page non datée est une observation, pas une nouveauté prouvée.</p></article><article class="method-card"><span>03 / SÉLECTIONNER</span><h2>Publier peu.</h2><p>Une cible de 8 à 10 signaux, avec un plafond de 10, hors champ compris. Aucun remplissage pour atteindre le volume. La couverture des axes est recherchée ; un sujet sans preuve suffisante n’est pas ajouté. Le résumé se lit en 30 secondes, le décryptage détaillé reste optionnel.</p></article><article class="method-card"><span>04 / DÉCIDER</span><h2>Proposer une suite bornée.</h2><p>Zéro à trois recommandations : vérifier, comparer, tester ou surveiller. Pilote proposé, résultat attendu et horizon indicatif ; aucun engagement automatique des équipes.</p></article></section><section class="container editorial-note"><h2>Ce que cette veille ne promet pas.</h2><div class="boundary-grid"><div><h3>Pas d’exhaustivité</h3><p>Une absence de signal retenu ne signifie pas une absence d’activité. Les limites de couverture restent explicites.</p></div><div><h3>Pas de performance inventée</h3><p>Une campagne visible ne donne ni son coût d’acquisition ni son taux de conversion. Un investissement annoncé ne mesure pas un impact.</p></div><div><h3>Pas d’automatisation active</h3><p>Cette version contient l’édition test du 15 octobre 2026. La préparation et la publication de nouvelles éditions restent soumises à une validation éditoriale.</p></div></div></section><section class="container method-bottom"><h2>Un regard hors ESR, avec une limite.</h2><p>Une mécanique extérieure est retenue pour sa proximité avec un problème de TBS Education. Sa transposition reste une hypothèse à tester, pas une promesse de résultats identiques.</p><h2>Une publication de veille, pas une prise de position officielle.</h2><p>Les analyses et suites sont des propositions de travail. Elles ne remplacent ni les modalités approuvées des programmes, ni une expertise juridique, ni les décisions des équipes.</p><h2>Vie privée.</h2><p>Ce site ne dépose aucun cookie de suivi, ne charge aucun outil de mesure d’audience et ne collecte aucune donnée par formulaire. Le thème sombre est activé par défaut. Si vous changez de thème, seule cette préférence est enregistrée dans le stockage local du navigateur ; aucune donnée de mesure n’est envoyée. Les liens de sources ouvrent des sites tiers, dont les règles peuvent être différentes. Une police locale ou les polices de votre système assurent l’affichage sans service tiers.</p></section>'''


def sources_body():
    rows = list(csv.DictReader((ROOT / "content/sources.csv").open(encoding="utf-8", newline=""), delimiter=";"))
    cards = []
    mapping = {"Marque et preuves": "marque", "Acquisition et conversion": "acquisition", "International et implantation": "international"}
    for row in rows:
        cards.append(f'''<article class="source-card" data-axis="{mapping[row['axe']]}"><div class="source-card-top"><span>{esc(row['axe'])}</span><span class="source-type">{esc(row['type'])}</span></div><h2>{esc(row['source'])}</h2><p>{esc(row['signal_observable'])}</p><div class="source-context"><p><strong>Statut</strong> · {esc(row['date_publication_ou_statut'])}</p><p><strong>Limite</strong> · {esc(row['limite'])}</p></div>{external(row['url'], 'Consulter la source', 'source-visit')}</article>''')
    controls = filter_controls([AXES[key] for key in ("marque", "acquisition", "international")], "Filtrer le corpus de sources")
    references = {source["url"]: source for signal in EDITIONS[0]["signals"] for source in signal["sources"]}
    primary = "".join(f'<li>{external(source["url"], source["publisher"] + " — " + source["name"])}<span>{esc(source["type"])} · {esc(source["date"])}</span></li>' for source in references.values())
    return page_intro("LA TRAÇABILITÉ", "Des sources.<br><span>Pas des suppositions.</span>", "Les références de l’édition et un corpus complémentaire pour mieux couvrir marque, acquisition et international.") + f'''<section class="container primary-sources"><h2>Les {len(references)} références de l’édition enrichie.</h2><ul>{primary}</ul></section><section class="container sources-section" data-filter-scope><div class="section-head"><div><p class="eyebrow">CORPUS COMPLÉMENTAIRE</p><h2>Élargir le regard.</h2></div><span class="section-counter" data-result-count aria-live="polite">{len(rows)} sources</span></div><p class="section-description">Pages consultées le 15 octobre 2026. Les bibliothèques publicitaires sont documentées, mais aucun inventaire d’annonces d’école n’a été interrogé. Les pages historiques restent des références, pas des actualités de semaine.</p>{controls}<div class="source-grid">{''.join(cards)}</div><div class="empty-state" hidden><h3>Aucune source dans cette sélection.</h3></div></section>'''


def write_page(route, page):
    folder = OUT / route
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "index.html").write_text(page, encoding="utf-8")


def validate_data():
    for edition in EDITIONS:
        date.fromisoformat(edition["date"])
        if len(edition["signals"]) > POLICY["maxSignals"] or len(edition["actions"]) > POLICY["maxActions"]:
            raise ValueError("Editorial caps exceeded")
        ids = {signal["id"] for signal in edition["signals"]}
        if len(ids) != len(edition["signals"]):
            raise ValueError("Duplicate signal ID")
        if edition.get("featuredSignal") not in ids or not edition.get("featuredLabel"):
            raise ValueError("Featured card must point to a signal and provide a factual label")
        for signal in edition["signals"]:
            if signal["axis"] not in AXES or not signal["sources"]:
                raise ValueError("Invalid axis or missing source")
            if signal.get("timing") not in TIMING:
                raise ValueError("Missing or invalid temporal qualification")
            if signal["timing"] in ("week", "context"):
                published = date.fromisoformat(signal["publicationDate"])
                elapsed = (date.fromisoformat(edition["date"]) - published).days
                if (signal["timing"] == "week" and not 0 <= elapsed <= 6) or (signal["timing"] == "context" and elapsed <= 6):
                    raise ValueError("Publication date conflicts with temporal qualification")
        if any(action["signal"] not in ids for action in edition["actions"]):
            raise ValueError("Action points to an unknown signal")


def main():
    validate_data()
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "assets", OUT / "assets", dirs_exist_ok=True)
    latest = EDITIONS[0]
    write_page("", shell("", "Veille Concurrents & ESR", SITE["description"], edition_body(latest)))
    routes = [("", "La veille"), ("archives/", "Archives"), ("axes/", "Les huit axes"), ("methode/", "La méthode"), ("sources/", "Sources")]
    write_page("archives/", shell("archives/", "Archives de la veille Concurrents & ESR", "Retrouver les éditions de veille, leurs sources et leurs suites proposées.", archives_body(), "archives"))
    write_page("axes/", shell("axes/", "Les huit axes de veille", "Sept axes concurrentiels et ESR, plus un regard hors champ pour enrichir les décisions.", axes_body(), "axes"))
    write_page("methode/", shell("methode/", "Méthode et limites de la veille", "Une méthode de collecte, qualification et sélection pour une veille courte et fiable.", method_body(), "methode"))
    write_page("sources/", shell("sources/", "Sources de veille Concurrents & ESR", "Sources de l’édition test et corpus alternatif pour marque, acquisition et international.", sources_body(), "sources"))
    for edition in EDITIONS:
        route = f'editions/{edition["id"]}/'
        routes.append((route, f'Édition du {edition["dateLabel"]}'))
        write_page(route, shell(route, f'Veille du {edition["dateLabel"]}', edition["title"], edition_body(edition, True), edition=edition))
    missing = page_intro("PAGE INTROUVABLE", "Ce lien n’existe pas.<br><span>Revenons à l’essentiel.</span>", "L’adresse demandée ne correspond à aucune page de veille.") + '<div class="container missing-link"><a href="../">Revenir à la veille actuelle</a></div>'
    write_page("404/", shell("404/", "Page introuvable", "Cette page n’existe pas.", missing))
    error_html = shell("", "Page introuvable", "Cette page n’existe pas.", missing.replace('href="../"', 'href="./"'))
    error_html = error_html.replace(f'<link rel="canonical" href="{esc(BASE)}">', '<meta name="robots" content="noindex">')
    error_html = error_html.replace('href="./', 'href="/veille-esr/').replace('src="./', 'src="/veille-esr/')
    (OUT / "404.html").write_text(error_html, encoding="utf-8")
    manifest = {"routes": [{"path": "/" + path, "title": title} for path, title in routes]}
    (OUT / "manus-routes.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "\n".join(f'<url><loc>{esc(BASE + path)}</loc><lastmod>{latest["date"]}</lastmod></url>' for path, _ in routes)
    (OUT / "sitemap.xml").write_text(sitemap + '\n</urlset>\n', encoding="utf-8")
    (OUT / ".htaccess").write_text('DirectoryIndex index.html\nErrorDocument 404 /veille-esr/404.html\nOptions -Indexes\n', encoding="utf-8")
    (OUT / ".nojekyll").touch()
    print(f"Built {len(routes)} pages in {OUT}; {len(latest['signals'])} signals and {len(latest['actions'])} proposed actions.")


if __name__ == "__main__":
    main()
