from matplotlib import pyplot as plt
import pandas as pd

data = pd.read_csv('./data/merged_data.csv', index_col=0)

data = pd.read_csv('data/merged_data.csv', index_col=0)
data = data[['prix', 'surface_m2', 'description', 'arrondissement']]
data = data.dropna()
data['prix_per_m2'] = data['prix'] / data['surface_m2']

x = data['surface_m2'].values
y = data['prix_per_m2'].values
all = plt.scatter(x, y, s=30, facecolor='#e0e0e0', linewidths=0.)

arr = '12eme'
_data = data[data['arrondissement']=='Paris %s' % arr]
_x = _data['surface_m2']
_y = _data['prix_per_m2']

arr12 = plt.scatter(_x, _y, s=30., facecolor='#b30000',  linewidths=0.)

arr = '3eme'
_data = data[data['arrondissement']=='Paris %s' % arr]
_x = _data['surface_m2']
_y = _data['prix_per_m2']

arr3 = plt.scatter(_x, _y, s=30., facecolor='#00b35a', linewidths=0.)
plt.xlim(0., 500.)
plt.ylim(0., 40000.)
plt.grid()
plt.legend(
        (all, arr12, arr3),
        ('All', '12eme Arrondissement', '3eme Arrondissement'),
        # scatterpoints=1,
        # loc='bellow',
        # ncol=3,
        # fontsize=8
        )
plt.xlabel("Surface (m2)")
plt.ylabel("Prix au M2 (euros)")
plt.savefig("plots/general_scatter.png")

