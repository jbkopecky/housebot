from utils import make_xy_data
from utils import sort_dict_by
from utils import plot_compare_feature_levels
import matplotlib.pyplot as plt
import numpy as np

X, y = make_xy_data('./data/merged_data.csv', ['surface_m2', 'piece'])
not_missing = {x: float(len(np.ones(len(X))[~X[x].isnull().values]))/float(len(X)) for x in X.columns}
sorted_not_missing = sort_dict_by(not_missing, by=1)
plot_compare_feature_levels(sorted_not_missing)
plt.show()
