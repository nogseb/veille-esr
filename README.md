# Veille Concurrents & ESR — TBS Education

Site statique de veille courte, sélective et sourcée. Destination : **https://nogues.app/veille-esr/**.

## Ce que contient le site

Une édition courante, des éditions précédentes conservées en Archives, une cible de 8 à 10 signaux, plafond de 10, trois suites proposées au maximum, les huit axes, la méthode et les sources. Les recommandations sont à valider. Aucune ancienne édition ou performance concurrente n’est inventée.

Le site ne contient ni base de données, ni formulaire, ni script de mesure d’audience. La police Manrope est hébergée localement ; sa licence est fournie avec les assets.

## Structure

| Dossier | Rôle |
| --- | --- |
| `content/editions.json` | Paramètres du site, huit axes et éditions structurées |
| `content/sources.csv` | Corpus complémentaire de sources vérifiées |
| `assets/` | CSS, JavaScript, police locale, favicon et image de partage |
| `scripts/build.py` | Générateur statique, sans dépendance Python externe |
| `scripts/serve.py` | Aperçu local, y compris sous `/veille-esr/` |
| `scripts/check.py` | Contrôle des données, pages et liens locaux |
| `scripts/test-interactions.cjs` | Tests des filtres, états vides, menu et impression, avec Node.js |
| `scripts/social.html` | Source éditable de l’image de partage |
| `dist/` | Fichiers compilés à publier uniquement dans le sous-répertoire cible |

## Construire et prévisualiser

Python 3.11 ou ultérieur est suffisant pour compiler le site. Les assets, y compris la police et l’image de partage, sont déjà présents.

```bash
python3 scripts/build.py
python3 scripts/check.py
python3 scripts/serve.py
```

Ouvrir `http://localhost:3000/veille-esr/`. La compilation n’appelle aucun service de génération et ne nécessite aucune clé. Le rendu des pages est disponible dans le HTML initial ; JavaScript gère les filtres, le menu, le thème, l’impression et les quatre facettes ; la lecture de tous les contenus reste possible sans JavaScript.

## Ajouter une édition

Ajouter un objet dans le tableau `editions` de `content/editions.json`. Utiliser un identifiant et une date ISO uniques. Le générateur choisit automatiquement la date la plus récente pour l’accueil et crée une page permanente pour chaque édition. La section Archives liste seulement les éditions antérieures ; l’édition courante n’y est pas étiquetée comme archive. Les contenus précédents restent inchangés.

Viser 8 à 10 signaux, avec un plafond de 10 et sans remplissage artificiel, hors champ compris, et zéro à trois suites. Chaque signal doit comporter un axe principal, son statut, des dates qualifiées, un fait, une implication, une limite et au moins une source HTTPS. Les suites pointent vers un signal de la même édition. `featuredSignal` désigne explicitement l’identifiant du signal majeur ; sa source est utilisée dans la carte principale. Vérifier la cohérence de `featuredTitle`, `featuredFact`, `featuredLabel` et `featuredNote` avec ce signal.

Les chiffres d’affichage se recalculent à partir de l’édition. La durée de lecture reste indicative et doit être revue par l’éditeur. Ne pas transformer une première observation de page non datée en nouveauté hebdomadaire.

Les contrôles structurels s’exécutent avec Python seul. `python3 scripts/test-editions.py` vérifie les archives, le statut du lien permanent et les périodes de collecte explicites, sans enregistrer d’édition fictive. Les tests d’interaction s’exécutent avec `node scripts/test-interactions.cjs`. Le workflow du dépôt source utilise Python 3.11 et Node.js 22 pour ces contrôles ; il ne publie pas le site sur OVHcloud.

## Publication via GitHub, sur l’hébergement existant

**nogues.app n’est pas hébergé sur GitHub Pages.** Au moment de l’intégration, le domaine est servi par Apache sur OVHcloud. Le dépôt `nogseb/nogues.app` contient un workflow GitHub Actions existant qui publie `site/` en SFTP à la racine du domaine, sans supprimer les autres fichiers.

Les responsabilités restent distinctes :

- `nogseb/veille-esr` conserve le code, les données éditoriales et les fichiers compilés ;
- `nogseb/nogues.app` reçoit **seulement** le contenu compilé dans `site/veille-esr/` et déclenche son workflow existant.

Aucun changement de DNS, de GitHub Pages, de secrets ou de workflow racine n’est nécessaire. L’accueil et sa carte Veille ESR sont préservés. **Un push dans `veille-esr` seul ne met pas à jour l’hébergement OVHcloud.** Après validation éditoriale et compilation, le contenu de `dist/` doit aussi être reporté dans `site/veille-esr/` du dépôt de publication.

Ne jamais copier `.git`, les sources, des secrets ou des notes internes dans le répertoire publié. Ne jamais effectuer de synchronisation avec suppression à la racine du domaine. Le workflow existant et ses secrets restent dans le dépôt principal.

La génération hebdomadaire du contenu n’est pas automatisée dans cette version. Le workflow déploie les fichiers approuvés ; il ne réalise pas la recherche de veille.

## Portabilité et références

Les liens de navigation et ressources des pages normales sont relatifs, pour fonctionner sous `/veille-esr/`. Les canoniques, le sitemap et les métadonnées sociales utilisent explicitement `https://nogues.app/veille-esr/`. Le `.htaccess` local fournit la page d’erreur du sous-site et désactive le listing de répertoires ; il ne modifie pas le `.htaccess` racine.

