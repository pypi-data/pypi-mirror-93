import hashlib
from collections import defaultdict

import numpy as np
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelBinarizer, LabelEncoder
from sklearn.utils import column_or_1d
from sklearn.utils.validation import check_is_fitted


class SafeLabelEncoder(LabelEncoder):
    """An extension of LabelEncoder that will
    not throw an exception for unseen data, but will
    instead return a default value of 99999

    Taken from https://www.alkaline-ml.com/skutil/rsts/codebase/skutil_preprocessing.html#skutil.preprocessing.SafeLabelEncoder

    Parameters
    ----------

    unseen : int,
        The integer label to be used for unseen classes. You can also use negative values (for some classifiers).
        Default: int(99999).

    """

    def __init__(self, unseen=99999):
        self.unseen = unseen

    def transform(self, y):
        """Perform encoding if already fit.

        Parameters
        ----------

        y : array_like, shape=(n_samples,)
            The array to encode

        Returns
        -------

        e : array_like, shape=(n_samples,)
            The encoded array
        """
        check_is_fitted(self, 'classes_')
        y = column_or_1d(y, warn=True)

        classes = np.unique(y)

        # Check not too many:
        if 0 <= self.unseen <= len(classes):
            raise ValueError(
                'Too many factor levels in feature. Max is %i: Increase the unseen label if possible.' % self.unseen)

        e = np.array([
            np.searchsorted(self.classes_, x) if x in self.classes_ else self.unseen
            for x in y
        ])

        return e


class PipeLineLabelBinarizer(TransformerMixin):

    def __init__(self, *args, **kwargs):
        self.encoder = LabelBinarizer(*args, **kwargs)

    def fit(self, X, y=None):
        self.encoder.fit(X)
        return self

    def transform(self, X, y=None):
        return self.encoder.transform(X)


class PipeLineLabelEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, safe_label_encoder=False, unseen_label=-1):
        self.safe_label_encoder = safe_label_encoder
        self.unseen_label = unseen_label
        if self.safe_label_encoder:
            self.encoder = SafeLabelEncoder(unseen=self.unseen_label)
        else:
            self.encoder = LabelEncoder()

    def fit(self, X, y=None):
        self.encoder.fit(X)
        return self

    def transform(self, X, y=None):
        return self.encoder.transform(X)

    def get_params(self, deep=False):
        return {'safe_label_encoder': self.safe_label_encoder, 'unseen_label': self.unseen_label}


class VectorToCentroidCosineTransformer(object):

    def __init__(self, centroids):
        self.centroids = centroids

    def fit(self, X, y=None):
        return self

    def partial_fit(self, X, y=None):
        return self

    def transform(self, X):
        print('Calculating embedding distances to centroids {}x{}.'.format(str(len(X)), str(len(self.centroids))))
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            return cosine_similarity(X, self.centroids)


class VectorValueThresholdReducer(object):

    def __init__(self, reduce_to=0.0):
        self.replacement_value = reduce_to
        super().__init__()

    def fit(self, X, y=None):
        self.thres_ = X.mean(axis=0) + (X.std(axis=0) * 2)
        return self

    def transform(self, X):
        X[X < self.thres_] = self.replacement_value
        return X


class Senses(object):

    def __init__(self, clusterer=KMeans()):
        self.clusterer = clusterer
        self.sense_clusters = self.clusterer.n_clusters

    def fit(self, X, y=None):
        element_index = X[:, 0]
        vector_index = X[:, 1]
        self.lexicon_size_ = element_index.shape[0]
        self.clusterer_ = self.clusterer.fit(vector_index)
        vector_distances = self.clusterer_.transform(vector_index)
        K = 50
        cluster_representatives = []
        for cluster in vector_distances.T:
            topK_indeces = np.argpartition(cluster, K)[:K]
            cluster_representatives.append(element_index[topK_indeces[np.argsort(cluster[topK_indeces])]])
        self.sense_representatives_ = np.array(cluster_representatives)
        return self


