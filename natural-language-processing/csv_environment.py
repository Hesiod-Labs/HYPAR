import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
# exception modules
from exceptions import ImproperModelError
from tutor import format_zip
import os


# machine learning implementation and processing of csv files
class CSV:

    @staticmethod
    def topic_model(model_name, file, topic):  # model types: LDA, NMF
        nl = format_zip(file)
        topics = []
        for csv in nl:
            ds = pd.read_csv(csv)
            if model_name is 'LDA':
                vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
                dtm = vectorizer.fit_transform(ds[topic])
                model = LatentDirichletAllocation(n_components=7, random_state=42)  # what else besides 7 and 42?
            elif model_name is 'NMF':
                vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
                dtm = vectorizer.fit_transform(ds[topic])
                model = NMF(n_components=7, random_state=42)  # change 42 or 7?
            else:
                raise ImproperModelError('The Model is not currently supported')
            model.fit(dtm)
            readme = open(f"rm_{file}.txt", 'w+')
            output = []
            for index, topic in enumerate(model.components_):
                output.append([vectorizer.get_feature_names()[i] for i in topic.argsort()[-10:]])
                readme.write(str(output))
            topic_results = model.transform(dtm)
            dataset = ds['Topic'] = topic_results.argmax(axis=1)
            readme.write(str(dataset))
            topics.append(readme)
        if os.path.exists(f'{file}'):
            os.remove(f'{file}')
        return topics

    def __init__(self, model, file, topic):
        CSV.topic_model(model, file, topic)
