from matplotlib import pyplot as plt
import pandas as pd


def load_data(path):
        data = pd.read_csv(path, index_col=0)
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


def plot_arr(path, listArr):
        data = load_data(path)
        x = data['surface_m2'].values
        y = data['prix_per_m2'].values
        all = plt.scatter(x, y, s=30, facecolor='#e0e0e0', linewidths=0.)
        plt.xlim(0., 500.)
        plt.ylim(0., 40000.)
        plt.grid()
        arrPlot = [plot_arrondissement(data, x[0], x[1]) for x in listArr]
        to_plot = [all] + arrPlot
        legend = ["all"] + [str(x[0]) + "eme arr." for x in listArr]
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
        path = r'C:\Users\pierreb\Documents\housebot-master\data\merged_data.csv'
        listArr = [(1, 'blue'), (15, 'red'), (5, 'green')]
        plot_arr(path, listArr)