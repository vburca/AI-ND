import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Baysian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # Set initial best log likelihood score as +inf; we care about low BIC scores
        best_bic = float("+inf")
        # Set initial default value for best number of states
        best_num_states = self.n_constant

        seqs, features = self.X.shape

        # Iterate over all the possible numbers of components
        for num_states in range(self.min_n_components, self.max_n_components + 1):
            model = self.base_model(num_states)

            # states + states * (states - 1) + states * features * 2
            p = num_states + num_states * (num_states - 1) + num_states * features * 2

            try:
                logL = model.score(self.X, self.lengths)
                bic = -2 * logL + p * np.log(seqs)

                if bic < best_bic:
                    best_bic = bic
                    best_num_states = num_states
            except:
                continue

        return self.base_model(best_num_states)


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def _dic_score(self, logL, logL_sum, M):
        # Return the dic score, based on the formula above
        return logL - (logL_sum - logL) / (M - 1)

    def _best_num_states(self, numstates_scores):
        # If we were not able to calculate the score for any of number of states, return the default
        if len(numstates_scores):
            return self.n_constant

        scores_sum = sum(numstates_scores)
        # Calculate each individual dic score
        M = len(numstates_scores)
        dic_scores = [self._dic_score(s, scores_sum, M) for s in numstates_scores]
        # Get the index of the max dic score
        max_dic_score_i = np.argmax(dic_scores)
        # This will correspond to the index of the number of states that generated this dic score
        num_states = numstates_scores.keys()
        return num_states[max_dic_score_i]

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # Keep track of all the scores for each number of states
        numstates_scores = {}

        # Iterate over all the possible numbers of components
        for num_states in range(self.min_n_components, self.max_n_components + 1):
            model = self.base_model(num_states)

            try:
                logL = model.score(self.X, self.lengths)
                numstates_scores[num_states] = logL
            except:
                continue

        return self.base_model(self._best_num_states(numstates_scores))


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # Since we are using the default KFold split, which works over 3 splits, we need to check
        # how many sequences we have for this word
        # If we do not have at least 3 sequences, do not use the splitting method
        if len(self.sequences) < 3:
            return self.base_model(self.n_constant)

        # Set the splitting method
        split_method = KFold()

        # Set initial best log likelihood score as -inf
        best_log_likelihood = float("-inf")
        # Set initial default value for best number of states
        best_num_states = self.n_constant

        # Iterate over all the possible numbers of components
        for num_states in range(self.min_n_components, self.max_n_components + 1):
            scores = []

            # Do the split and train on each training combination
            for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                train_X, train_Xlengths = combine_sequences(cv_train_idx, self.sequences)
                test_X, test_Xlengths = combine_sequences(cv_test_idx, self.sequences)

                try:
                    model = GaussianHMM(n_components=num_states, covariance_type='diag', n_iter=1000,
                                        random_state=self.random_state).fit(train_X, train_Xlengths)
                    scores.append(model.score(test_X, test_Xlengths))
                except:
                    # If we encounter an error, skip
                    continue

            # Now, if we have some scores for this number of states, find the best score; if there are no scores,
            # continue to next number of states
            if len(scores) <= 0:
                continue

            # Update the best score, averaging over the current num_states' scores
            scores_mean = np.mean(scores)
            if best_log_likelihood < scores_mean:
                best_log_likelihood = scores_mean
                best_num_states = num_states

        return self.base_model(best_num_states)