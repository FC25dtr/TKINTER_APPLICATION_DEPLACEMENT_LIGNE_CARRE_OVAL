import tkinter as tk 
from tkinter import messagebox
import random as r 

liste_carres = []
dict_lignes = {}
carre_en_cours_deplacement = None
oval_en_cours_deplacement = None
pos_init = (0, 0)
pos_init_oval = (0,0)
dx_souris, dy_souris = 0, 0
ligne_suppr = 0
 
#fonction binding

def fermeture_fenetre():
    """
    creation d'une top level afin de confirmer la fermeture ou non de root
    """
    #creation top level et bouton ok et annuler + placement
    toplevel = tk.Toplevel()
    Label_toplevel = tk.Label(toplevel, text = "Etes vous sur de vouloir fermer la fenetre ?")
    
    #creation bouton
    bouton_ok = tk.Button(toplevel,text = "ok",command = ok_toplevel)
    bouton_annuler = tk.Button(toplevel,text = "annuler",command = lambda p = toplevel: annuler_toplevel(p))#utilisation de lambda pour placer l'id de la top level en parametre 

    #placement
    Label_toplevel.grid(column = 1,row = 1 , columnspan = 2)
    bouton_ok.grid(column = 1,row = 2)
    bouton_annuler.grid(column = 2, row = 2)

def ok_toplevel():
    """
    fermeture de la top level et fermeture de root
    """
    root.destroy()

def annuler_toplevel(toplevel):
    """
    fermeture top level mais pas fermeture de root 
    """
    toplevel.destroy()
    
def debuter_deplacement(event):
    """ 
    stockage position carre
    """
    global carre_en_cours_deplacement, pos_init, dx_souris, dy_souris
    
    #carre en dessous de la souris au moment du clic 
    carre_en_cours_deplacement = canva_frame.find_withtag("current")[0]
    #stockage pos initial en cas de carre en dessous
    pos_init = canva_frame.coords(carre_en_cours_deplacement)
    dx_souris = event.x
    dy_souris = event.y

def deplacer_souris(event):
    """ 
    deplace le carre au deplacement de la souris en calculant ca nouvelle position grace au deplacement
    """
    global dx_souris, dy_souris, dict_lignes
    if carre_en_cours_deplacement is not None:
        #calcul nouvelle coordonnées 
        dx = event.x - dx_souris 
        dy = event.y - dy_souris 
        #deplacement aux nouvelles coordonnées 
        canva_frame.move(carre_en_cours_deplacement, dx, dy) 
        dx_souris = event.x
        dy_souris = event.y 
        for id_ligne, (c1, c2,oval) in dict_lignes.items():
            #recup les coordonnes des carre attache  la ligne 
            coord1 = canva_frame.coords(c1)
            coord2 = canva_frame.coords(c2)
        
            #recalcul placement ligne avec centre carre
            x1 = (coord1[0] + coord1[2]) / 2
            y1 = (coord1[1] + coord1[3]) / 2
            x2 = (coord2[0] + coord2[2]) / 2
            y2 = (coord2[1] + coord2[3]) / 2
        
            #mise a jour ligne canva
            canva_frame.coords(id_ligne, x1, y1, x2, y1,x2,y2)

            #mise a jour de la position de oval meme methode que ligne
            canva_frame.coords(oval,x2-10,y1-10,x2+10,y1+10)

