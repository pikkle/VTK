VTK - Visualisation du développement de l'embryon de la souris
==============================================================

Loïc Serafin
------------

Ce laboratoire est en deux parties:
- Une visualisation de l'évolution de l'embryon d'une souris en 4 étapes (ts10, ts11, ts12 et ts13)
- Une visualisation à l'étape ts14 des différents organes

Pour la première partie (fichier evolution.py), les embryons sont affichés comme des volumes, en appliquant une fonction
par morceaux d'opacité. Cette fonction d'opacité a été obtenue en regardant les résultats directement avec le programme
Paraview.
Le stage 13 n'est pas à la même échelle que les trois premiers et s'affiche en plus petit. Ne sachant pas à quel ratio
ce changement d'échelle se fait, j'ai laissé les données telles quelles.


Pour la seconde partie (fichier organs.py), la même méthode a été utilisée, mais la palette de couleur a été adaptée
pour afficher des couleurs différentes dans les différents segments scalaires correspondants aux différentes régions
intéressantes. L'opacité des régions intermédiaires à ces régions est à 0, ce qui nous permet de bien voir les régions
internes. Les régions n'étant pas définies très clairement, et incluant des zones très différentes (ex: le scalaire 226
qui définit la vésicule optique définit également des points sur le derme de l'embryon), une opacité très faible a été
adaptée pour chacune de ces régions, pour ne rendre visible que le noyau central de l'organe.
À noter que les deux carotides ne sont pas bien définis, et s'attribuent à la même zone que pour la vésicule optique.


Dans les deux parties, les volumes sont rendus avec du RayCasting.
