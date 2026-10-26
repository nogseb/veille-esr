# Site Veille Concurrents & ESR — TBS Education

- [x] Site éditorial responsive inspiré de veilleiaweb.digital, en Bento box sobre, rouge #FF3e52 et nom TBS Education écrit en entier. Lecture rapide et contenu dans le HTML initial. Six pages publiques et assets locaux.
- [x] Intégrer l’édition test du 15 octobre 2026 : cinq signaux au maximum, trois suites proposées au maximum, dates et sources qualifiées, inspiration IKEA explicitement hors actualité. Les recommandations ne sont pas des actions engagées. JSON, HTML et compteurs contrôlés.
- [x] Structurer les huit axes sans obliger leur présence dans chaque édition. Filtres fonctionnels, états vides honnêtes, présentation de la méthode et de la couverture. Tests d’interaction réussis.
- [x] Archives et page d’édition permanente ; page des huit axes et de la méthodologie ; page des sources. Une seule édition réelle, aucune ancienne édition fictive ni note interne brute publiée.
- [x] Site autonome sans base de données, cookies de suivi ou scripts tiers. Données éditoriales structurées et procédure simple de mise à jour hebdomadaire. README et workflow de vérification fournis.
- [x] Fonctionnement sous /veille-esr/ et liens/ressources relatifs, avec métadonnées correspondant à https://nogues.app/veille-esr/. Publication HTTPS200, contenu initial complet pour Googlebot/Twitterbot, route inconnue404/noindex. Redirection du chemin sans slash301 vers HTTPS port443 standard puis200.
- [x] Code sur le dépôt public existant nogseb/veille-esr. Commit source 1eaad034b3cf2416e549c60d507fcf95e6fe4b8e ; workflow de vérification réussi : https://github.com/nogseb/veille-esr/actions/runs/38799985704 . Dépôt géré conservé séparément pour la prévisualisation.
- [x] Créer uniquement site/veille-esr/ dans nogseb/nogues.app et réutiliser son workflow de publication OVHcloud. Commit de publication 1d6840bf58cbf5d5cb139a40aab74e915490758e. Workflow et transfert SFTP réellement réussis : https://github.com/nogseb/nogues.app/actions/runs/38799989747 . Accueil et changements concurrents préservés, aucun changement DNS ou secrets.
- [x] Présenter l’aperçu et le contenu exact avant le push public et le déclenchement de publication. Confirmation explicite « Publier cette version » reçue le 15 octobre 2026 à 22:11 Europe/Paris.
- [x] Vérifier pages, liens locaux, filtres, contenu, chemins et publication réelle après autorisation. Six pages, CSS, JavaScript, police, image de partage et sitemap publiés comparés octet par octet aux fichiers approuvés. La production hebdomadaire des nouvelles éditions n’est pas automatisée.

## Évolution du 15 octobre — mode sombre

- [x] Mode sombre par défaut dès le HTML initial, indépendamment du thème système, sur toutes les pages y compris les archives et erreurs. Préserver le rouge #FF3e52 et les contenus approuvés.
- [x] Bouton de bascule clair/sombre accessible dans l’en-tête, sur desktop et mobile. Conserver uniquement la préférence de thème dans le stockage local, sans cookie de suivi ; fonctionner aussi lorsque le stockage est bloqué.
- [x] Appliquer les contrastes à toutes les surfaces et aux sources/détails/filtres. L’impression reste claire et lisible. Aucun changement d’offre, de données ou de source.
- [x] Tester la bascule, la préférence enregistrée et le fonctionnement sans stockage, puis republier par le circuit GitHub/OVHcloud existant sans modifier l’accueil ni les autres sous-sites.

Publication vérifiée le 15 octobre 2026 à 22:19 Europe/Paris : source `1c2e10b`, publication `82ec10a`. CI et transfert SFTP réussis ; six pages et trois assets de thème comparés aux fichiers compilés. Tests de préférence, stockage bloqué et contrastes principaux réussis. Accueil de nogues.app préservé.

## Évolution du 15 octobre — titre Playfair Display

- [x] Appliquer Playfair Display uniquement à « DÉCISIONS » dans le titre principal, en conservant le rouge et Manrope pour « CONCURRENCE » et « SECTEUR ».
- [x] Héberger la police et sa licence localement, préserver les thèmes clair/sombre et le circuit de publication existant, puis vérifier les fichiers publiés.

Publication vérifiée : source `bc51126`, déploiement `624b72f`. Accueil, édition permanente, CSS, police et licence en ligne identiques aux fichiers compilés ; CI et SFTP réussis.

## Évolution du 15 octobre — point rouge

- [x] Remplacer les trois barres du repère de veille par un gros point rouge dans l’en-tête, sur desktop et mobile, et adapter le favicon au même signe. Préserver le rouge existant, le titre Playfair Display et les thèmes.
- [x] Publier cette modification ciblée par les dépôts existants, puis vérifier le logo et le favicon en ligne sans modifier l’accueil de nogues.app.

