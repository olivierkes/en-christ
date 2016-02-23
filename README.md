# En Christ
> De l'identité en crise
> À l'identité en Christ

Une étude biblique sur l'épître aux éphésiens.

# [Demo](http://www.theologeek.ch/en-christ)

# T'aime pas ma théologie?

J'ai crée ce guide et cette étude pour ma paroisse, mais rien ne vous empêche de le reprendre et le modifier, pour l'adapter à une autre sujet, ou pour corriger toutes les hérésies que j'y ai mises.

Parce que c'est libre.

#### C'est quoi ce truc en fait?

C'est fondamentalement un générateur de site static bricolé au couteau suisse pour satisfaire mes besoins. Ca prend le contenu du dossier `src` écrit en `txt2tags` pour en faire un joli site mobile-friendly.

Il suffit de remplacer ces contenus par autre chose pour en faire un site mobile friendly sur vos recettes de cuisine préférée.

# Comment ça marche?

#### Dépendances

- [python 3](http://www.python.org)
- [txt2tags](http://www.txt2tags.org): pour le markup
- [feedparser](https://pypi.python.org/pypi/feedparser) (optionel)
- `make` optionel mais fortement recommendé

#### Cloner le repo (ou [téléchargez-le](https://github.com/olivierkes/en-christ/archive/master.zip)):
```sh
git clone git@github.com:olivierkes/en-christ.git
```

#### Contenu
Il y a un certains nombre de chose que vous n'aurez pas à toucher. Voilà ce qui vous intéresse:

- `scripts/generate.py`: pour remplacer les infos par les vôtres
- `src/`: c'est la que le contenu se trouve
- `www/img/`: pour les images

#### Rédaction

La rédaction se fait dans `src`.

- `src/TOC.csv` est la table des matières, qui référence les fichiers `*.t2t` que vous créez.
- Le marckup t2t est un peu modifié, des shortcodes ont été créez. Si le besoin se fait sentir (ce qui m'étonnerai) je ferais une vraie doc, sinon regardez un peu comment moi je les utilise.

#### Générer le site
Pour compiler le bouzin:

    make generate

Si vous ne voulez pas utiliser `make`: je prie pour vous. Mais vous pouvez vous en sortir en:

- **Compilant chaque fichier `*.t2t`:** `txt2tags -C inc/settings.t2t -H -i src/NOM.t2t -o src/NOM.html`
- **Générant le site:** `python3 scripts/generate.py`
