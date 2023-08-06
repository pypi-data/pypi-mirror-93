import numpy as np
from sklearn.ensemble._forest import ForestClassifier
from sklearn.tree import ExtraTreeClassifier
from dsbox.ml.ensemble.rrclassifier.randomrotation import random_rotation_matrix

from sklearn.ensemble._base import _partition_estimators
from joblib import Parallel, delayed
from scipy.stats.mstats_basic import mquantiles

__credits__ = "https://github.com/tmadl/sklearn-random-rotation-ensembles"


def _parallel_helper(obj, methodname, *args, **kwargs):
    """Private helper to workaround Python 2 pickle limitations"""
    return getattr(obj, methodname)(*args, **kwargs)


class RRExtraTreeClassifier(ExtraTreeClassifier):
    def __init__(self,
                 criterion="gini",
                 splitter="random",
                 max_depth=None,
                 min_samples_split=2,
                 min_samples_leaf=1,
                 min_weight_fraction_leaf=0.,
                 max_features="auto",
                 random_state=None,
                 max_leaf_nodes=None,
                 class_weight=None):
        super(RRExtraTreeClassifier, self).__init__(
            criterion=criterion,
            splitter=splitter,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            min_weight_fraction_leaf=min_weight_fraction_leaf,
            max_features=max_features,
            max_leaf_nodes=max_leaf_nodes,
            class_weight=class_weight,
            random_state=random_state)

    def rotate(self, X):
        if not hasattr(self, 'rotation_matrix'):
            raise Exception('The estimator has not been fitted')

        return np.dot(X, self.rotation_matrix)

    def _fit_rotation_matrix(self, X):
        # self.rotation_matrix = np.eye(X.shape[1]).astype(np.float32)
        self.rotation_matrix = random_rotation_matrix(X.shape[1])

    def fit(self, X, y, sample_weight=None, check_input=True):
        self._fit_rotation_matrix(X)
        super(RRExtraTreeClassifier, self).fit(self.rotate(X), y,
                                               sample_weight, check_input)

    def predict_proba(self, X, check_input=True):
        return super(RRExtraTreeClassifier, self).predict_proba(self.rotate(X),
                                                                check_input)

    def predict(self, X, check_input=True):
        return super(RRExtraTreeClassifier, self).predict(self.rotate(X),
                                                          check_input)

    def apply(self, X, check_input=True):
        return super(RRExtraTreeClassifier, self).apply(self.rotate(X),
                                                        check_input)

    def decision_path(self, X, check_input=True):
        return super(RRExtraTreeClassifier, self).decision_path(self.rotate(X),
                                                                check_input)