Publication vérifiée : source `4310791`, déploiement `662cb42`. Logo rond 34px sur desktop, 28px sur mobile, favicon assorti et versionné. Contrôles et transfert SFTP réussis ; thème sombre et Playfair Display préservés.

## Évolution du 15 octobre — format élargi et axes complétés

- [x] Passer à une cible de 8 à 10 signaux hebdomadaires, plafond 10, hors champ compris, sans abaisser les exigences de source ni simuler des actualités. Maintenir trois suites prioritaires maximum. Cette édition enrichie comporte neuf signaux et couvre les huit axes.
- [x] Ajouter Marque et preuves : analyse critique du changement de marque SKEMA du 21 septembre 2026, distinguant les faits, notre appréciation et les résultats non publiés. Mobiliser les deux sources fournies, sans reprendre les visuels protégés dans le site.
- [x] Ajouter Acquisition et conversion : observation du parcours BBA international EDHEC et de l’offre Early Bird KEDGE. Décrire leurs mécanismes, limites et pistes pour TBS Education ; ne pas inventer de gains de conversion ni recommander automatiquement une remise.
- [x] Ajouter International : Audencia Barcelone, explicitement campus collaboratif hébergé chez ESCI-UPF et non campus autonome. Marquer la publication du 17 septembre hors fenêtre. Écarter le double diplôme EDHEC–Tampa dont le lancement était déjà annoncé en 2025.
- [x] Rendre visibles les statuts « actualité de la semaine », « contexte hors période » et « observation de dispositif ». Conserver un résumé de 30 secondes et développer la critique SKEMA sur demande dans la carte, pour ne pas allonger la lecture rapide.
- [x] Harmoniser méthode, compteurs, sources, documentation et contrôles avec le nouveau plafond. Préserver mode sombre, point rouge, titre Playfair Display et pages existantes.
- [x] Présenter l’aperçu et le contenu exact des nouvelles analyses avant le push public et la publication. La première validation ne portait pas sur cette nouvelle critique ni les nouvelles recommandations ; aucun push public de la version enrichie avant confirmation. Confirmation « Publier la version enrichie » reçue le 15 octobre à 22:54 Europe/Paris.

Contrôles : neuf signaux / huit axes / onze références uniques ; quatre actualités, trois contextes, deux observations. Lecture principale : 1 437 mots, sept minutes indicatives. Revue ciblée terminée ; seul écart relevé, visuel de partage resté à cinq signaux, corrigé et régénéré. Confirmation du nouveau contenu reçue, puis publication effectuée et vérifiée.

Publication confirmée le 15 octobre 2026 à 22:56 Europe/Paris : source `0d01d8f`, déploiement `c29cf2a`. Vérification CI réussie (run 38805783854), transfert OVHcloud SFTP réussi (run 38805786649). Six pages, styles et visuel de partage en ligne identiques aux fichiers approuvés. Neuf signaux, huit axes, trois suites, onze références ; répartition 4 actualités / 3 contextes / 2 observations. Accueil et changements concurrents de nogues.app préservés.

## Évolution du 15 octobre — combinaison typographique H1

- [x] Appliquer Oswald Bold (700, droit) aux parties blanches des H1 et Playfair Display ExtraBold Italic (800, vraie italique) aux parties rouges de tous les H1, y compris pages secondaires et erreurs. Préserver la lisibilité du thème clair, les tailles adaptatives, le point rouge et les contenus.
- [x] Héberger les deux polices avec leurs licences sans appel tiers à l’affichage, tester les règles CSS et les glyphes accentués, puis publier via le circuit GitHub/OVHcloud et vérifier les ressources en ligne.

Publication vérifiée : source `8249b87`, déploiement `4e4be4b`. CI et SFTP réussis ; six pages, styles, deux polices et image de partage contrôlés en ligne. Vraies graisses et italique vérifiés dans les métadonnées des polices ; glyphes français disponibles.

## Évolution du 15 octobre — lisibilité des textes

- [x] Augmenter légèrement les corps de texte et les microtextes sur toutes les pages, desktop et mobile, sans modifier la taille ou les polices H1 validées. Conserver le contenu, le point rouge et les deux thèmes.
- [x] Renforcer les libellés et contenus des accordéons, notamment « Lire le décryptage critique » et « Dates, sources & limites », avec un interlignage confortable et des zones de clic suffisantes. Ne pas conserver de petites surcharges mobiles annulant l’augmentation.
- [x] Préserver la mise en page et l’impression, publier via le circuit GitHub/OVHcloud existant, puis vérifier styles et pages en ligne.