def lacher_carre(event):
    """
    depose le carre au bon endroit sur la grille aimanté 
    """
    global carre_en_cours_deplacement, pos_init
    if carre_en_cours_deplacement is not None:
        
        #taille de la grille magnétique
        taille_grille = canva_frame.winfo_width() // 10
        
        #coordonnées et aimantation
        x1, y1, x2, y2 = canva_frame.coords(carre_en_cours_deplacement)
        largeur = x2 - x1
        hauteur = y2 - y1
        
        #je recupere le multiple de la case la plus proche en x et y 
        x_vise = round(x1 / taille_grille) * taille_grille 
        y_vise = round(y1 / taille_grille) * taille_grille
        canva_frame.coords(carre_en_cours_deplacement, x_vise, y_vise, x_vise + largeur, y_vise + hauteur)
        
        #recuêration des objets dans la zone 
        objets_proches = canva_frame.find_overlapping(x_vise , y_vise, (x_vise + largeur), (y_vise + hauteur))

        #on verifie si l'objet dans la zone est un carre
        carres_proches = [obj for obj in objets_proches if "carre" in canva_frame.gettags(obj)]
        
        #si l'objet est bien un carre on ramene notre carre a la pos init
        if len(carres_proches) > 1:
            canva_frame.coords(carre_en_cours_deplacement, pos_init[0], pos_init[1], pos_init[2], pos_init[3])
            
        #mise a jour pose ligne suite a deplacement avec attachement a la grille 
        for id_ligne, (c1, c2,oval) in dict_lignes.items():
            coord1 = canva_frame.coords(c1)
            coord2 = canva_frame.coords(c2)
            
            x1_l = (coord1[0] + coord1[2]) / 2
            y1_l = (coord1[1] + coord1[3]) / 2
            x2_l = (coord2[0] + coord2[2]) / 2
            y2_l = (coord2[1] + coord2[3]) / 2
            
            canva_frame.coords(id_ligne, x1_l, y1_l, x2_l, y1_l,x2_l,y2_l)

            #mise a jour de l'oval comme la ligne
            canva_frame.coords(oval,x2_l-10,y1_l-10,x2_l+10,y1_l+10)
        carre_en_cours_deplacement = None #fin utilisation carre en cours de deplacement 


        
def redimensionner_fenetre(event=None):
    """
    Remet le dernier carré créé bien au milieu quand on redimensionne la fenêtre
    """
    global liste_carres,canva_taille_height, canva_taille_width
    
    #calcul tailel canva
    heightbis = canva_frame.winfo_height()
    widthbis = canva_frame.winfo_width()
    
    ratio_x = widthbis / canva_taille_width
    ratio_y = heightbis / canva_taille_height
    #modification de la taille de tout les carre avec le tag
    for i in liste_carres:
        coord  = canva_frame.coords(i)

        #calcul du milieu du carre
        milieux = (coord[0] + coord[2])/2
        milieuy = (coord[1] + coord[3])/2

        #changement de taille en fontion du retrecissment ou agrandissement 
        canva_frame.scale(i,milieux,milieuy,ratio_x,ratio_y)
    canva_taille_height = heightbis
    canva_taille_width = widthbis
            
        
        
        
def creer_carre(event=None):
    """
    Appelé UNIQUEMENT quand on clique sur le bouton pour créer un carré.
    """
    global carre_en_cours_deplacement
    
    x = canva_frame.winfo_width()
    y = canva_frame.winfo_height()
    
    #calcul du milieu du canva
    x1 = x // 2 -10
    x2 = x // 2 +10
    y1 = y // 2 -10
    y2 = y // 2 +10
    
    #verifie si un carre est deja sur la case 
    objets_proches = canva_frame.find_overlapping(x1 , y1 , x2, y2)

    #on verifie si c'est bien un carre dans la zone est pas un segment par exemple 
    carre_proche = [obj for obj in objets_proches if "carre" in canva_frame.gettags(obj)]

    #si ce n'est pas un carre alors on crée le carré 
    if len(carre_proche)<1:
        anar = r.randint(1,4)
        if anar == 1:
            nouveau_carre = canva_frame.create_rectangle(x1, y1, x2, y2, fill='black', tags=("carre","anarchiste")) 
            liste_carres.append(nouveau_carre)
        else :
            nouveau_carre = canva_frame.create_rectangle(x1, y1, x2, y2, fill='black', tags="carre") 
            liste_carres.append(nouveau_carre)
    else :
        print("carre deja cree")

def detruire_carre(event=None):
    """
    supression du carre au clique droit dessus et des lignes relié au carré 
    """
    global liste_carres, dict_lignes
    ligne_suppr = []
    id_carre_clique = canva_frame.find_withtag("current")[0]
    canva_frame.delete(id_carre_clique)

    #supression de l'id dans la liste carré 
    if id_carre_clique in liste_carres:
        liste_carres.remove(id_carre_clique)

    #parcours et dico par cle valeur
    for id_ligne, (carre1,carre2,oval) in dict_lignes.items():

        #recherche si le carré supprimé est associé a une ligne
        if (carre1 == id_carre_clique) or (carre2 == id_carre_clique):

            #supression de la ligne associé au carre
            canva_frame.delete(id_ligne)
            canva_frame.delete(oval)
            ligne_suppr += [id_ligne]

    #suppresion hors de la boucle de la ligne dans le DICTIONNAIRE pour eviter les erreur avec items dans la boucle 
    for i in ligne_suppr :
        #pop pour supprimer
        dict_lignes.pop(i)
        print(dict_lignes,"element supprimé avec succés")
        
    
            
