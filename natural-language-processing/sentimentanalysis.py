import spacy
from scipy import spatial
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd


# aqnalysis of stocks of the same kind like all the banks or cetain banks tech etc and
# see how their movements are related in a given day, year, earnigns report etc


# sentiment analysis
class SentimentAnalysis:
    nlp = spacy.load('en_core_web_md')  # make sure to use a larger model!
    nltk.downloader.download('vader_lexicon')

    # It's sometimes helpful to aggregate 300 dimensions into a Euclidian (L2) norm, computed as the
    # square root of the sum-of-squared-vectors. This is accessible as the .vector_norm token attribute.
    # Other helpful attributes include .has_vector and .is_oov or out of vocabulary.
    # can do things like find the highest and lowest similarity with token.similarity(token)

    @staticmethod
    def cosine_similarity(word_one, word_two):
        return 1 - spatial.distance.cosine(word_one, word_two)

    # similarity companion helper method, can use this to create the method like go though the word and if it
    # does not have related vectors or does not meet the is alpha, is lower, has vector, else don't record it
    @staticmethod
    def related_words(vector_equation):
        # returnable list of similar words
        computed_similarities = []
        # need to find a way to realistically evaluate the vectos in the input
        for word in SentimentAnalysis.nlp.vocab:
            if word.is_alpha and word.has_vector:
                similarity = SentimentAnalysis.cosine_similarity(vector_equation.vector, word.vector)
                computed_similarities.append((word, similarity))
        similar_words = sorted(computed_similarities, key=lambda item: -item[1])
        return [w[0].text for w in similar_words[:10]]

    # negative, neutral, positive, compound (computed by normalizing the scores above)
    # coi: column of interest what determines the result, roi: result of interest object of interest
    @staticmethod
    def vader_analysis(file, attribute_oi):
        # polarity_scores,
        sentiment_analyzer = SentimentIntensityAnalyzer()
        data = pd.read_csv(file)
        # adding scores to the data-frame
        data['Sentiment Scores'] = data[attribute_oi].apply(lambda label_score: sentiment_analyzer.polarity_scores(label_score))
        data['Compound Score'] = data['Sentiment Scores'].apply(lambda score_dict: score_dict['Compound Score'])
        data['Positive'] = data['Sentiment Scores'].apply(lambda score_dict: score_dict['pos'])
        data['Negative'] = data['Sentiment Scores'].apply(lambda score_dict: score_dict['neg'])
        data['Neutral'] = data['Sentiment Scores'].apply(lambda score_dict: score_dict['neu'])
        data['Assigned Label'] = data['Compound Score'].apply(lambda c: 'pos' if c >= 0 else 'neg')
        return [accuracy_score(data[attribute_oi], data['Compound Score']),
                classification_report(data[attribute_oi], data['Compound Score']),
                confusion_matrix(data[attribute_oi], data['Compound Score'])]
