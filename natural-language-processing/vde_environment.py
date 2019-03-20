# NLP Environment creation for analysis of VDE

import spacy
import os
from engine import search, wikipedia
from tutor import mcdir, chback, move_files, nlp, generic_file_extraction, format_zip
import re
from nltk.stem.snowball import SnowballStemmer


# the Topic for the sub-environment repository
class Topic:

    def __init__(self, name, titles, files):
        self.description = open(f'{name}')
        self.titles = titles
        self.files = files
        self.topic_dict = {}
        for name, page in zip(titles, files):
            self.topic_dict.update({name: page})


# vocab, document, entity repository
class VDE:
    # if the entity is non real then just throw a non-real entity exception and delete it
    stemmer = SnowballStemmer(language='english')

    @staticmethod
    def absorb(repository, topic):
        # overarching repository creation
        os.mkdir(repository)
        move_files(topic, repository)
        mcdir(repository)
        file_list = generic_file_extraction(topic.files)
        for subtopic in topic.titles:
            for file in file_list:

                f_text = open(file, 'r+').read()
                mcdir(f"{file.replace('.txt', '')}")
                recorder = nlp(f_text)

                # record entities
                mcdir('Entities')
                cwd = os.getcwd()
                ent_list = list(recorder.ents)
                # inside the Entities repository
                for entity in ent_list:
                    # creating entity sub repositories based on label
                    mcdir(f'{entity.label_}')
                    mcdir(f'{entity}.txt')
                    # recording the entity in the sub repository
                    f = open(f'{entity}.txt', 'w+')
                    f.write(f'Entity Plain Text: {entity.text}\n')
                    f.write(f'Label: {entity.label_}\n')
                    pattern = re.compile('\W')
                    # sub('[^A-Za-z/ ]', '', n)
                    wp = search(re.sub(pattern, 'None', entity))
                    if wp is not None:
                        f.write(f'{wp.title} : {wp.url}\n')
                        f.write(f'{wikipedia.summary(wp.title, sentences=10)}')
                    os.chdir(cwd)
                chback(2)

                # record vocabulary
                mcdir('Vocabulary')
                for word in recorder:
                    if not word.is_stop and not os.path.exists(f'{word}.txt'):  # duplicate entities
                        doc = open(f'{word}.txt', 'w+')
                        doc.write(f'{word}\n')
                        # prints pos + explanation, fine grain pos + explanation
                        doc.write(f'Part of Speech:{word.pos_:{6}} '
                                  f'{spacy.explain(word.pos_):{6}} '
                                  f'{spacy.explain(word.tag_)}\n')
                        doc.write(f'Stem: {VDE.stemmer.stem(word)}')
                        # record the stem of the word
                        search(word)
                    # look up the definition of a word in the search engine, etc
                chback(1)

                chback(1)
                os.rename(f'{file}', f"{file.replace('.txt', '')}/{file}")

        os.chdir(repository)

    def __init__(self, repository_name, topic_name, topic_titles, topic_files):
        repository_topic = Topic(topic_name, topic_titles, topic_files)
        VDE.absorb(repository_name, repository_topic)
