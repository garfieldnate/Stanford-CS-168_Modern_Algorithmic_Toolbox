from pathlib import Path

import gudhi
import matplotlib.gridspec as gds
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import gaussian_kde
from sklearn.decomposition import PCA
from sklearn.neighbors import KDTree

MATERIALS = Path(__file__).parents[1] / "materials" / "Week 6"
SNAP_CSV = MATERIALS / "cs168mp6.csv"


def load_snap() -> pd.DataFrame:
    return pd.read_csv(SNAP_CSV, header=None)


# Code below is adapted from https://github.com/Coricos/TdaToolbox/tree/master/clustering
# Shared under Apache 2.0

# Author:  DINDIN Meryll
# Date:    26/06/2018
# Project: clustering

# Credits
# http://code.activestate.com/recipes/215912-union-find-data-structure/

# Implementation of the UnionFind algorithm


class UnionFind:

    # Initialization
    def __init__(self):

        self.num_weights = {}
        self.parent_pointers = {}
        self.num_to_objects = {}
        self.objects_to_num = {}

    # Insert objects among the already existing ones
    def insert_objects(self, objects):

        for object in objects:
            self.find(object)

    # Find a given object / build it if non-existing
    def find(self, object):

        if object not in self.objects_to_num:

            obj_num = len(self.objects_to_num)
            self.num_weights[obj_num] = 1
            self.objects_to_num[object] = obj_num
            self.num_to_objects[obj_num] = object
            self.parent_pointers[obj_num] = obj_num

            return object

        stk = [self.objects_to_num[object]]
        par = self.parent_pointers[stk[-1]]

        while par != stk[-1]:
            stk.append(par)
            par = self.parent_pointers[par]

        for i in stk:
            self.parent_pointers[i] = par

        return self.num_to_objects[par]

    # Link two different objects in a same distinct set
    def union(self, object1, object2):

        o1p = self.find(object1)
        o2p = self.find(object2)

        if o1p != o2p:

            on1 = self.objects_to_num[o1p]
            on2 = self.objects_to_num[o2p]
            w1 = self.num_weights[on1]
            w2 = self.num_weights[on2]

            if w1 < w2:
                o1p, o2p, on1, on2, w1, w2 = o2p, o1p, on2, on1, w2, w1

            self.num_weights[on1] = w1 + w2
            del self.num_weights[on2]
            self.parent_pointers[on2] = on1


# Implements the ToMaTo clustering algorithm (https://geometrica.saclay.inria.fr/team/Steve.Oudot/papers/cgos-pbc-09/cgos-pbcrm-11.pdfhttps://geometrica.saclay.inria.fr/team/Steve.Oudot/papers/cgos-pbc-09/cgos-pbcrm-11.pdf)


