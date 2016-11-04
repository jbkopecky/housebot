from matplotlib import pyplot as plt
import pandas as pd


def load_data(path, limit=None):
        data = pd.read_csv(path, index_col=0, nrows=limit)
        data = data[['prix', 'surface_m2', 'description', 'arrondissement']]
        data = data.dropna()
        data['prix_per_m2'] = data['prix'] / data['surface_m2']
        return data


def plot_arrondissement(data, intArr, col):
        arr = str(intArr) + 'eme' if intArr != 1 else "1er"
        _data = data[data['arrondissement'] == 'Paris %s' % arr]
        _x = _data['surface_m2']
        _y = _data['prix_per_m2']
        return plt.scatter(_x, _y, s=30., facecolor=col,  linewidths=0.)


def plot_metro(data, metro, col):
        _data = data[data['metro'] == metro]
        _x = _data['surface_m2']
        _y = _data['prix_per_m2']
        return plt.scatter(_x, _y, s=30., facecolor=col,  linewidths=0.)


def get_list_metro():
    metros = {}

    metros["Abbesses"] = {}
    metros["Alésia"] = {"synonyme" : ["Alesia"]}
    metros["Alexandre"] = {}
    metros["Dumas"] = {}
    metros["Alma - Marceau"] = {}
    metros["Anatole France"] = {}
    metros["Anvers"] = {}
    metros["Argentine"] = {}
    metros["Arts et Métiers"] = {}
    metros["Assemblée nationale"] = {}
    metros["Aubervilliers - Pantin - Quatre"] = {}
    metros["Chemins"] = {}
    metros["Avenue Émile - Zola"] = {}
    metros["Avron"] = {}
    metros["Balard"] = {}
    metros["Barbès - Rochechouart"] = {}
    metros["Basilique de Saint - Denis"] = {}
    metros["Bastille"] = {}
    metros["Bel - Air"] = {}
    metros["Belleville"] = {}
    metros["Bérault"] = {}
    metros["Bercy"] = {}
    metros["Bibliothèque"] = {}
    metros["François - Mitterrand"] = {}
    metros["Billancourt"] = {}
    metros["Bir - Hakeim"] = {}
    metros["Blanche"] = {}
    metros["Bobigny - Pablo"] = {}
    metros["Picasso"] = {}
    metros["Bobigny - Pantin - Raymond"] = {}
    metros["Queneau"] = {}
    metros["Boissière"] = {}
    metros["Bolivar"] = {}
    metros["Bonne - Nouvelle"] = {}
    metros["Botzaris"] = {}
    metros["Boucicaut"] = {}
    metros["Boulogne - Jean"] = {}
    metros["Jaurès"] = {}
    metros["Boulogne - Pont de Saint - Cloud"] = {}
    metros["Bourse"] = {}
    metros["Bréguet - Sabin"] = {}
    metros["Brochant"] = {}
    metros["Buttes"] = {}
    metros["Chaumont"] = {}
    metros["Buzenval"] = {}
    metros["Cadet"] = {}
    metros["Cambronne"] = {}
    metros["Campo - Formio"] = {}
    metros["Cardinal"] = {}
    metros["Lemoine"] = {}
    metros["Carrefour"] = {}
    metros["Pleyel"] = {}
    metros["Censier - Daubenton"] = {}
    metros["Champs - Élysées - Clemenceau"] = {}
    metros["Chardon - Lagache"] = {}
    metros["Charenton - Écoles"] = {}
    metros["Charles de Gaulle - Étoile"] = {}
    metros["Charles"] = {}
    metros["Michels"] = {}
    metros["Charonne"] = {}
    metros["Château d'Eau"] = {}
    metros["Château de Vincennes"] = {}
    metros["Château - Landon"] = {}
    metros["Château Rouge"] = {}
    metros["Châtelet"] = {}
    metros["Châtillon - Montrouge"] = {}
    metros["Chaussée d'Antin - La Fayette"] = {}
    metros["Chemin Vert"] = {}
    metros["Chevaleret"] = {}
    metros["Cité"] = {}
    metros["Cluny - La Sorbonne"] = {}
    metros["Colonel Fabien"] = {}
    metros["Commerce"] = {}
    metros["Concorde"] = {}
    metros["Convention"] = {}
    metros["Corentin"] = {}
    metros["Cariou"] = {}
    metros["Corentin"] = {}
    metros["Celton"] = {}
    metros["Corvisart"] = {}
    metros["Cour Saint - Émilion"] = {}
    metros["Courcelles"] = {}
    metros["Couronnes"] = {}
    metros["Créteil - l'Échat"] = {}
    metros["Créteil - Préfecture"] = {}
    metros["Créteil - Université"] = {}
    metros["Crimée"] = {}
    metros["Croix de Chavaux"] = {}
    metros["Danube"] = {}
    metros["Daumesnil"] = {}
    metros["Denfert - Rochereau"] = {}
    metros["Dugommier"] = {}
    metros["Dupleix"] = {}
    metros["Duroc"] = {}
    metros["École Militaire"] = {}
    metros["École vétérinaire de Maisons - Alfort"] = {}
    metros["Edgar Quinet"] = {}
    metros["Église d'Auteuil"] = {}
    metros["Église de Pantin"] = {}
    metros["Esplanade de La Défense"] = {}
    metros["Étienne Marcel"] = {}
    metros["Europe"] = {}
    metros["Exelmans"] = {}
    metros["Faidherbe - Chaligny"] = {}
    metros["Falguière"] = {}
    metros["Félix"] = {}
    metros["Faure"] = {}
    metros["Filles du Calvaire"] = {}
    metros["Fort d'Aubervilliers"] = {}
    metros["Franklin D.Roosevelt"] = {}
    metros["Front Populaire"] = {}
    metros["Gabriel Péri"] = {}
    metros["Gaîté"] = {}
    metros["Gallieni"] = {}
    metros["Gambetta"] = {}
    metros["Gare d'Austerlitz"] = {}
    metros["Gare de l'Est"] = {}
    metros["Gare de Lyon"] = {}
    metros["Gare du Nord"] = {}
    metros["Garibaldi"] = {}
    metros["George V"] = {}
    metros["Glacière"] = {}
    metros["Goncourt"] = {}
    metros["Grands Boulevards"] = {}
    metros["Guy Môquet"] = {}
    metros["Havre - Caumartin"] = {}
    metros["Hoche"] = {}
    metros["Hôtel de Ville"] = {}
    metros["Iéna"] = {}
    metros["Invalides"] = {}
    metros["Jacques Bonsergent"] = {}
    metros["Jasmin"] = {}
    metros["Jaurès"] = {}
    metros["Javel - André"] = {}
    metros["Citroën"] = {}
    metros["Jourdain"] = {}
    metros["Jules Joffrin"] = {}
    metros["Jussieu"] = {}
    metros["Kléber"] = {}
    metros["La Chapelle"] = {}
    metros["La Courneuve - 8 Mai 1945"] = {}
    metros["La Défense"] = {}
    metros["La Fourche"] = {}
    metros["La Motte - Picquet - Grenelle"] = {}
    metros["La Muette"] = {}
    metros["La Tour - Maubourg"] = {}
    metros["Lamarck - Caulaincourt"] = {}
    metros["Laumière"] = {}
    metros["Le Kremlin - Bicêtre"] = {}
    metros["Le Peletier"] = {}
    metros["Ledru - Rollin"] = {}
    metros["Les Agnettes"] = {}
    metros["Les Courtilles"] = {}
    metros["Les Gobelins"] = {}
    metros["Les Halles"] = {}
    metros["Les Sablons"] = {}
    metros["Liberté"] = {}
    metros["Liège"] = {}
    metros["Louis Blanc"] = {}
    metros["Louise Michel"] = {}
    metros["Lourmel"] = {}
    metros["Louvre - Rivoli"] = {}
    metros["Mabillon"] = {}
    metros["Madeleine"] = {}
    metros["Mairie d'Issy"] = {}
    metros["Mairie d'Ivry"] = {}
    metros["Mairie de Clichy"] = {}
    metros["Mairie de Montreuil"] = {}
    metros["Mairie de Montrouge"] = {}
    metros["Mairie de Saint - Ouen"] = {}
    metros["Mairie des Lilas"] = {}
    metros["Maison Blanche"] = {}
    metros["Maisons - Alfort - Les Juilliottes"] = {}
    metros["Maisons - Alfort - Stade"] = {}
    metros["Malakoff - Plateau de Vanves"] = {}
    metros["Malakoff - Rue Étienne Dolet"] = {}
    metros["Malesherbes"] = {}
    metros["Maraîchers"] = {}
    metros["Marcadet - Poissonniers"] = {}
    metros["Marcel Sembat"] = {}
    metros["Marx Dormoy"] = {}
    metros["Maubert - Mutualité"] = {}
    metros["Ménilmontant"] = {}
    metros["Michel Bizot"] = {}
    metros["Michel - Ange - Auteuil"] = {}
    metros["Michel - Ange - Molitor"] = {}
    metros["Mirabeau"] = {}
    metros["Miromesnil"] = {}
    metros["Monceau"] = {}
    metros["Montgallet"] = {}
    metros["Montparnasse - Bienvenüe"] = {}
    metros["Mouton - Duvernet"] = {}
    metros["Nation"] = {}
    #metros["Nationale"] = {} attention assemblee nationale etc
    metros["Notre - Dame - de - Lorette"] = {}
    metros["Notre - Dame - des - Champs"] = {}
    metros["Oberkampf"] = {}
    metros["Odéon"] = {}
    metros["Olympiades"] = {}
    metros["Opéra"] = {}
    metros["Ourcq"] = {}
    metros["Palais"] = {}
    metros["Royal - Musée du Louvre"] = {}
    metros["Parmentier"] = {}
    metros["Passy"] = {}
    metros["Pasteur"] = {}
    metros["Pelleport"] = {}
    metros["Père Lachaise"] = {}
    metros["Pereire"] = {}
    metros["Pernety"] = {}
    metros["Philippe Auguste"] = {}
    metros["Picpus"] = {}
    metros["Pierre et Marie Curie"] = {}
    metros["Pigalle"] = {}
    metros["Place d'Italie"] = {}
    metros["Place de Clichy"] = {}
    metros["Place des Fêtes"] = {}
    metros["Place Monge"] = {}
    metros["Plaisance"] = {}
    metros["Pointe du Lac"] = {}
    metros["Poissonnière"] = {}
    metros["Pont de Levallois - Bécon"] = {}
    metros["Pont de Neuilly"] = {}
    metros["Pont de Sèvres"] = {}
    metros["Pont Marie"] = {}
    metros["Pont Neuf"] = {}
    metros["Porte Dauphine"] = {}
    metros["Porte d'Auteuil"] = {}
    metros["Porte de Bagnolet"] = {}
    metros["Porte de Champerret"] = {}
    metros["Porte de Charenton"] = {}
    metros["Porte de Choisy"] = {}
    metros["Porte de Clichy"] = {}
    metros["Porte de Clignancourt"] = {}
    metros["Porte de la Chapelle"] = {}
    metros["Porte de la Villette"] = {}
    metros["Porte de Montreuil"] = {}
    metros["Porte de Pantin"] = {}
    metros["Porte de Saint - Cloud"] = {}
    metros["Porte de Saint - Ouen"] = {}
    metros["Porte de Vanves"] = {}
    metros["Porte de Versailles"] = {}
    metros["Porte de Vincennes"] = {}
    metros["Porte des Lilas"] = {}
    metros["Porte d'Italie"] = {}
    metros["Porte d'Ivry"] = {}
    metros["Porte Dorée"] = {}
    metros["Porte d'Orléans"] = {}
    metros["Porte Maillot"] = {}
    metros["Pré Saint - Gervais"] = {}
    metros["Pyramides"] = {}
    metros["Pyrénées"] = {}
    metros["Quai de la Gare"] = {}
    metros["Quai de la Rapée"] = {}
    metros["Quatre - Septembre"] = {}
    metros["Rambuteau"] = {}
    metros["Ranelagh"] = {}
    metros["Raspail"] = {}
    metros["Réaumur - Sébastopol"] = {}
    metros["Rennes"] = {}
    metros["République"] = {}
    metros["Reuilly - Diderot"] = {}
    metros["Richard - Lenoir"] = {}
    metros["Richelieu - Drouot"] = {}
    metros["Riquet"] = {}
    metros["Robespierre"] = {}
    metros["Rome"] = {}
    metros["Rue de la Pompe"] = {}
    metros["Rue des Boulets"] = {}
    metros["Rue du Bac"] = {}
    metros["Rue Saint - Maur"] = {}
    metros["Saint - Ambroise"] = {}
    metros["Saint - Augustin"] = {}
    metros["Saint - Denis - Porte de Paris"] = {}
    metros["Saint - Denis - Université"] = {}
    metros["Saint - Fargeau"] = {}
    metros["Saint - François - Xavier"] = {}
    metros["Saint - Georges"] = {}
    metros["Saint - Germain - des - Prés"] = {}
    metros["Saint - Jacques"] = {}
    metros["Saint - Lazare"] = {}
    metros["Saint - Mandé"] = {}
    metros["Saint - Marcel"] = {}
    metros["Saint - Michel"] = {}
    metros["Saint - Paul"] = {}
    metros["Saint - Philippe du Roule"] = {}
    metros["Saint - Placide"] = {}
    metros["Saint - Sébastien - Froissart"] = {}
    metros["Saint - Sulpice"] = {}
    metros["Ségur"] = {}
    metros["Sentier"] = {}
    metros["Sèvres - Babylone"] = {}
    metros["Sèvres - Lecourbe"] = {}
    metros["Simplon"] = {}
    metros["Solférino"] = {}
    metros["Stalingrad"] = {}
    metros["Strasbourg - Saint - Denis"] = {}
    metros["Sully - Morland"] = {}
    metros["Télégraphe"] = {}
    metros["Temple"] = {}
    metros["Ternes"] = {}
    metros["Tolbiac"] = {}
    metros["Trinité - d’Estienne"] = {}
    metros["d’Orves"] = {}
    metros["Trocadéro"] = {}
    metros["Tuileries"] = {}
    metros["Vaneau"] = {}
    metros["Varenne"] = {}
    metros["Vaugirard"] = {}
    metros["Vavin"] = {}
    metros["Victor Hugo"] = {}
    metros["Villejuif - Léo"] = {}
    metros["Lagrange"] = {}
    metros["Villejuif - Louis"] = {}
    metros["Aragon"] = {}
    metros["Villejuif - Paul"] = {}
    metros["Vaillant - Couturier"] = {}
    metros["Villiers"] = {}
    metros["Volontaires"] = {}
    metros["Voltaire"] = {}
    metros["Wagram"] = {}
    for n in metros:
        metros[n]["number"] = 0
        metros[n]["prices"] = []
        metros[n]["surfaces"] = []
        metros[n]["prices_m2"] = []
        if "synonyme" not in metros[n]:
            metros[n]["synonyme"] = []
    return metros


