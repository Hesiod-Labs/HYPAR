import spacy
from zipfile import ZipFile
import os
import pandas as pd
import PyPDF2
import docx2txt
from datetime import date


# accumulation of helper methods
# english dictionary used
nlp = spacy.load('en_core_web_sm')


def extract_pdf_text(pdf_file):
    f = open(pdf_file, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(f)
    result_file = open(f"{pdf_file.replace('.pdf', '.txt')}", 'w+')
    for index in range(pdf_reader.numPages):
        page = pdf_reader.getPage(index)
        result_file.write(page.extractText())
    f.close()


def format_zip(file):
    zp = ZipFile(file, 'r')
    zp.extractall(os.getcwd())
    nl = zp.namelist()
    if '__MACOSX/' in nl:
        nl.remove('__MACOSX/')
    return nl


# files not accepted: xml, html, images: could also be used to download any file on a computer: .conf, .md, etc
def retrieve(filepath, file_type):
    accepted_files = {
        'txt': lambda file: open(f'{file}', 'r+').read(),
        'csv': lambda file: pd.read_csv(f'{filepath}'),
        'xlsx': lambda file: pd.read_excel(f'{filepath}'),
        'json': lambda file: pd.read_json(f'{filepath}'),
        'hdf': lambda file: pd.read_hdf(f'{filepath}'),
        'pdf': lambda file: Tutor.extract_pdf_text(filepath),
        'tsv': lambda file: pd.read_csv(f'{filepath}'),
        'docx': lambda file: docx2txt.process(f'{filepath}')
    }
    return accepted_files[file_type]


def move_files(topic, repository):
    for file in topic.files:
        os.rename(f'{file}', f'{repository}/{file}')


# text_gen helper method 1
def generic_file_extraction(filepath):
    # zip files not currently accepted
    file_type = filepath.split('.')[1]
    return retrieve(filepath, file_type)


# make a directory and change into it
def mcdir(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    os.chdir(filepath)


def percent_change(number, changer):
    divide = (changer - number) / number
    if number > changer:
        divide = -divide
    return divide * 100


# dates taken in as strings
def days_between(date1, date2):
    # '2018-01-01', '2018-12-31'
    one_split = date1.split('-')
    two_split = date2.split('-')
    date_one = date(int(one_split[0]), int(one_split[1]), int(one_split[2]))
    date_two = date(int(two_split[0]), int(two_split[1]), int(two_split[2]))
    delta = date_two - date_one
    return delta.days
