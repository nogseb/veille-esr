# Veille Concurrents & ESR — TBS Education

Site statique de veille courte, sélective et sourcée. Destination : **https://nogues.app/veille-esr/**.

## Ce que contient le site

Une édition test du **15 octobre 2026**, cinq signaux au maximum, trois suites proposées au maximum, des archives réelles, les huit axes, la méthode et les sources. Les recommandations sont à valider. Aucune ancienne édition ou performance concurrente n’est inventée.

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

Ouvrir `http://localhost:3000/veille-esr/`. La compilation n’appelle aucun service de génération et ne nécessite aucune clé. Le rendu des pages est disponible dans le HTML initial ; JavaScript sert uniquement aux filtres, au menu et à l’impression.

## Ajouter une édition

Ajouter un objet dans le tableau `editions` de `content/editions.json`. Utiliser un identifiant et une date ISO uniques. Le générateur choisit automatiquement la date la plus récente pour l’accueil et crée une page permanente pour chaque édition.

Conserver cinq signaux maximum, hors champ compris, et zéro à trois suites. Chaque signal doit comporter un axe principal, son statut, des dates qualifiées, un fait, une implication, une limite et au moins une source HTTPS. Les suites pointent vers un signal de la même édition. `featuredSignal` désigne explicitement l’identifiant du signal majeur ; sa source est utilisée dans la carte principale. Vérifier la cohérence de `featuredTitle`, `featuredFact`, `featuredLabel` et `featuredNote` avec ce signal.

Les chiffres d’affichage se recalculent à partir de l’édition. La durée de lecture reste indicative et doit être revue par l’éditeur. Ne pas transformer une première observation de page non datée en nouveauté hebdomadaire.

Les contrôles structurels s’exécutent avec Python seul. Les tests d’interaction s’exécutent avec `node scripts/test-interactions.cjs`. Le workflow du dépôt source utilise Python 3.11 et Node.js 22 pour ces contrôles ; il ne publie pas le site sur OVHcloud.

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

Playfair Display est hébergée localement, avec sa licence SIL Open Font License, et utilisée uniquement pour « DÉCISIONS » dans le titre principal. « CONCURRENCE », « SECTEUR » et les autres textes restent en Manrope. Source : [Google Fonts — Playfair Display](https://fonts.google.com/specimen/Playfair+Display).