Publication confirmée : source `031c3da`, déploiement `fc826bf`. Contrôles GitHub et SFTP réussis. Textes des signaux à 15 px, implications et contenus d’accordéons à 14 px ; libellés à 13 px. Six pages contrôlées à 320, 390, 800, 900 et 1440 px ; débordements détectés à 320 px dans l’en-tête et les compteurs corrigés, puis chemins concernés recontrôlés. H1 et contenu préservés ; six pages et deux feuilles de style identiques en ligne.

## Évolution du 15 octobre — résumé stratégique en 30 secondes

- [x] Remplacer la description du nombre et du statut des sources par des enseignements utiles pour TBS Education : preuves de différenciation et clarté des parcours de candidature.
- [x] Expliquer la portée du recul national de l’apprentissage en français direct : il ne permet pas de conclure à la même baisse chez TBS Education ; vérifier nos propres candidatures et contrats avant d’ajuster les messages.
- [x] Mettre à jour l’accueil et la page permanente de l’édition, sans modifier les signaux ni leurs sources, puis publier et contrôler le texte en ligne.

Publication vérifiée : source `d22c92d`, déploiement `9819710`. CI et transfert SFTP réussis. Résumé de 84 mots identique sur l’accueil et la page permanente, sans modification des neuf signaux, de leurs sources ni des suites proposées. Changements concurrents de l’accueil principal préservés.

## Évolution du 15 octobre — panorama et quatre facettes

- [x] Rédiger et publier « L’essentiel en 30 secondes » selon l’angle 1, panorama analytique, enrichi ponctuellement de l’angle 2, fil rouge : synthèse et compréhension de l’environnement, pas recommandations à TBS Education ni inventaire des sources. Préserver les faits, dates, références et neuf signaux.
- [x] Créer en pied de page une animation à quatre facettes : « Le panorama analytique — Que retenir de cette édition ? », « Le fil rouge — Qu’est-ce qui relie les sujets ? », « Les tensions du secteur — Quelles dynamiques faut-il lire ensemble ? », « La lecture concurrentielle — Sur quels terrains les écoles cherchent-elles à se distinguer ? ». Les textes analysent l’édition datée, avec un prisme 3D, sélection directe et pause/reprise.
- [x] Garantir un fonctionnement accessible : arrêt automatique au survol/focus, hors écran ou onglet masqué, pause après choix manuel, mouvement réduit respecté, quatre lectures consultables sans JavaScript et à l’impression, thèmes et responsive conservés.
- [x] Proposer « Cartographie des signaux », fond de courbes et points rouges animé lentement, désactivé par défaut et essayable au moyen d’un bouton. Aucun suivi, stockage nouveau, ressource tierce ou interaction bloquée ; fond statique en mouvement réduit.
- [x] Publier dans les dépôts existants, préserver les changements concurrents et vérifier les pages et les assets en ligne.

Publication vérifiée le 15 octobre à 23:37 Europe/Paris : source `b56cbec`, déploiement `665550c`. CI et SFTP réussis ; six pages et deux assets d’animation identiques en ligne. Résumé de 93 mots, quatre lectures datées reliées aux signaux ; neuf signaux et onze sources inchangés. Contrôles des commandes à 320/390/800/1440 px, mouvement réduit, impression et JavaScript désactivé réussis. Revue ciblée : repli clavier ajouté et testé sans inert natif. Le fond reste une proposition désactivée par défaut, activable au moyen du bouton.

## Évolution du 26 octobre — S44 et archives

- [x] Constituer une édition « S44 — point au 26 octobre » avec collecte principale du 20 au 26 octobre, huit axes recherchés, Hyperhumain et L’Antisèche inclus dans le repérage public, 8–10 signaux visés sans remplissage, sources et limites traçables.
- [ ] Préserver intégralement l’objet de l’édition du 15 octobre et son lien permanent ; le déplacer hors de l’accueil dans la section Archives lorsque la nouvelle édition est publiée.
- [x] Adapter les formulations du prototype devenues inexactes après une deuxième édition, sans modifier le design, les polices, les thèmes ou les animations.
- [x] Préparer la nouvelle édition avec panorama analytique, quatre facettes, zéro à trois suites et contrôles existants réussis ; distinguer aperçu, sauvegarde et publication réelle.
- [ ] Publier seulement le périmètre autorisé dans les deux dépôts, après validation du contenu public si nécessaire ; vérifier l’accueil et les deux liens permanents en ligne.

État au 26 octobre : aperçu préparé avec dix signaux, huit axes, trois suites, résumé de 97 mots et quatre facettes. Fenêtre explicite du 20 au 26 octobre ; un contexte ESSCA daté du 1er octobre pour l’inauguration prévue le 28. Édition du 15 octobre strictement inchangée en données et accessible en archive. Huit tests de dates et d’archives, contrôles HTML et tests d’interaction réussis. Le déplacement en Archives est prêt dans l’aperçu ; aucune nouvelle publication publique avant validation du contenu S44.