class Element2SenseVector(object):

    def __init__(self, sense_vectors, element2embedding, sense_threshold=None, unknown=None, override=False,
                 fit_embeddings=False):
        self.sense_converter = VectorToCentroidCosineTransformer(sense_vectors)
        self.element2embedding = element2embedding
        self.sense_threshold = sense_threshold
        self.unknown = unknown
        self.override = override
        self.fit_embeddings = fit_embeddings

    def __calc_stub_vector(self):
        if not self.unknown or self.unknown is None:
            self.stub_vec_ = None
        elif self.unknown == 'mean':
            self.stub_vec_ = np.mean(np.array(self.token2sense_vec_.values()), axis=0)
            if self.sense_threshold:
                self.stub_vec_ = self.sense_threshold_.transform(self.stub_vec_)
        elif self.unknown == 'zero':
            self.stub_vec_ = np.zeros_like(next(iter(self.token2sense_vec_.values())))
        else:
            self.stub_vec_ = None

    def fit(self, X, y=None):
        if self.fit_embeddings:
            print('Fitting embeddings.')
            self.element2embedding_ = self.element2embedding.fit(X)
        else:
            self.element2embedding_ = self.element2embedding

        # Get embeddings for known elements.
        target_lexicon = list(set(token for tokens in X for token in tokens))
        print('Collecting known embeddings for requested elements.')

        elements_, vectors_ = zip(*filter(lambda x: x[1] is not None, zip(target_lexicon,
                                                                          self.element2embedding_.transform(
                                                                              np.array([target_lexicon]))[0])))

        print('\t{} out of requested {} element embeddings are present in inner embedding dictionary.'
              .format(str(len(elements_)), str(len(target_lexicon))))

        print('Converting embeddings to senses.')
        self.sense_converter_ = self.sense_converter.fit(vectors_)
        sense_vectors_ = self.sense_converter_.transform(vectors_)

        print('Building sense index.')
        self.token2sense_vec_ = dict(zip(elements_, sense_vectors_))

        if self.sense_threshold:
            print('Fitting threshold.')
            self.sense_threshold_ = self.sense_threshold.fit(sense_vectors_)

        self.__calc_stub_vector()
        return self

    def partial_fit(self, X, y=None):
        # Get embeddings for known elements.
        if self.fit_embeddings:
            print('Partially fitting embeddings.')
            self.element2embedding_ = self.element2embedding_.partial_fit(X)

        target_lexicon = list(set(token for tokens in X for token in tokens))

        if not self.override:
            target_lexicon = list(filter(lambda x: x not in self.token2sense_vec_, target_lexicon))

        print('[{}]: Collecting senses for requested elements with{} override.'.format(self.__class__.__name__,
                                                                                       '' if self.override else 'out'))
        elements_and_vectors = list(filter(lambda x: x[1] is not None,
                                           zip(target_lexicon, self.element2embedding_.transform([target_lexicon])[0])))

        if len(elements_and_vectors) > 0:
            print('\t{} out of requested {} element embeddings are present in inner embedding dictionary.'
                  .format(str(len(elements_and_vectors)), str(len(target_lexicon))))
            elements_, vectors_ = zip(*elements_and_vectors)

            print('Converting embeddings to senses.')
            self.sense_converter_.partial_fit(vectors_)
            sense_vectors_ = self.sense_converter_.transform(vectors_)

            print('Updating token to sense mapping.')
            self.token2sense_vec_.update(zip(elements_, sense_vectors_))

            if self.sense_threshold:
                print('Refitting threshold.')
                self.sense_threshold_ = self.sense_threshold_.fit(np.array(list(self.token2sense_vec_.values())))

            self.__calc_stub_vector()
        else:
            print('No new elements can be fitted from {} of the input lexicon.'.format(len(target_lexicon)))
        return self

    def transform(self, X):
        if self.sense_threshold:
            return np.array([
                np.array([self.__get_thresholded_vec_indexed(token) for token in tokens])
                for tokens in X
            ])
        else:
            return np.array([
                np.array([self.__get_vec_indexed(token) for token in tokens])
                for tokens in X
            ])

    def __get_vec_indexed(self, element):
        try:
            return self.sense_threshold_.transform(self.token2sense_vec_[element])
        except KeyError:
            return self.stub_vec_

    def __get_thresholded_vec_indexed(self, element):
        try:
            return self.token2sense_vec_[element]
        except KeyError:
            return self.stub_vec_