def map_metro(description, metros, price=None, surface=None, price_m2=None):
    #print(description)
    descr = description.lower()
    for name in sorted(metros):
        good_names = [name, name.replace(" -", ""), name.replace(" ", "")]
        good_names += metros[name]["synonyme"]
        good_names = list(set(good_names))
        if any([n.lower() in descr for n in good_names]):
            metros[name]["number"] += 1
            if price is not None:
                metros[name]["prices"].append(price)
                metros[name]["surfaces"].append(surface)
                metros[name]["prices_m2"].append(price_m2)
            return name
    return None


def mark_metro(data):
    metros = get_list_metro()
    data["metro"] = None
    for line in data.index:
        data["metro"][line] = map_metro(data["description"][line], metros,
                                        price=data["prix"][line],
                                        surface=data["surface_m2"][line],
                                        price_m2=data["prix_per_m2"][line])
    return metros


def stats_metros(metros):
    x = []
    y = []
    for n in sorted(metros, key=lambda b: -sum(metros[b]["prices_m2"]) / 0.1+metros[b]["number"]):
        num = metros[n]["number"]
        if num > 75:
            v = sum(metros[n]["prices_m2"])/num
            print(n, num, v)
            x.append(n)
            y.append(v)
    numOk = sum([metros[x]["number"] if "number" in metros[x] else 0 for x in metros])
    print("Number matched", numOk)
    y_pos = range(len(y))
    plt.barh(y_pos, y)
    y_pos = [a + 0.3 for a in y_pos]
    plt.yticks(y_pos, x)
    plt.show()


