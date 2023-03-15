from sklearn.feature_extraction.text import CountVectorizer

# Global and constant
DEFAULT_CV = 10

CLASSIFIER = "Classifier"
HYPERPARAMETER = "Hyperparameter"
BEST_HYPERPARAMETER = "Best Hyperparameter"
BEST_SCORE = "Best Score"
LOWER_BOUND = "Lower Bound"
UPPER_BOUND = "Upper Bound"
F1_SCORE = "F1 Score"
RECALL = "Recall"
ACCURACY = "Accuracy"
PRECISION = "Precision"
PREDICTION = "Prediction"

# We also define an object to map the monuments between their labels and their category
LABELS_NAMES = {
    0: "Château",
    1: "Eglise",
    2: "Maison",
    3: "Autre",
    4: "Croix",
    6: "Chapelle",
    7: "Immeuble",
    9: "Monument aux morts",
    10: "Hôtel",
    11: "Fontaine",
    12: "Pont",
    13: "Musée",
    14: "Ferme"
}

CATEGORIES = list(LABELS_NAMES.values())

vectorizer = CountVectorizer()