class ToMaTo:

    # Initialization
    def __init__(self, x):

        self.x = x

        # Vizualization requires 2D data points
        if x.shape[1] > 2:
            self.reduced = PCA(n_components=2).fit_transform(x)
            print(f"Reduced {x.shape[1]} dimensions to 2 via PCA")
        self.estimate_clusters()

    # Estimate gaussian densities around the data distribution
    # nbins refers to the visualization and space mapping
    # graph is a boolean for data visualization
    def estimate_density(self, nbins=100, graph=False):
        # TODO: what are the output dimensions?
        calc_density = gaussian_kde(self.x.T)
        vec = calc_density(np.vstack(([*self.x.T])))

        if graph:
            reduced = self.reduced if hasattr(self, "reduced") else self.x
            plot_density(self.x, reduced, nbins, calc_density, vec)

        return vec

    # Build the simplex tree and the corresponding filtration
    # num_neighbors refers to the neighboring graph of each element
    # graph is a boolean for data visualization
    def estimate_clusters(self, num_neighbors=6, graph=False):

        vec = self.estimate_density(graph=graph)

        self.kdt = KDTree(self.x, metric="euclidean")
        self.sxt = gudhi.SimplexTree()

        for i in range(self.x.shape[0]):
            self.sxt.insert([i], filtration=-vec[i])
            neighbors = self.kdt.query(
                [self.x[i]], num_neighbors, return_distance=False
            )[0][1:]
            for j in neighbors:
                self.sxt.insert([i, j], filtration=np.mean([-vec[i], -vec[j]]))

        self.sxt.persistence()

        if graph:

            dig, res = self.sxt.persistence(), []
            for ele in dig:
                if ele[0] == 0:
                    res.append(ele)

            plt.figure(figsize=(18, 4))
            fig = gds.GridSpec(1, 2)
            plt.subplot(fig[0, 0])
            print(f"plotting persistance diagram of {res}")
            gudhi.plot_persistence_diagram(res)
            plt.subplot(fig[0, 1])
            gudhi.plot_persistence_barcode(res)
            plt.tight_layout()
            plt.show()

    # Find the clusters and their centroids
    # num_clusters refers to the guessed number of clusters
    # tau is the limitation for one cluster to be merged into another
    # num_neighbors refers to the neighboring graph of each element
    # graph is a boolean for data visualization
    def fit_predict(self, num_clusters, tau=1e-2, num_neighbors=6, graph=False):

        if not hasattr(self, "sxt"):
            self.estimate_clusters(num_neighbors=num_neighbors, graph=graph)

        lst = np.asarray(
            [ele[0][0] for ele in self.sxt.get_filtration() if len(ele[0]) == 1]
        )
        fil = np.asarray(
            [-ele[1] for ele in self.sxt.get_filtration() if len(ele[0]) == 1]
        )
        fil = {k: v for k, v in zip(lst, fil)}

        def define_clusters(lst, fil, num_neighbors):

            unf = UnionFind()

            for idx in lst:

                grp, srt = [], np.where(lst == idx)[0][0]
                for ele in self.kdt.query(
                    [self.x[idx]], num_neighbors, return_distance=False
                )[0][1:]:
                    if np.where(lst == ele)[0][0] < srt:
                        grp.append(ele)

                if len(grp) == 0:
                    unf.insert_objects([idx])

                else:
                    parent = grp[np.asarray([fil[j] for j in grp]).argmax()]
                    unf.union(parent, idx)
                    for ele in grp:
                        root = unf.find(ele)
                        if (
                            root != parent
                            and min(fil[parent], fil[root]) < fil[idx] + tau
                        ):
                            unf.union(parent, root)
                            parent = unf.find(root)

            return unf

        unf, ini = define_clusters(lst, fil, num_neighbors), num_neighbors

        while len(np.unique(list(unf.parent_pointers.values()))) > num_clusters:

            ini += 2
            unf = define_clusters(lst, fil, ini)

        self.cen, self.sts = [], []
        ind = np.asarray(list(unf.num_to_objects.values()))
        rts = np.asarray(list(unf.parent_pointers.values()))

        for ele in np.unique(rts):

            self.cen.append(unf.num_to_objects[ele])
            self.sts.append(ind[np.where(rts == ele)[0]])

        self.cen = np.asarray(self.cen)

        if graph:

            plt.figure(figsize=(18, 4))
            plt.subplot(1, 2, 1)
            plt.title("Initial Data")
            plt.scatter(self.x[:, 0], self.x[:, 1], c="lightgrey")
            plt.xticks([])
            plt.yticks([])
            plt.subplot(1, 2, 2)
            plt.title("Clustered Data")
            for idx, grp in enumerate(self.sts):
                plt.scatter(
                    self.x[grp, 0], self.x[grp, 1], label="Cluster {}".format(idx)
                )
            plt.scatter(
                self.x[self.cen, 0],
                self.x[self.cen, 1],
                c="black",
                marker="x",
                label="Centroids",
            )
            plt.legend(loc="best")
            plt.xticks([])
            plt.yticks([])
            plt.tight_layout()
            plt.show()

        return rts


def plot_density(X, reduced, nbins, den, vec):
    x, y = reduced.T

    u, v = np.mgrid[x.min() : x.max() : nbins * 1j, y.min() : y.max() : nbins * 1j]
    # In if original data dimention > 2, the vizualization will show the
    # density over the reduced (2D) representation of the data calculated by PCA
    # Otherwise, reduced is equal to original data
    # TODO: Change to use original density function
    val = gaussian_kde(reduced.T)(np.vstack([u.flatten(), v.flatten()]))

    plt.figure(figsize=(18, 10))
    fig = gds.GridSpec(3, 6)

    plt.subplot(fig[0, 0:2])
    plt.title("Data Scatter Plot")
    plt.plot(x, y, "ko")
    plt.xticks([])
    plt.yticks([])
    plt.subplot(fig[0, 2:4])
    plt.title("Gaussian KDE")
    plt.pcolormesh(u, v, val.reshape(u.shape), cmap=plt.cm.BuGn_r)
    plt.xticks([])
    plt.yticks([])
    plt.subplot(fig[0, 4:6])
    plt.title("Density Contours")
    plt.pcolormesh(u, v, val.reshape(u.shape), cmap=plt.cm.BuGn_r, shading="gouraud")
    plt.contour(u, v, val.reshape(u.shape))
    plt.xticks([])
    plt.yticks([])

    ax0 = plt.subplot(fig[1:3, 0:3], projection="3d")
    ax0.set_title("Mapped Density over 2D Space")
    ax0.set_xticks([])
    ax0.set_yticks([])
    ax0.set_zticks([])
    ax0.scatter(u, v, val, s=2, c="lightblue")
    ax0.set_xlabel("x Coordinate")
    ax0.set_ylabel("y Coordinate")
    ax0.set_zlabel("Density Value")

    ax1 = plt.subplot(fig[1:3, 3:6], projection="3d")
    ax1.set_title("Density Estimate over 2D Space")
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_zticks([])
    ax1.scatter(x, y, vec, s=2, c="lightgrey")
    ax1.set_xlabel("x Coordinate")
    ax1.set_ylabel("y Coordinate")
    ax1.set_zlabel("Density Value")

    plt.tight_layout()
    plt.show()