class SenseTextTransformer(object):

    def __init__(self, element2sense, embedding_accumulator):
        self.element2sense = element2sense
        self.embeddings_accumulator = embedding_accumulator
        super().__init__()

    def fit(self, X, y=None):
        self.element2sense.fit(X)
        return self

    def partial_fit(self, X, y=None):
        self.element2sense.partial_fit(X)
        return self

    def transform(self, X):
        return np.array([self.__collect_text_embedding(embeddings) for embeddings in self.element2sense.transform(X)])

    def __collect_text_embedding(self, token_embeddings):
        known_vecs = np.array(list(filter(lambda x: x is not None, token_embeddings)))
        if len(known_vecs) <= 0:
            return self.element2sense.stub_vec
        else:
            return self.embeddings_accumulator.transform(known_vecs)


class EmbeddingAccumulator(object):
    """
    """

    def __init__(self, mean=False):
        self.get_mean = mean

    def transform(self, X):
        return self.__calc_embedding(X)

    def __calc_embedding(self, embeddings):
        if self.get_mean:
            return np.mean(embeddings, axis=0)
        else:
            return np.sum(embeddings, axis=0)


class MeanEmbeddingAccumulator(object):
    """
    This class duplicates MeanEmbeddingVectorizer, but for the functionality of normalizing the vectors.
    Also, it may be a little optimized for fully-oov-sentences.
    """

    def __init__(self, embeddings, element_index, mean_for_unknown=False):
        self.element2embedding = {element: np.array(embedding) for element, embedding in zip(element_index, embeddings)}
        self.get_mean = mean_for_unknown
        if self.get_mean:
            self.stub_vec = np.mean(embeddings, axis=0)
        else:
            self.stub_vec = np.zeros_like(self.element2embedding[next(iter(self.element2embedding))])

    def __calc_vecs_for_known_elements(self, tokens):
        if len(tokens) <= 0:
            return self.stub_vec
        elif any(token in self.element2embedding for token in tokens):
            return np.mean([self.element2embedding[token] for token in tokens if token in self.element2embedding],
                           axis=0)
        else:
            return self.stub_vec

    def transform(self, X):
        vecs = np.array([self.__calc_vecs_for_known_elements(tokens) for tokens in X])
        return vecs


class Vector2VectorTransformer(dict):

    def __init__(self, vector_transformer):
        self.transformer = vector_transformer
        super().__init__()

    def __get_alias(self, vec):
        return hashlib.sha1(vec.view(np.uint8)).hexdigest()

    def fit(self, X, y=None):
        vectors2 = self.transformer.transform(X)
        print('Collecting transformed vectors.')
        self.vec2vec_ = dict(map(lambda vec, vec2: (self.__get_alias(vec), vec2), X, vectors2))
        return self

    def partial_fit(self, X, y=None):
        print('Finding new embedding entries.')
        new_alias2vec = {}
        for vec in X:
            alias = self.__get_alias(vec)
            if alias not in self.vec2vec_ and alias not in new_alias2vec:
                new_alias2vec[alias] = vec

        # Transform to sense vectors
        print('Calculating embedding distances to senses.')
        aliases, vecs = zip(*new_alias2vec.items())
        transformed_vecs = self.transformer.transform(np.array(vecs))

        # Add to tokenVec2senseVec dictionary
        print('Collecting sense vectors.')
        self.vec2vec_.update(zip(aliases, transformed_vecs))
        return self

    def transform(self, X):
        aliases = [self.__get_alias(vec) for vec in X]
        return np.array([self.vec2vec_[vec_alias] if vec_alias in self.vec2vec_ else None
                         for vec_alias in aliases])


class TfidfEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        self.word2weight_ = None
        self.dim = len(next(iter(word2vec.items()))[1])
        self.empty_stub = np.zeros(self.dim)

    def fit(self, X, y=None):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(X)
        # if a word was never seen - it must be at least as infrequent
        # as any of the known words - so the default idf is the max of
        # known idf's
        max_idf = max(tfidf.idf_)
        self.word2weight_ = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] * self.word2weight_[w]
                     for w in words if w in self.word2vec] or
                    [self.empty_stub], axis=0)
            for words in X
        ])
