# Tkinter-TP : éditeur de carrés et de lignes
 
Petite application Tkinter pour créer des carrés sur un canvas, les relier par des lignes coudées et les déplacer à la souris sur une grille aimantée. Certains carrés sont "anarchistes" et fuient la souris.
 
## Fonctionnalités
 
- **Carrés** : le bouton `carre` crée un carré au centre du canvas (impossible s'il y en a déjà un à cet endroit).
- **Carrés anarchistes** : 1 carré sur 4 est créé avec le tag `anarchiste`. Il s'enfuit de 50 px quand la souris le survole.
- **Déplacement** : glisser-déposer d'un carré avec la souris.
- **Grille aimantée** : au relâchement, le carré se cale sur la grille (largeur du canvas / 10).
- **Anti-chevauchement** : si le carré tombe sur un autre carré, il retourne à sa position initiale.
- **Lignes** : le bouton `ligne` relie deux carrés choisis au hasard avec une ligne en "L" (horizontale puis verticale). Les lignes suivent les carrés quand ils bougent.
- **Ovals** : chaque ligne a un oval à son coude, qu'on peut attraper et déplacer pour modifier le tracé. Deux ovals ne peuvent pas se chevaucher.
- **Suppression** :
  - clic droit sur un carré : supprime le carré et toutes ses lignes
  - clic droit sur une ligne : supprime la ligne et son oval
- **Effacer tout** : touche `Echap`, avec confirmation.
- **Fermeture** : une fenêtre de confirmation s'ouvre avant de quitter.
- **Redimensionnement** : les carrés sont mis à l'échelle quand la fenêtre change de taille.
## Lancer le projet
 
Prérequis : Python 3 avec Tkinter (inclus par défaut sur Windows et macOS ; sous Linux : `sudo apt install python3-tk`).
 
```bash
git clone https://github.com/<ton-pseudo>/<ton-repo>.git
cd <ton-repo>
python main.py
```
 
Aucune dépendance externe : uniquement `tkinter` et `random` de la bibliothèque standard.
 
## Commandes
 
| Action | Commande |
|---|---|
| Créer un carré | Bouton `carre` |
| Créer une ligne | Bouton `ligne` |
| Déplacer un carré ou un oval | Clic gauche maintenu + glisser |
| Supprimer un carré ou une ligne | Clic droit dessus |
| Tout effacer | `Echap` |
| Quitter | Fermer la fenêtre, puis confirmer |
 
## Structure du code
 
Le projet tient dans un seul fichier. Les données sont stockées dans :
 
- `liste_carres` : les identifiants des carrés présents sur le canvas
- `dict_lignes` : `{id_ligne: (carre1, carre2, oval)}`, qui associe chaque ligne à ses deux carrés et à son oval
Les fonctions sont regroupées par rôle :
 
| Rôle | Fonctions |
|---|---|
| Fenêtre | `fermeture_fenetre`, `ok_toplevel`, `annuler_toplevel`, `redimensionner_fenetre` |
| Carrés | `creer_carre`, `detruire_carre`, `debuter_deplacement`, `deplacer_souris`, `lacher_carre`, `fuite_carre` |
| Lignes | `creer_ligne`, `detruire_ligne` |
| Ovals | `debut_deplacement_oval`, `deplacer_souris_oval`, `lacher_oval` |
| Canvas | `effacer_canvas_avec_confirmation` |
 
Les interactions passent par `tag_bind` sur les tags `carre`, `ligne`, `oval` et `anarchiste`.
 
## Limites connues
 
- Quand un carré est déplacé, l'oval de ses lignes revient à sa position par défaut (au-dessus du centre du second carré).
- Les deux carrés reliés par une ligne sont choisis au hasard.
## Auteur
 
Franck, L3 Informatique, Université de Toulon.
 
