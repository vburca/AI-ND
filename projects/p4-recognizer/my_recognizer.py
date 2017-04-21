import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []

    for X, len in test_set.get_all_Xlengths().values():
        score = float("-inf")
        guess = None
        x_probs = {}

        for word, model in models.items():
            try:
                # Get the score
                logL = model.score(X, len)
                x_probs[word] = logL

                # If score is higher, update score and guess
                if score < logL:
                    score = logL
                    guess = word
            except:
                # Couldn't train
                x_probs[word] = float("-inf")
                continue

        guesses.append(guess)
        probabilities.append(x_probs)

    return probabilities, guesses