def effacer_canvas_avec_confirmation(event=None):
    """
    suppression canva entier 
    """
    # boite de dialogue de confirmation
    global liste_carres, dict_lignes
    reponse = messagebox.askyesno("confirmation", "etes-vous sur de vouloir effacer la zone graphique ?")
    if reponse == True:
        canva_frame.delete("all") # efface  tout ce qu'il y a sur le canvas
        liste_carres = []      # On reinitialise l'id du carré
        dict_lignes.clear()

        
def creer_ligne():
    """
    creation de la ligne entre deux carre
    """
    global liste_ligne 
    if len(liste_carres) < 2 : #verif si il existe deux carres
        print("pas assez de carre pour creer une ligne")
        return 
    carre1 = r.choice(liste_carres)
    carre2 = None 
    while carre2 == None or carre2 == carre1:
        #pour forcer a seletionner deux carre different
        carre2 = r.choice(liste_carres) 
        
    #recuperation coordonnees des deux carres
    coord_carre1 = canva_frame.coords(carre1)
    coord_carre2 = canva_frame.coords(carre2) 
    
    #stockage en x et en y pour create ligne en recuperant leur milieu 
    x1 = (coord_carre1[0] + coord_carre1[2]) / 2
    y1 = (coord_carre1[1] + coord_carre1[3]) / 2
    x2 = (coord_carre2[0] + coord_carre2[2]) / 2
    y2 = (coord_carre2[1] + coord_carre2[3]) / 2
    
    #creation de la ligne plus stockage dans une liste
    id_ligne = canva_frame.create_line(x1, y1, x2, y1,x2,y2, width=2,tags = "ligne")

    #creation des ovales sur les sommets des lignes
    oval_sommet = canva_frame.create_oval(x2-10,y1-10,x2+10,y1+10,fill = "black",tags = "oval")
    dict_lignes[id_ligne] = (carre1, carre2,oval_sommet)

def detruire_ligne(event=None):
    """
    suppression de ligne lors du clique droit dessus ainsi que de l'oval associé
    """
    global dict_lignes
    
    #recuperation du clique 1. On récupère l'élément survolé au moment du clic
    id_clique = canva_frame.find_withtag("current")[0]
    
    #liste pour stocker ce qu'on doit retirer du dictionnaire
    lignes_a_supprimer = []
    
    #parcours orthographe ave items 
    for id_ligne, (c1, c2, oval) in dict_lignes.items():
        
        #verifi si clique correspond a la ligne 
        if id_clique == id_ligne :
            
            #suppression ligne sur le canva
            canva_frame.delete(id_ligne)
            canva_frame.delete(oval)
            
            # on stocke la cle  a suppr
            lignes_a_supprimer.append(id_ligne)
            
    #suppresion apres le item
    for ligne in lignes_a_supprimer:
        dict_lignes.pop(ligne)
        print("Ligne supprimée avec succès")

def fuite_carre(event):
    #on récupère le carré survolé
    id_carre = canva_frame.find_withtag("current")[0]
    
    # on récupère ses coordonnées (on prend juste son point de départ x, y)
    coords = canva_frame.coords(id_carre)
    x_carre = coords[0]
    y_carre = coords[1]
    
    # si la souris est à gauche du carré, on va à droite (+50), sinon à gauche (-50)
    dx = 50 if event.x < x_carre else -50
    
    #même chose pour le haut et le bas
    dy = 50 if event.y < y_carre else -50
    
    # on applique le mouvement du carre ananrchiste a la ligne 
    canva_frame.move(id_carre, dx, dy)
    for id_ligne, (c1, c2,oval) in dict_lignes.items():
        coord1 = canva_frame.coords(c1)
        coord2 = canva_frame.coords(c2)
            
        x1_l = (coord1[0] + coord1[2]) / 2
        y1_l = (coord1[1] + coord1[3]) / 2
        x2_l = (coord2[0] + coord2[2]) / 2
        y2_l = (coord2[1] + coord2[3]) / 2
        canva_frame.coords(id_ligne, x1_l, y1_l, x2_l, y1_l,x2_l,y2_l)
        
        #mise a jour de la position de l'oval relie a la ligne aussi
        canva_frame.coords(oval,x2_l-10,y1_l-10,x2_l+10,y1_l+10)

