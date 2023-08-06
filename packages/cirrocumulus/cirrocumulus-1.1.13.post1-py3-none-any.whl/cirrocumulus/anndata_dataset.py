import anndata
import numpy as np
import pandas as pd
import scipy.sparse

from cirrocumulus.abstract_dataset import AbstractDataset
# only works with local files
from cirrocumulus.io_util import read_star_fusion_file
from cirrocumulus.simple_data import SimpleData


class AnndataDataset(AbstractDataset):

    def __init__(self, backed=None, force_sparse=True, extensions=['h5ad', 'loom', 'zarr']):
        super().__init__()
        self.path_to_data = {}
        self.backed = backed
        self.force_sparse = force_sparse
        self.extensions = extensions

    def get_suffixes(self):
        return self.extensions

    def read_adata(self, path):
        path_lc = path.lower()
        if path_lc.endswith('.loom'):
            return anndata.read_loom(path)
        elif path_lc.endswith('.zarr'):
            return anndata.read_zarr(path)
        elif path_lc.endswith('.tsv'):
            return read_star_fusion_file(path)
        return anndata.read(path, backed=self.backed)
        # elif path.endswith('.mtx'):
        #
        #     return anndata.read_mtx(path, backed=self.backed)
        # elif path.endswith('.txt'):
        #
        #     return anndata.read_text(path, backed=self.backed)
        # elif path.endswith('.csv'):
        #
        #     return anndata.read_csv(path, backed=self.backed)

    def add_data(self, path, data):
        self.path_to_data[path] = data

    def get_data(self, path):
        adata = self.path_to_data.get(path)
        if adata is None:
            adata = self.read_adata(path)
            if scipy.sparse.isspmatrix_csr(adata.X):
                adata.X = adata.X.tocsc()
            self.add_data(path, adata)
        return adata

    def schema(self, file_system, path):
        return SimpleData.schema(self.get_data(path))

    def read_dataset(self, file_system, path, keys=None, dataset=None, schema=None):
        adata = self.get_data(path)
        force_sparse = self.force_sparse
        df = None
        if keys is None:
            keys = {}
        keys = keys.copy()
        var_keys = keys.pop('X', [])
        obs_keys = keys.pop('obs', [])
        basis = keys.pop('basis', [])

        if len(var_keys) > 0:
            X = adata[:, var_keys].X
            if len(X.shape) == 1:
                X = np.array([X]).T
            if force_sparse and not scipy.sparse.issparse(X):
                X = scipy.sparse.csr_matrix(X)
            if scipy.sparse.issparse(X):
                df = pd.DataFrame.sparse.from_spmatrix(X, columns=var_keys)
            else:
                df = pd.DataFrame(data=X, columns=var_keys)
        for key in keys.keys():
            if df is None:
                df = pd.DataFrame()
            d = adata.uns[key]
            features = keys[key]
            X = d['X'][:, d['var'].index.get_indexer_for(features)]
            for i in range(len(features)):
                df[features[i]] = X[:, i]
        if len(obs_keys) > 0:
            if df is None:
                df = pd.DataFrame()
            for key in obs_keys:
                if key == 'index':
                    values = adata.obs.index.values
                else:
                    values = adata.obs[key].values
                df[key] = values

        if basis is not None and len(basis) > 0:
            if df is None:
                df = pd.DataFrame()
            for b in basis:
                embedding_name = b['name']
                embedding_data = adata.obsm[embedding_name]
                dimensions = b['dimensions']
                for i in range(dimensions):
                    df[b['coordinate_columns'][i]] = embedding_data[:, i]
        return df