class RRExtraTreesClassifier(ForestClassifier):
    """

        Parameters
        ----------
        see sklearn documentation
        http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html
    
        Examples
        --------
        
        >>> from sklearn.datasets import load_iris
        >>> from sklearn.model_selection import train_test_split
        >>> from dsbox.ml.ensemble.rrclassifier import RRExtraTreesClassifier
        
        >>> import numpy as np
        >>> np.random.seed(42)
        
        >>> X = load_iris()
        >>> X_train, X_test, y_train, y_test = train_test_split(X.data, X.target, test_size=0.33, stratify=X.target, random_state=42)
        
        >>> clf = RRExtraTreesClassifier(random_state=42)
        >>> _ = clf.fit(X_train, y_train)
        >>> clf.predict(X_test)
        array([1, 1, 0, 1, 2, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 2, 2, 1, 2, 1, 2, 1,
               0, 2, 0, 2, 2, 0, 0, 2, 2, 2, 0, 1, 0, 0, 2, 1, 2, 1, 1, 1, 0, 0,
               2, 1, 2, 1, 1, 2])
        
        References
        ----------
        
        original package: https://github.com/tmadl/sklearn-random-rotation-ensembles
        
        Implementation of the Algorithm: J. J. Rodriguez, L. I. Kuncheva and C. J. Alonso, 
        "Rotation Forest: A New Classifier Ensemble Method," in IEEE Transactions on Pattern 
        Analysis and Machine Intelligence, vol. 28, no. 10, pp. 1619-1630, Oct. 2006.
        doi: 10.1109/TPAMI.2006.211
        
    """

    def __init__(self,
                 n_estimators=10,
                 criterion="gini",
                 max_depth=None,
                 min_samples_split=2,
                 min_samples_leaf=1,
                 min_weight_fraction_leaf=0.,
                 max_features="auto",
                 max_leaf_nodes=None,
                 bootstrap=False,
                 oob_score=False,
                 n_jobs=1,
                 random_state=None,
                 verbose=0,
                 warm_start=False,
                 class_weight=None,
                 scaling=True):

        super(RRExtraTreesClassifier, self).__init__(
            base_estimator=RRExtraTreeClassifier(),
            n_estimators=n_estimators,
            estimator_params=("criterion", "max_depth", "min_samples_split",
                              "min_samples_leaf", "min_weight_fraction_leaf",
                              "max_features", "max_leaf_nodes", "random_state"),
            bootstrap=bootstrap,
            oob_score=oob_score,
            n_jobs=n_jobs,
            random_state=random_state,
            verbose=verbose,
            warm_start=warm_start,
            class_weight=class_weight)

        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.min_weight_fraction_leaf = min_weight_fraction_leaf
        self.max_features = max_features
        self.max_leaf_nodes = max_leaf_nodes
        self.scaling = scaling

        # self.estimator_weights = np.random.random((n_estimators,))
        self.estimator_weights = np.ones((n_estimators,))

    def _fit_scale(self, X):
        self.Q5 = []
        self.Q95 = []
        for i in range(X.shape[1]):
            q5, q95 = mquantiles(X[:, i], [0.05, 0.95])
            self.Q5.append(q5)
            self.Q95.append(q95)

    def _scale(self, X):
        X2 = np.copy(X)
        for i in range(X.shape[1]):
            lessidx = np.where(X2[:, i] < self.Q5[i])[0]
            if len(lessidx) > 0:
                lessval = -.01 * np.log(1 + np.log(1 + np.abs(self.Q5[i] - X2[lessidx, i])))
            moreidx = np.where(X2[:, i] > self.Q95[i])[0]
            if len(moreidx) > 0:
                moreval = 1 + .01 * np.log(1 + np.log(1 + np.abs(self.Q5[i] - X2[moreidx, i])))

            denominator = (self.Q95[i] - self.Q5[i]) if self.Q95[i] != self.Q5[i] else 1
            X2[:, i] = (X[:, i] - self.Q5[i]) / denominator

            if len(lessidx) > 0:
                X2[lessidx, i] = lessval
            if len(moreidx) > 0:
                X2[moreidx, i] = moreval

        return X2

    def fit(self, X, y, sample_weight=None):
        if self.scaling:
            self._fit_scale(X)
            super(RRExtraTreesClassifier, self).fit(self._scale(X), y, sample_weight)
        else:
            super(RRExtraTreesClassifier, self).fit(X, y, sample_weight)

    def predict_proba(self, X):
        """Predict class probabilities for X.

        The predicted class probabilities of an input sample is computed as
        the mean predicted class probabilities of the trees in the forest. The
        class probability of a single tree is the fraction of samples of the same
        class in a leaf.

        Parameters
        ----------
        X : array-like or sparse matrix of shape = [n_samples, n_features]
            The input samples. Internally, it will be converted to
            ``dtype=np.float32`` and if a sparse matrix is provided
            to a sparse ``csr_matrix``.

        Returns
        -------
        p : array of shape = [n_samples, n_classes], or a list of n_outputs
            such arrays if n_outputs > 1.
            The class probabilities of the input samples. The order of the
            classes corresponds to that in the attribute `classes_`.
        """
        # Check data
        if self.scaling:
            X = self._scale(X)
        X = self._validate_X_predict(X)

        # Assign chunk of trees to jobs
        n_jobs, _, _ = _partition_estimators(self.n_estimators, self.n_jobs)

        # Parallel loop
        all_proba = Parallel(n_jobs=n_jobs, verbose=self.verbose,
                             backend="threading")(
            delayed(_parallel_helper)(e, 'predict_proba', X,
                                      check_input=False)
            for e in self.estimators_)

        # Reduce
        proba = all_proba[0]

        if self.n_outputs_ == 1:
            for j in range(1, len(all_proba)):
                proba += self.estimator_weights[j] * all_proba[j]

            # proba /= len(self.estimators_)
            proba /= np.sum(self.estimator_weights[j])

        else:
            for j in range(1, len(all_proba)):
                for k in range(self.n_outputs_):
                    proba[k] += self.estimator_weights[j] * all_proba[j][k]

            for k in range(self.n_outputs_):
                proba[k] /= np.sum(self.estimator_weights[j])

        return proba