Direction éditoriale inspirée de [veilleiaweb.digital](https://veilleiaweb.digital/). Police [Manrope](https://fonts.google.com/specimen/Manrope), distribuée sous SIL Open Font License. Les sources factuelles figurent dans chaque signal et sur la page Sources.

## Thèmes d’affichage

Le site s’ouvre en **mode sombre par défaut**, y compris lorsque le système du lecteur utilise un thème clair. Le bouton « Clair » / « Sombre » de l’en-tête permet de basculer ; seule cette préférence est mémorisée dans `localStorage`, sous la clé `veille-esr-theme`. Aucune donnée de mesure n’est transmise. Un choix clair déjà enregistré reste prioritaire lors des visites suivantes.

Le thème est appliqué avant le chargement des styles pour éviter un flash clair. Sans JavaScript, le sombre reste le thème initial et le bouton non fonctionnel est masqué. Si le stockage est bloqué, la bascule fonctionne toujours pour la page courante. Les règles d’impression restent claires. Les assets CSS et JavaScript sont versionnés dans les URL à partir de leur contenu pour éviter un mélange de versions en cache.

Tous les H1 associent **Oswald Bold (700, droit)** pour les parties blanches en mode sombre et **Playfair Display ExtraBold Italic (800)** pour les parties rouges. Le thème clair conserve des titres foncés lisibles ; les tailles restent adaptatives via CSS `clamp()`, qui règle la taille et ne désigne pas une police. Les autres niveaux de titres et textes restent en Manrope. Les vraies variantes typographiques sont hébergées localement, avec leurs licences SIL Open Font License : [Oswald](https://fonts.google.com/specimen/Oswald) et [Playfair Display](https://fonts.google.com/specimen/Playfair+Display).

## Format éditorial élargi

L’édition test du 15 octobre 2026 est enrichie à neuf signaux couvrant les huit axes. Le format vise 8 à 10 signaux, avec un plafond technique de 10 ; il n’impose pas une fausse nouveauté dans chaque axe. Trois suites prioritaires maximum sont conservées. Le tableau `editorialPolicy` centralise les plafonds.

Chaque signal renseigne `timing` : `week` (publication dans la fenêtre glissante de sept jours), `context` (publication antérieure) ou `observation` (dispositif observé). `publicationDate` est requis pour `week` et `context` ; `dateLabel` précise les dates d’annonce, d’événement, de données ou d’observation sans les confondre. Les cartes affichent ces distinctions sans devoir ouvrir les détails. Les champs optionnels `periodStart` et `periodEnd`, fournis ensemble, définissent explicitement la période de collecte (sept jours au maximum), indépendamment de la date de publication. Sans ces champs, les anciennes éditions conservent leur fenêtre glissante de sept jours incluant la date d’édition. Le générateur refuse une date incompatible avec le statut ou une période future.

`verdict` et `analysis` sont facultatifs et explicitement éditoriaux. Le résumé reste visible, les développements critiques sont repliables. Toutes les sources restent rattachées au signal et accessibles dans la page Sources ; leur nombre est calculé, pas codé en dur. Les performances non publiées ne sont pas déduites des dispositifs visibles.

## Lisibilité des textes

Les textes courants des signaux passent à 15 px et leurs implications à 14 px. Les accordéons utilisent des libellés de 13 px et un corps de 14 px, avec un interlignage de 1,8 ; le décryptage critique bénéficie de titres de 15 px. Les textes secondaires et les versions mobiles sont augmentés de façon cohérente. Les H1 et la composition typographique validée restent inchangés ; les styles d’impression ne sont pas agrandis par cette évolution.

Le bloc « L’essentiel en 30 secondes » synthétise les dynamiques de l’environnement ESR et concurrentiel en une centaine de mots maximum. Son socle est un panorama analytique, enrichi ponctuellement d’un fil rouge. Il ne contient ni recommandations pour TBS Education, ni comptage des signaux ou des sources. Les implications opérationnelles restent dans les cartes et les suites proposées ; les différences de périmètre et de calendrier ne sont pas gommées.

## Quatre facettes en pied de page

Le tableau `perspectives` de chaque édition contient quatre lectures : `panorama`, `fil-rouge`, `tensions`, `concurrence`, dans cet ordre. Chaque lecture a un nom, une question, un texte et les identifiants des signaux auxquels revenir. Le premier texte doit être identique au résumé `intro`. Le générateur refuse une incohérence ou une référence à un signal inexistant. Les pages secondaires montrent la dernière édition datée ; une archive utilise ses propres lectures. Aucun module supplémentaire sur les pages d’erreur.

Le module est un prisme 3D à quatre faces, avec boutons de sélection directe, navigation fléchée, compteur et pause/reprise. Rotation automatique toutes les 24 secondes seulement lorsque le module est visible, sans survol ni focus, en onglet visible. Un choix manuel met la rotation en pause. Les faces inactives sont `inert` et retirées de la lecture assistée ; un repli `tabindex` exclut leurs liens du clavier même sans prise en charge native d’`inert`, puis restaure leur comportement lors de l’activation. La préférence de mouvement réduit désactive la rotation automatique et les transitions. Sans JavaScript et à l’impression, les quatre lectures sont affichées en cartes statiques. `node scripts/test-perspectives.cjs` vérifie la logique, également dans GitHub Actions.

Le fond « Cartographie des signaux » est une proposition optionnelle, désactivée par défaut. Le bouton permet de l’essayer et de le désactiver ; courbes et points CSS locaux restent derrière les contenus, sans intercepter les interactions. L’animation s’arrête en onglet masqué et devient statique avec les mouvements réduits. Aucun appel tiers ou stockage supplémentaire n’est ajouté.
