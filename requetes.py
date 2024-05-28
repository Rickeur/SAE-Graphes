import networkx as nx
import json
import matplotlib.pyplot as plt

#Q1
def json_vers_nx(chemin):
    '''
    Construit un graphe à partir d'un fichier JSON contenant des films et leurs acteurs.
    Args:
        chemin (str): Le nom du fichier JSON.
    Returns:
        nx.Graph: Un graphe NetworkX où les nœuds sont les acteurs et les arêtes représentent les collaborations entre acteurs dans des films.
        '''
    G = nx.Graph()
    with open(chemin) as json_load:
        for ligne in json_load:
            movie = json.loads(ligne)
            cast = movie["cast"]
            cast = [acteur.strip("[]") for acteur in cast]
            for i in range(len(cast)):
                for j in range(i + 1, len(cast)):
                    G.add_edge(cast[i], cast[j], movie=movie["title"])
    print("Graphe créé")
    return G

def afficher_graphe(G):
    '''
    Affiche le graphe en utilisant la bibliothèque Matplotlib.
    Args:
        G (nx.Graph): Le graphe à afficher.
    '''
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=35, node_color="skyblue", edge_color="gray", alpha=0.7, font_size=5)
    plt.show()

#Q2
def collaborateurs_communs(G, u, v):
    '''
    Renvoit l’ensemble des acteurs qui ont collaboré avec deux personnes.
    Args:
        G (nx.Graph): Le graphe contenant les collaborations entre acteurs
        u (str): Le nom d'un acteur
        v (str): Le nom d'un acteur
    Returns:
        set: L’ensemble des acteurs qui ont collaboré avec les deux acteurs.
    '''
    if u not in G.nodes or v not in G.nodes:
        print(f"Erreur: Un des acteurs ({u}, {v}) n'existe pas dans le graphe.")
        return set()
    voisins_u = set(G.neighbors(u))
    voisins_v = set(G.neighbors(v))
    return voisins_u.intersection(voisins_v)

#Q3
def collaborateurs_proches(G, u, k):
    '''
    Renvoit les acteurs qui se trouvent à distance au plus k d'un acteur
    Args:
        G (nx.Graph): Le graphe contenant les collaborations entre acteurs
        u (str): Le nom d'un acteur
        k (int): La distance maximale
    Returns:
        set: L’ensemble des acteurs qui se trouvent à distance au plus k d'un acteur
    '''
    if u not in G.nodes:
        print(u,"est inconnu")
        return None
    collaborateurs = set()
    collaborateurs.add(u)
    print(collaborateurs)
    for i in range(k):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    return collaborateurs

def est_proche(G,u,v,k=1):
    '''
    Renvoit True si l'acteur est situé à coté d'un autre acteur
    Args:
        G (nx.Graph): Le graphe contenant les collaborations entre acteurs
        u (str): Le nom d'un acteur
        v (str): Le nom d'un acteur
        k (int): La distance maximale
    Returns:
        boolean: True si les 2 acteurs sont à distance 1
    '''
    proches = collaborateurs_proches(G,u,k)
    return v in proches

def distance_naive(G,u,v):
    '''
    Trouve la distance entre 2 acteurs de façon naive
    Args:
        G (nx.Graph): Le graphe contenant les collaborations entre acteurs
        u (str): Le nom du premier acteur.
        v (str): Le nom du second acteur.
    Returns:
        int: la distance entre 2 acteurs
    '''
    pass

def distance(G, u, v):
    '''
    Trouve la distance entre deux acteurs dans un graphe.
    Args:
        G (nx.Graph): Le graphe contenant les collaborations entre acteurs.
        u (str): Le nom du premier acteur.
        v (str): Le nom du second acteur.
    Returns:
        int: La distance entre les deux acteurs, ou -1 si les acteurs ne sont pas connectés.
    '''
    if u not in G.nodes or v not in G.nodes:
        print(f"Erreur: Un des acteurs ({u}, {v}) n'existe pas dans le graphe.")
        return -1

    queue = [(u, 0)]
    visited = set([u])

    while queue:
        current, distance = queue.pop(0)
        if current == v:
            return distance

        for voisin in G.neighbors(current):
            if voisin not in visited:
                visited.add(voisin)
                queue.append((voisin, distance + 1))
    return -1

#Q4
def centralite(G, u):
    '''
    Calcule l'excentricité d'un acteur dans un graphe.
    Args:
        G (nx.Graph): Le graphe contenant les collaborations entre acteurs.
        u (str): Le nom de l'acteur.
    Returns:
        int: L'excentricité de l'acteur.
    '''
    if u not in G.nodes:
        print(f"Erreur: L'acteur {u} n'existe pas dans le graphe.")
        return -1

    #ici, on utilise l'algorithme de dijkstra
    longest_distance = 0
    for target in G.nodes:
        if target != u:
            distance = nx.shortest_path_length(G, source=u, target=target)
            if distance > longest_distance:
                longest_distance = distance
    return longest_distance

def centre_hollywood(G):
    '''
    Trouve l'acteur le plus central dans un graphe.
    Args:
        G (nx.Graph): Le graphe contenant les collaborations entre acteurs.
    Returns:
        str: Le nom de l'acteur le plus central.
    '''
    centralite_min = float('inf')
    acteur_central = None
    
    for acteur in G.nodes:
        centralite_acteur = centralite(G, acteur)
        if centralite_acteur < centralite_min:
            centralite_min = centralite_acteur
            acteur_central = acteur
    return acteur_central

#Q5
def eloignement_max(G:nx.Graph):
    pass

def centralite_groupe(G,S):
    pass

#Bonus
def centralite_groupe(G,S):
    pass

# TEST
# dataTest2
# data_100

# Al Pacino, Frank Oz, Jeremy Irons, Jay Mohr

# graphe = json_vers_nx("data_100.json")