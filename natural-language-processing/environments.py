# NLP Environment creation for analysis of VDE

import spacy
import os
from engine import search, wikipedia
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
# exception modules
from exceptions import ImproperModelError
from tutor import Tutor
import re
from nltk.stem.snowball import SnowballStemmer


# the Topic for the sub-environment repository
class Topic:

    def __init__(self, titles, files):
        self.titles = titles
        self.files = files
        self.topic_dict = {}
        for name, zp in zip(titles, files):
            self.topic_dict.update({name: zp})


# vocab, document, entity repository
class VDE:
    # if the entity is non real then just throw a non-real entity exception and delete it

    @staticmethod
    def stem(word):
        stemmer = SnowballStemmer(language='english')
        return stemmer.stem(word)

    # record the words in a given document
    @staticmethod
    def record_words(recorder):
        Tutor.mcdir('Vocabulary')
        for word in recorder:
            if not word.is_stop and not os.path.exists(f'{word}.txt'):  # duplicate entities
                doc = open(f'{word}.txt', 'w+')
                doc.write(f'{word}\n')
                # prints pos + explanation, fine grain pos + explanation
                doc.write(f'Part of Speech:{word.pos_:{6}} {spacy.explain(word.pos_):{6}} {spacy.explain(word.tag_)}\n')
                search(word)
            # look up the definition of a word in the search engine, etc
        os.chdir('..')

    # record new entities for the specific entity sub repositories
    @staticmethod
    def record_entities(recorder):
        Tutor.mcdir('Entities')
        cwd = os.getcwd()
        ent_list = list(recorder.ents)
        # inside the Entities repository
        for entity in ent_list:
            # creating entity sub repositories based on label
            Tutor.mcdir(f'{entity.label_}')
            Tutor.mcdir(f'{entity}.txt')
            # recording the entity in the sub repository
            f = open(f'{entity}.txt', 'w+')
            f.write(f'Entity Plain Text: {entity.text}\n')
            f.write(f'Label: {entity.label_}\n')
            pattern = re.compile('\W')
            #sub('[^A-Za-z/ ]', '', n)
            #
            wp = search(re.sub(pattern, 'None', entity))
            if wp is not None:
                f.write(f'{wp.title} : {wp.url}\n')
                f.write(f'{wikipedia.summary(wp.title, sentences=10)}')
            os.chdir(cwd)
        os.chdir('..')
        os.chdir('..')

    @staticmethod
    def enjoy_file(file):
        f_text = open(file, 'r+').read()
        Tutor.mcdir(f"{file.replace('.txt', '')}")
        recorder = Tutor.nlp(f_text)
        # record entities
        VDE.record_entities(recorder)
        # record vocabulary
        VDE.record_words(recorder)
        os.chdir('..')
        os.rename(f'{file}', f"{file.replace('.txt', '')}/{file}")

    # vde_dict format will be in Vocab, Document, Entity format
    @staticmethod
    def main(repository, topic):  # repository is a name, topic contains the titles and zips
        # overarching repository creation
        os.mkdir(repository)
        Tutor.move_files(topic, repository)
        Tutor.mcdir(repository)
        file_list = Tutor.generic_file_extraction(topic.files)
        for subtopic in topic.titles:
            for file in file_list:
                VDE.enjoy_file(file)
        os.chdir(repository)

    def __init__(self, topic):
        VDE.main('VDE_Repository', topic)


# machine learning implementation and processing of csv files
class CSV:

    @staticmethod
    def topic_model(model_name, file, topic):  # model types: LDA, NMF
        nl = Tutor.format_zip(file)
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

    @staticmethod
    def main(model_name, file, topic):
        CSV.topic_model(model_name, file, topic)

    def __init__(self, model_name, file, topic):
        CSV.main(model_name, file, topic)