def plot_arr(data, listArr):
        x = data['surface_m2'].values
        y = data['prix_per_m2'].values
        all = plt.scatter(x, y, s=30, facecolor='#e0e0e0', linewidths=0.)
        plt.xlim(0., 500.)
        plt.ylim(0., 40000.)
        plt.grid()
        if type(listArr[0][0]) == str:
            arrPlot = [plot_metro(data, x[0], x[1]) for x in listArr]
        else:
            arrPlot = [plot_arrondissement(data, x[0], x[1]) for x in listArr]
        to_plot = [all] + arrPlot
        legend = ["all"] + [str(x[0]) for x in listArr]
        plt.legend(
                to_plot,
                legend,
                # scatterpoints=1,
                # loc='bellow',
                # ncol=3,
                # fontsize=8
                )
        plt.xlabel("Surface (m2)")
        plt.ylabel("Prix au M2 (euros)")
        plt.show()

if __name__ == "__main__":
    pd.options.mode.chained_assignment = None # allow to set values on slice of dataframes
    path = r'C:\Users\pierreb\Documents\gitSeLoger\housebot\merged_data.csv'
    data = load_data(path)
    listArr = [(1, 'blue'), (15, 'red'), (5, 'green')]
    listMetro = [("Bastille", 'blue'), ("Cambronne", 'red'), ("Europe", 'green')]
    metros = mark_metro(data)
    stats_metros(metros)
    #plot_arr(data, listMetro)


