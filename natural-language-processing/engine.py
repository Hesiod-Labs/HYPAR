import wolframalpha  # https://pypi.org/project/wolframalpha/
import wikipedia  # https://pypi.org/project/wikipedia/1.4.0/
from wikipedia import PageError
import wikipediaapi
import spacy


nlp = spacy.load('en_core_web_sm')
w_client = wolframalpha.Client("5Y5EE6-YHE62W22W3")
# Web scraping for google searchable with return information as first line type questions
wiki = wikipediaapi.Wikipedia('en')
accepted_labels = ['PERSON', 'ORG', 'NORP', 'FAC', 'GPE', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE']
wolfram_query = False  # do not know how to quantify this yet


def search(query):
    # single entity for now
    entity = nlp(query)
    if str(entity.label_) in accepted_labels:
        # if the query is a valid wikipedia entry
        if not wiki.page(str(entity)).exists():
            raise PageError(f'{entity} does not correspond to a valid Wikipedia page')
        page = wikipedia.page(entity)
        # can do a lot more here than just return the Wikipedia page
        return page
    if wolfram_query:
        # if the query is a wolfram alpha query
        res = w_client.query(str(entity))
        return next(res.results).text