def debut_deplacement_oval(event):
    """
    stockage coordonnée de base de l'oval et association du clique au debut du deplacement 
    """
    global oval_en_cours_deplacement, pos_init_oval, dx_souris, dy_souris
    
    #carre en dessous de la souris au moment du clic 
    oval_en_cours_deplacement = canva_frame.find_withtag("current")[0]
    #stockage pos initial en cas de carre en dessous
    pos_init_oval = canva_frame.coords(oval_en_cours_deplacement)
    dx_souris = event.x
    dy_souris = event.y

def deplacer_souris_oval(event):
    """ 
    deplace l'oval au deplacement de la souris en calculant ca nouvelle position grace au deplacement ainsi que ces lignes associé 
    """
    global dx_souris, dy_souris, dict_lignes, oval_en_cours_deplacement
    if oval_en_cours_deplacement is not None:
        #calcul nouvelle coordonnées 
        dx = event.x - dx_souris 
        dy = event.y - dy_souris
        
        #deplacement aux nouvelles coordonnées 
        canva_frame.move(oval_en_cours_deplacement, dx, dy) 
        dx_souris = event.x
        dy_souris = event.y
        
        for id_ligne, (c1, c2,oval) in dict_lignes.items():
            #recup les coordonnes des carre attache  la ligne
            if oval == oval_en_cours_deplacement:

                #calcul position des carre relié 
                coord1 = canva_frame.coords(c1)
                coord2 = canva_frame.coords(c2)
        
                #recalcul placement ligne avec centre carre
                x1 = (coord1[0] + coord1[2]) / 2
                y1 = (coord1[1] + coord1[3]) / 2
                x2 = (coord2[0] + coord2[2]) / 2
                y2 = (coord2[1] + coord2[3]) / 2
        
                #mise a jour ligne canva avec la nouvele position de l'oval
                canva_frame.coords(id_ligne, x1, y1, dx_souris, dy_souris,x2,y2)


#debut root 
root = tk.Tk()
root.wait_visibility()

height = root.winfo_screenheight()
width = root.winfo_screenwidth()
#recuperation de la moitie de la taille de l'ecran 
taille_root_height = height // 2
taille_root_width = width // 2

# conversion taille en str 
c1 = str(taille_root_height)
c2 = str(taille_root_width)
c3 = c2 + 'x' + c1


#configuration de root 
root.title("Tkinter-TP")
root.geometry(c3)

#creation frames 
Frame_text_carre = tk.Frame(root,bg = "black")
Frame_canva = tk.Frame(root,bg = 'green')

#ajout bouton frame 
bouton_carre = tk.Button(Frame_text_carre, text = "carre",command = creer_carre)
bouton_ligne = tk.Button(Frame_text_carre, text = "ligne", command = creer_ligne)

#creation canva dans frame 
canva_frame = tk.Canvas(Frame_canva,bg = 'grey90')

#stockage tailel frame canva
canva_taille_height = canva_frame.winfo_height()
canva_taille_width = canva_frame.winfo_width()

#binding, protocol 
root.protocol('WM_DELETE_WINDOW',fermeture_fenetre)
canva_frame.bind("<Configure>", redimensionner_fenetre)
root.bind("<Escape>", effacer_canvas_avec_confirmation)
canva_frame.tag_bind("carre", "<Button-1>", debuter_deplacement)
canva_frame.tag_bind("carre", "<B1-Motion>", deplacer_souris)
canva_frame.tag_bind("carre", "<ButtonRelease-1>", lacher_carre)
canva_frame.tag_bind("carre","<Button-3>",detruire_carre)
canva_frame.tag_bind("ligne","<Button-3>",detruire_ligne)
canva_frame.tag_bind("anarchiste","<Enter>",fuite_carre)
canva_frame.tag_bind("oval","<Button-1>",debut_deplacement_oval)
canva_frame.tag_bind("oval","<B1-Motion>",deplacer_souris_oval)

#placement widget 
Frame_text_carre.pack(fill = "x")
Frame_canva.pack(expand = True,fill = "both")
bouton_carre.pack(side = 'left')
canva_frame.pack(expand = True, fill = "both")
bouton_ligne.pack(side = 'left')

root.mainloop()
