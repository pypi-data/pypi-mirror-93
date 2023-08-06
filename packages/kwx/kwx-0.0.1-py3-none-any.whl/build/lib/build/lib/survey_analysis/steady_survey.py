# coding: utf-8

# =============================================================================
# Survey keyword cleaning, modeling, analysis, and generation
#
# Contents
# --------
#   0. NoClass
#       update_dependencies
#
#       load_survey_data
#       _combine_tokens_to_str
#       _clean_text_strings
#       clean_and_tokenize_texts
#       prepare_survey_data
#       _prepare_corpus_path
#
#       get_topic_words
#       get_coherence
#       _order_and_subset_by_coherence
#
#       graph_topic_num_evals
#       gen_word_cloud
#       pyLDAvis_topics
#
#       translate_output
#       _order_by_pos
#       gen_survey_keywords
#       prompt_for_ignore_words
#       gen_analysis_files
#
#   1. Autoencoder
#       __init__
#       _compile
#       fit
#
#   2. TopicModel
#       __init__
#       _vectorize
#       fit
#       predict
# =============================================================================

# Packages included in the Python standard library: https://docs.python.org/3/library/index.html
import os
import math
import time
from datetime import datetime
import random
import string
import re
import inspect
import zipfile
import io
from collections import defaultdict, Counter
from subprocess import PIPE, Popen
import warnings
warnings.filterwarnings('ignore', category=Warning)
warnings.filterwarnings('ignore', category=DeprecationWarning) 

# Packages not included in the standard library
try:
    import numpy as np
except:
    os.system('pip install numpy')
    import numpy as np

try:
    import pandas as pd
except:
    os.system('pip install xlrd')
    os.system('pip install pandas')
    import pandas as pd

try:
    from stopwordsiso import stopwords
except:
    os.system('pip install stopwordsiso')
    from stopwordsiso import stopwords

try:
    import gensim
    from gensim.models import Phrases, LdaModel, CoherenceModel
    from gensim import corpora
except:
    os.system('pip install gensim')
    import gensim
    from gensim.models import Phrases, LdaModel, CoherenceModel
    from gensim import corpora

try:
    from IPython.display import display
except:
    os.system('pip install ipython')
    from IPython.display import display

try:
    import pyLDAvis
    import pyLDAvis.gensim
except:
    os.system('pip install pyLDAvis')
    import pyLDAvis
    import pyLDAvis.gensim

try:
    from wordcloud import WordCloud
except:
    os.system('pip install wordcloud')
    from wordcloud import WordCloud

try:
    import nltk
    from nltk.stem.snowball import SnowballStemmer
except:
    os.system('pip install nltk')
    import nltk
    from nltk.stem.snowball import SnowballStemmer

try:
    import spacy
except:
    os.system('pip install spacy')
    import spacy

try:
    import emoji
except:
    os.system('pip install emoji')
    import emoji

try:
    from googletrans import Translator
except:
    os.system('pip install googletrans')
    from googletrans import Translator

try:
    import matplotlib.pyplot as plt
except:
    os.system('pip install matplotlib')
    import matplotlib.pyplot as plt

try:
    import seaborn as sns
except:
    os.system('pip install seaborn')
    import seaborn as sns

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    from sklearn.model_selection import train_test_split
except:
    os.system('pip install sklearn')
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    from sklearn.model_selection import train_test_split

try:
    from sentence_transformers import SentenceTransformer
except:
    os.system('pip install sentence_transformers')
    from sentence_transformers import SentenceTransformer

try:
    import tensorflow as tf
    tf.get_logger().setLevel('ERROR')
    import keras
    from keras.layers import Input, Dense
    from keras.models import Model
except:
    os.system('pip install tensorflow')
    os.system('pip install keras')
    import tensorflow as tf
    tf.get_logger().setLevel('ERROR')
    import keras
    from keras.layers import Input, Dense
    from keras.models import Model

# The following languages have been selected because:
# Their stopwords can be removed via https://github.com/stopwords-iso/stopwords-iso/tree/master/python

# Their following can be lemmatized via https://spacy.io/usage/models
# These languages are also those that can have their words ordered by part of speech
lem_lang_abbr_dict = {'chinese': 'zh',
                      'danish': 'da',
                      'dutch': 'nl',
                      'english': 'en',
                      'french': 'fr',
                      'german': 'de',
                      'greek': 'el',
                      'italian': 'it',
                      'japaneze': 'ja',
                      'lithuanian': 'lt',
                      'norwegian': 'nb',
                      'polish': 'pl',
                      'portugese': 'pt',
                      'romanian': 'ro',
                      'spanish': 'es'}

# Hungarian and other languages don't have good lemmatizers, and will thus be stemmed via: https://www.nltk.org/api/nltk.stem.html
stem_lang_abbr_dict = {'arabic': 'ar',
                       'finnish': 'fi',
                       'hungarian': 'hu',
                       'swedish': 'sv'}

# The final languages can only have their stopwords removed (see https://github.com/stopwords-iso/stopwords-iso to potentially expand this)
stop_wrods_lang_abbr_dict = {'afrikaans': 'af',
                             'bulgarian': 'bg',
                             'bengali': 'bn',
                             'breton': 'br',
                             'catalan': 'ca',
                             'czech': 'cs',
                             'esperanto': 'eo',
                             'estonian': 'et',
                             'basque': 'eu',
                             'farsi': 'fa',
                             'persian': 'fa',
                             'irish': 'ga',
                             'galician': 'gl',
                             'gujarati': 'gu',
                             'hausa': 'ha',
                             'hebrew': 'he',
                             'hindi': 'hi',
                             'croatian': 'hr',
                             'armenian': 'hy',
                             'indonesian': 'id',
                             'korean': 'ko',
                             'kurdish': 'ku',
                             'latin': 'la',
                             'latvian': 'lv',
                             'marathi': 'mr',
                             'malay': 'ms',
                             'norwegian': 'no',
                             'russian': 'ru',
                             'slovak': 'sk',
                             'slovenian': 'sl',
                             'somali': 'so',
                             'sotho': 'st',
                             'swahili': 'sw',
                             'thai': 'th',
                             'tagalog': 'tl',
                             'turkish': 'tr',
                             'ukrainian': 'uk',
                             'urdu': 'ur',
                             'vietnamese': 'vi',
                             'yoruba': 'yo',
                             'zulu': 'zu'}

def update_dependencies():
    """
    Updates all packages that steady_survey depends on
    """
    package_names = ['numpy', 'pandas', 'stopwordsiso', 
                     'gensim', 'pyLDAvis', 'wordcloud', 
                     'nltk', 'spacy', 'emoji', 
                     'googletrans', 'matplotlib', 'seaborn',
                     'sklearn', 'sentence_transformers', 'keras']

    def cmdline(cmd):
        """
        Allows for command line oputputs to be shown through Python functional call of them
        """
        process = Popen(args=cmd,
                        stdout=PIPE,
                        shell=True)
        return process.communicate()[0]

    for p in package_names:
        print(cmdline('pip install {} --upgrade'.format(p))[:-1])
        print('\n')


def load_survey_data(data):
    """
    Loads survey data from a path and formats it into a pandas df

    Parameters
    ----------
        data : pd.DataFrame or csv/xlsx path
            The survey data in df or path form

    Returns
    -------
        df_responses : pd.DataFrame
            The survey responses as a df
    """
    if type(data) == str:
        if data[-len('xlsx'):] == 'xlsx':
            df_responses = pd.read_excel(io=data)
        elif data[-len('csv'):] == 'csv':
            df_responses = pd.read_csv(filepath_or_buffer=data)
        else:
            df_responses = data

    column_names = ['user_id', 'val_benefit', 'unval_benefit', 
                    'val_personal', 'unval_personal', 
                    'most_important', 'mission_description', 'higher_purpose', 
                    'expensive_ok', 'expensive_not_ok', 'bargain_ok', 'bargain_not_ok', 
                    'likelihood_expensive', 'likelihood_bargain', 'contact_duraction', 
                    'start_time', 'submit_time', 'network_id']

    extra_index = 0
    while len(column_names) < len(df_responses.columns):
        column_names.append('extra_col_{}'.format(extra_index))
        extra_index += 1

    df_responses.columns = column_names

    for col in df_responses.columns:
        # This could be used to combine the 'Other' columns, but each dataset would then need them
        if 'other' in col:
            if df_responses[col].isnull().all():
                df_responses.drop(col, axis=1, inplace=True)
                
            else:
                col_idx = df_responses.columns.get_loc(col)
                for i in df_responses.index:
                    if type(df_responses.loc[i, col]) == str:
                        df_responses.loc[i, df_responses.columns[col_idx - 1]] = df_responses.loc[i, col]
                        
                df_responses.drop(col, axis=1, inplace=True)

    return df_responses


def _combine_tokens_to_str(responses, ignore_words=None):
    """
    Combines the survey responses into one string
    """
    if type(responses[0]) == list:
        flat_words = [word for sublist in responses for word in sublist]
    else:
        flat_words = responses

    if type(ignore_words) == str:
        ignore_words = [ignore_words]
    elif ignore_words == None:
        ignore_words = []

    flat_words = [word for word in flat_words if word not in ignore_words]
    response_str = ' '.join([word for word in flat_words])

    return response_str


def _clean_text_strings(s):
    """
    Cleans the string of a text body to prepare it for BERT analysis

    Parameters
    ----------
        s : str
            The survey combined response of a user to be cleaned

    Returns
    -------
        s : str
            The response formatted for text analysis
    """
    s = re.sub(r'([a-z])([A-Z])', r'\1\. \2', s)
    s = s.lower()
    s = re.sub(r'&gt|&lt', ' ', s)
    s = re.sub(r'([a-z])\1{2,}', r'\1', s)
    s = re.sub(r'([\W+])\1{1,}', r'\1', s)
    s = re.sub(r'\*|\W\*|\*\W', '. ', s)
    s = re.sub(r'\(.*?\)', '. ', s)
    s = re.sub(r'\W+?\.', '.', s)
    s = re.sub(r'(\.|\?|!)(\w)', r'\1 \2', s)
    s = re.sub(r' ing ', ' ', s)
    s = re.sub(r'product received for free[.| ]', ' ', s)
    s = re.sub(r'(.{2,}?)\1{1,}', r'\1', s)

    return s.strip()

def clean_and_tokenize_texts(responses,
                             input_language=None,
                             min_freq=2,
                             min_word_len=4,
                             sample_size=1):
    """
    Cleans and tokenizes a text body to prepare it for analysis

    Parameters
    ----------
        responses : str or list
            The survey response to be cleaned and tokenized

        input_language : str (default=None)
            The English name of the input_language in which the survey was conducted

        min_freq : int (default=2)
            The minimum allowable frequency of a word inside the text corpus

        min_word_len : int (default=4)
            The smallest allowable length of a word

        sample_size : float (default=None: sampling for non-BERT techniques)
            The size of a sample for BERT models

    Returns
    -------
        text_corpus, clean_texts, selection_idxs : list or list of lists (default=None), list, list
            The responses formatted for text analysis both as tokens and strings, as well as the indexes for selected entries
    """
    input_language = input_language.lower()

    # Select abbreviation for the lemmatizer, if it's available
    if input_language in lem_lang_abbr_dict.keys():
        input_language = lem_lang_abbr_dict[input_language]

    if type(responses) == str:
        responses = [responses]

    # Remove spaces that are greater that one in length
    responses_no_large_spaces = []
    for r in responses:
        for i in range(25, 0, -1): # loop backwards to assure that smaller spaces aren't made
            large_space = str(i * ' ')
            if large_space in r:
                r = r.replace(large_space, ' ')
                
        responses_no_large_spaces.append(r)

    responses_no_random_punctuation = []
    # Prevent words from being combined when a user types word/word or word-word
    for r in responses_no_large_spaces:
        r = r.replace('/', ' ')
        r = r.replace('-', ' ')
        if input_language == 'fr':
            # Get rid of the 'of' abbreviation for French
            r = r.replace("d'", '')

        responses_no_random_punctuation.append(r)
    
    # Remove punctuation
    responses_no_punctuation = []
    for r in responses_no_random_punctuation:
        responses_no_punctuation.append(r.translate(str.maketrans('', '', string.punctuation+'–'+'’')))

    # Remove emojis
    responses_no_emojis = []
    for response in responses_no_punctuation:
        responses_no_emojis.append(emoji.get_emoji_regexp().sub(r'', response))

    # Remove stopwords and tokenize
    if stopwords(input_language) != set(): # the input language has stopwords
        stop_words = stopwords(input_language)
    elif input_language in stem_lang_abbr_dict.keys():
        stop_words = stopwords(stem_lang_abbr_dict[input_language])
    elif input_language in stop_wrods_lang_abbr_dict.keys():
        stop_words = stopwords(stop_wrods_lang_abbr_dict[input_language])
    else:
        stop_words = []
    
    tokenized_texts = [[word for word in text.lower().split() if word not in stop_words and not word.isnumeric()] \
                        for text in responses_no_emojis]
    tokenized_texts = [t for t in tokenized_texts if t != []]

    # Add bigrams (first_second word combinations that appear often together)
    tokens_with_bigrams = []
    bigrams = Phrases(sentences=tokenized_texts, min_count=3, threshold=5.0) # minimum count for a bigram to be included is 3
    for i in range(len(tokenized_texts)):
        for token in bigrams[tokenized_texts[i]]:
            if '_' in token:
                # Token is a bigram, so add it to the tokens
                tokenized_texts[i].insert(0, token)
                
        tokens_with_bigrams.append(tokenized_texts[i])

    # Lemmatize or stem words
    def lemmatize(tokens):
        """
        Lemmatizes tokens (allows for one line in each of the next try and except clauses)
        """
        allowed_pos_tags = ['NOUN', 'PROPN', 'ADJ', 'ADV', 'VERB']

        lemmatized_tokens = []
        for tokens in tokens:
            combined_tokens = _combine_tokens_to_str(tokens)

            lem_tokens = nlp(combined_tokens)
            lemmed_tokens = [token.lemma_ for token in lem_tokens if token.pos_ in allowed_pos_tags]
            
            lemmatized_tokens.append(lemmed_tokens)
    
        return lemmatized_tokens

    nlp = None
    try:
        nlp = spacy.load(input_language)
        lemmatized_tokens = lemmatize(tokens_with_bigrams)

    except OSError:
        try:
            os.system('python -m spacy download {}'.format(input_language))
            nlp = spacy.load(input_language)
            lemmatized_tokens = lemmatize(tokens_with_bigrams)
        except:
            pass

    if nlp == None:
        stemmer = None
        if input_language in SnowballStemmer.languages:
            stemmer = SnowballStemmer(input_language)
        # Correct if the abbreviations were put in
        elif input_language == 'ar':
            stemmer = SnowballStemmer('arabic')
        elif input_language == 'fi':
            stemmer = SnowballStemmer('finish')
        elif input_language == 'hu':
            stemmer = SnowballStemmer('hungarian')
        elif input_language == 'sv':
            stemmer = SnowballStemmer('swedish')

        if stemmer != None:
            # Stemming instead of lemmatization
            lemmatized_tokens = [] # still call it lemmatized for consistency
            for tokens in tokens_with_bigrams:
                stemmed_tokens = [stemmer.stem(t) for t in tokens]
                lemmatized_tokens.append(stemmed_tokens)

        else:
            # We cannot lemmatize or stem
            lemmatized_tokens = tokens_with_bigrams
    
    # Remove words that don't appear enough or are too small
    token_frequencies = defaultdict(int)
    for tokens in lemmatized_tokens:
        for t in list(set(tokens)):
            token_frequencies[t] += 1
    
    if min_word_len == None or min_word_len == False:
        min_word_len = 0
    if min_freq == None or min_freq == False:
        min_freq = 0

    min_len_freq_tokens = []
    for tokens in lemmatized_tokens:
        min_len_freq_tokens.append([t for t in tokens if len(t) >= min_word_len and token_frequencies[t] >= min_freq])
    
    # Derive those responses that still have valid words
    non_empty_token_indexes = [i for i in range(len(min_len_freq_tokens)) if min_len_freq_tokens[i] != []]
    text_corpus = [min_len_freq_tokens[i] for i in non_empty_token_indexes]
    clean_texts = [_clean_text_strings(s=responses[i]) for i in non_empty_token_indexes]

    # Sample words, if necessary
    if sample_size != 1:
        selected_idxs = [i for i in random.choices(range(len(text_corpus)), k=int(sample_size * len(text_corpus)))]
    else:
        selected_idxs = list(range(len(text_corpus)))

    text_corpus = [text_corpus[i] for i in selected_idxs]
    clean_texts = [clean_texts[i] for i in selected_idxs]
    
    return text_corpus, clean_texts, selected_idxs
    

def prepare_survey_data(data=None,
                        input_language=None,
                        incl_mc_questions=False,
                        min_freq=2,
                        min_word_len=4,
                        sample_size=1):
    """
    Prepares input survey data for analysis

    Parameters
    ----------
        data : pd.DataFrame or csv/xlsx path
            The survey data in df or path form

        incl_mc_questions : bool (default=False)
            Whether to include the multiple choice questions (True) or just the free answer questions

        input_language : str (default=None)
            The English name of the input_language in which the survey was conducted

        min_freq : int (default=2)
            The minimum allowable frequency of a word inside the text corpus

        min_word_len : int (default=4)
            The smallest allowable length of a word

        sample_size : float (default=None: sampling for non-BERT techniques)
            The size of a sample for BERT models

    Returns
    -------
        text_corpus : list or list of lists
            The text corpus over which analysis should be done
    """
    input_language = input_language.lower()

    # Select abbreviation for the lemmatizer, if it's available
    if input_language in lem_lang_abbr_dict.keys():
        input_language = lem_lang_abbr_dict[input_language]

    df_responses = load_survey_data(data)

    # Select columns from which texts should come
    raw_texts = []
    if incl_mc_questions:
        included_cols = ['val_benefit', 'val_personal', 'most_important', 'mission_description', 'higher_purpose']
    else:
        included_cols = ['most_important', 'mission_description', 'higher_purpose']

    for i in df_responses.index:
        text = ''
        for c in included_cols:
            if type(df_responses.loc[i, c]) == str:
                text += ' ' + df_responses.loc[i, c]
            
        text = text[1:] # remove first blank space
        raw_texts.append(text)

    text_corpus, clean_texts, selected_idxs = clean_and_tokenize_texts(responses=raw_texts, 
                                                                       input_language=input_language, 
                                                                       min_freq=min_freq,
                                                                       min_word_len=min_word_len,
                                                                       sample_size=sample_size)

    return text_corpus, clean_texts, selected_idxs


def _prepare_corpus_path(text_corpus=None, 
                         clean_texts=None,
                         input_language=None, 
                         incl_mc_questions=False, 
                         min_freq=2, 
                         min_word_len=4, 
                         sample_size=1):
    """
    Checks a text corpus to see if it's a path, and prepares the survey data if so
    """
    if type(text_corpus) == str:
        try:
            os.path.exists(text_corpus) # a path has been provided
            text_corpus, clean_texts = prepare_survey_data(data=text_corpus,
                                                           input_language=input_language,
                                                           incl_mc_questions=incl_mc_questions,
                                                           min_freq=min_freq,
                                                           min_word_len=min_word_len,
                                                           sample_size=sample_size)[:2]
            
            return text_corpus, clean_texts

        except:
            pass
    
    if clean_texts != None:
        return text_corpus, clean_texts

    else:
        return text_corpus, [_clean_text_strings(_combine_tokens_to_str(t_c)) for t_c in text_corpus]


def get_topic_words(text_corpus, 
                    labels, 
                    num_topics=None, 
                    num_keywords=None):
    """
    Get top words within each topic for cluster models
    """
    if num_topics == None:
        num_topics = len(np.unique(labels))
    topics = ['' for _ in range(num_topics)]
    for i, c in enumerate(text_corpus):
        topics[labels[i]] += (' ' + ' '.join(c))

    # Count the words that appear for a given topic label
    word_counts = list(map(lambda x: Counter(x.split()).items(), topics))
    word_counts = list(map(lambda x: sorted(x, key=lambda x: x[1], reverse=True), word_counts))

    topics = list(map(lambda x: list(map(lambda x: x[0], x[:num_keywords])), word_counts))

    non_blank_topic_idxs = [i for i in range(len(topics)) if topics[i] != []]
    topics = [topics[i] for i in non_blank_topic_idxs]

    return topics, non_blank_topic_idxs


def get_coherence(model, 
                  text_corpus, 
                  num_topics=15, 
                  num_keywords=15, 
                  measure='c_v'):
    """
    Gets model coherence from gensim.models.coherencemodel
    
    Parameters
    ----------
        model : steady_survey.TopicModel
            A model trained on the given text corpus

        text_corpus : list, list of lists, or str
            The text corpus over which analysis should be done
            Note 1: generated using prepare_survey_data

        num_topics : int (default=15)
            The number of categories for LDA and BERT based approaches

        num_keywords : int (default=15)
            The number of keywords that should be generated

        measure : str (default=c_v)
            A gensim measure of coherence

    Returns
    -------
        coherence : float
            The coherence of the given model over the given texts
    """
    if model.method.lower() == 'lda':
        cm = CoherenceModel(model=model.lda_model, 
                            texts=text_corpus, 
                            corpus=model.bow_corpus, 
                            dictionary=model.dirichlet_dict,
                            coherence=measure)
    else:
        topic_words = get_topic_words(text_corpus=text_corpus, 
                                      labels=model.cluster_model.labels_, 
                                      num_topics=num_topics, 
                                      num_keywords=num_keywords)[0]

        cm = CoherenceModel(topics=topic_words, 
                            texts=text_corpus, 
                            corpus=model.bow_corpus, 
                            dictionary=model.dirichlet_dict,
                            coherence=measure)

    coherence = cm.get_coherence()

    return coherence
    

def _order_and_subset_by_coherence(model, 
                                   num_topics=15,
                                   num_keywords=15):
    """
    Orders topics based on their average coherence across the text corpus

    Parameters
    ----------
        model : steady_survey.TopicModel
            A model trained on the given text corpus

        num_topics : int (default=15)
            The number of categories for LDA and BERT based approaches

        num_keywords : int (default=15)
            The number of keywords that should be generated

    Returns
    -------
        ordered_topic_words, selection_indexes: list of lists and list of lists
            Topics words ordered by average coherence and indexes by which they should be selected
    """
    # Derive average topics across responses for a given method
    if model.method == 'lda':
        shown_topics = model.lda_model.show_topics(num_topics=num_topics, 
                                                   num_words=num_keywords,
                                                   formatted=False)

        topic_words = [[word[0] for word in topic[1]] for topic in shown_topics]
        topic_corpus = model.lda_model.__getitem__(bow=model.bow_corpus, eps=0) # cutoff probability to 0 

        topics_per_response = [response for response in topic_corpus]
        flat_topic_coherences = [item for sublist in topics_per_response for item in sublist]

        topic_averages = [(t, sum([t_c[1] for t_c in flat_topic_coherences if t_c[0] == t]) / len(model.bow_corpus)) \
                          for t in range(num_topics)]

    elif model.method == 'bert' or model.method == 'lda_bert':
        # The topics in cluster models are not guranteed to be the size of num_keywords
        topic_words, non_blank_topic_idxs = get_topic_words(text_corpus=model.text_corpus, 
                                                            labels=model.cluster_model.labels_, 
                                                            num_topics=num_topics, 
                                                            num_keywords=num_keywords)

        # Create a dictionary of the assignment counts for the topics
        counts_dict = dict(Counter(model.cluster_model.labels_))
        counts_dict = {k: v for k, v in counts_dict.items() if k in non_blank_topic_idxs}
        keys_ordered = sorted([k for k in counts_dict.keys()])

        # Map to the range from 0 to the number of non-blank topics
        counts_dict_mapped = {i: counts_dict[keys_ordered[i]] for i in range(len(keys_ordered))}

        # Derive the average assignment of the topics
        topic_averages = [(k, counts_dict_mapped[k]/sum(counts_dict_mapped.values())) for k in counts_dict_mapped.keys()]
    
    # Order ids by the average coherence across the responses
    topic_ids_ordered = [tup[0] for tup in sorted(enumerate(topic_averages), key=lambda i:i[1][1])[::-1]]
    ordered_topic_words = [topic_words[i] for i in topic_ids_ordered]

    ordered_topic_averages = [tup[1] for tup in sorted(topic_averages, key=lambda i:i[1])[::-1]]
    ordered_topic_averages = [a / sum(ordered_topic_averages) for a in ordered_topic_averages] # normalize just in case

    # Create selection indexes for each topic given its average coherence and how many keywords are wanted
    selection_indexes = [list(range(int(math.floor(num_keywords * ordered_topic_averages[i])))) \
                            if math.floor(num_keywords * ordered_topic_averages[i]) > 0 else [0] \
                                for i in range(len(ordered_topic_averages))]
    
    total_indexes = sum([len(i) for i in selection_indexes])
    s_i = 0
    while total_indexes < num_keywords:
        selection_indexes[s_i] = selection_indexes[s_i] + [selection_indexes[s_i][-1]+1]
        s_i += 1
        total_indexes += 1

    return ordered_topic_words, selection_indexes


def graph_topic_num_evals(method=['lda', 'lda_bert'],
                          text_corpus=None, 
                          clean_texts=None,
                          input_language=None,
                          num_keywords=15,
                          topic_nums_to_compare=None,
                          incl_mc_questions=False,
                          min_freq=2,
                          min_word_len=4,
                          sample_size=1,
                          metrics=True,
                          fig_size=(20,10),
                          save_file=False,
                          return_ideal_metrics=False):
    """
    Graphs metrics for the given models over the given number of topics

    Parameters
    ----------
        method : str (default=lda_bert)
            The modelling method

            Options:
                LDA: Latent Dirichlet Allocation
                    - Survey data is classified into a given number of categories
                    - These categories are then used to classify individual entries given the percent they fall into categories
                BERT: Bidirectional Encoder Representations from Transformers
                    - Words are classified via Google Neural Networks
                    - Word classifications are then used to derive topics
                LDA_BERT: Latent Dirichlet Allocation with BERT embeddigs
                    - The combination of LDA and BERT via an autoencoder

        text_corpus : list, list of lists, or str
            The text corpus over which analysis should be done
            Note 1: generated using prepare_survey_data
            Note 2: if a str is provided, then the data will be loaded from a path

        clean_texts : list
            Text strings that are formatted for cluster models

        input_language : str (default=None)
            The spoken language in which the survey was conducted

        num_keywords : int (default=15)
            The number of keywords that should be generated

        topic_nums_to_compare : list (default=None)
            The number of topics to compare metrics over
            Note: None selects all numbers from 1 to num_keywords

        incl_mc_questions : bool (default=False)
            Whether to include the multiple choice questions (True) or just the free answer questions
            Note: included so that it can be passed to prepare_survey_data if a path is provided

        min_freq : int (default=2)
            The minimum allowable frequency of a word inside the text corpus

        min_word_len : int (default=4)
            The smallest allowable length of a word

        sample_size : float (default=None: sampling for non-BERT techniques)
            The size of a sample for BERT models

        metrics : str or bool (default=True: all metrics)
            The metrics to include

            Options:
                stability: model stability based on Jaccard similarity

                coherence: how much the words assosciated with model topics co-occur

        fig_size : tuple (default=(20,10))
            The size of the figure

        save_file : bool or str (default=False)
            Whether to save the figure as a png or a path in which to save it

        return_ideal_metrics : bool (default=False)
            Whether to return the ideal number of topics for the best model based on metrics

    Returns
    -------
        ax : matplotlb axis
            A graph of the given metrics for each of the given models based on each topic number

        
    """
    assert metrics == 'stability' or metrics == 'coherence' or metrics == True, \
        "An invalid value has been passed to the 'metrics' argument - please choose from 'stability', 'coherence', or True for both."

    if metrics == True:
        metrics = ['stability', 'coherence']

    if type(method) == str:
        method = [method]

    method = [m.lower() for m in method]

    input_language = input_language.lower()

    if input_language in lem_lang_abbr_dict.keys():
        input_language = lem_lang_abbr_dict[input_language]

    text_corpus, clean_texts = _prepare_corpus_path(text_corpus=text_corpus,
                                                    clean_texts=clean_texts,
                                                    input_language=input_language, 
                                                    incl_mc_questions=incl_mc_questions, 
                                                    min_freq=min_freq, 
                                                    min_word_len=min_word_len, 
                                                    sample_size=sample_size)

    def jaccard_similarity(topic_1, topic_2):
        """
        Derives the Jaccard similarity of two topics

        Jaccard similarity:
            - A statistic used for comparing the similarity and diversity of sample sets
            - J(A,B) = (A ∩ B)/(A ∪ B)
            - Goal is low Jaccard scores for coverage of the diverse elements
        """
        # Fix for cases where there are not enough responses for clustering models
        if topic_1 == [] and topic_2 != []:
            topic_1 = topic_2
        if topic_1 != [] and topic_2 == []:
            topic_2 = topic_1
        if topic_1 == [] and topic_2 == []:
            topic_1, topic_2 = ['_None'], ['_None']
        intersection = set(topic_1).intersection(set(topic_2))
        num_intersect = float(len(intersection))

        union = set(topic_1).union(set(topic_2))
        num_union = float(len(union))
   
        return num_intersect / num_union

    plt.figure(figsize=fig_size) # begin figure
    metric_vals = [] # add metric values so that figure y-axis can be scaled

    # Initialize the topics numbers that models should be run for
    if topic_nums_to_compare == None:
        topic_nums_to_compare = list(range(num_keywords+2))[1:]
    else:
        # If topic numbers are given, then add one more for comparison
        topic_nums_to_compare = topic_nums_to_compare + [topic_nums_to_compare[-1]+1]

    bert_model = None
    if 'bert' in method or 'lda_bert' in method:
        # Multilingual BERT model trained on the top 100+ Wikipedias for semantic textual similarity
        bert_model = SentenceTransformer('xlm-r-bert-base-nli-stsb-mean-tokens')

    ideal_topic_num_dict = {}
    for m in method:
        topics_dict = {}
        stability_dict = {}
        coherence_dict = {}

        for t_n in topic_nums_to_compare:
            tm = TopicModel(num_topics=t_n, method=m, bert_model=bert_model)
            tm.fit(texts=clean_texts, 
                   text_corpus=text_corpus, 
                   method=m, 
                   m_clustering=None)

            # Assign topics given the current number t_n
            topics_dict[t_n] = _order_and_subset_by_coherence(model=tm,
                                                              num_topics=t_n,
                                                              num_keywords=num_keywords)[0]

            coherence_dict[t_n] = get_coherence(model=tm,
                                                text_corpus=text_corpus,
                                                num_topics=t_n,
                                                num_keywords=num_keywords,
                                                measure='c_v')

        if 'stability' in metrics:
            for j in range(0, len(topic_nums_to_compare)-1):
                jaccard_sims = []
                for t1, topic1 in enumerate(topics_dict[topic_nums_to_compare[j]]): # pylint: disable=unused-variable
                    sims = []
                    for t2, topic2 in enumerate(topics_dict[topic_nums_to_compare[j+1]]): # pylint: disable=unused-variable
                        sims.append(jaccard_similarity(topic1, topic2))    
                    
                    jaccard_sims.append(sims)
                
                stability_dict[topic_nums_to_compare[j]] = np.array(jaccard_sims).mean()

            mean_stabilities = [stability_dict[t_n] for t_n in topic_nums_to_compare[:-1]]
            metric_vals += mean_stabilities

            ax = sns.lineplot(x=topic_nums_to_compare[:-1], y=mean_stabilities, label='{}: Average Topic Overlap'.format(m.upper()))
        
        if 'coherence' in metrics:            
            coherences = [coherence_dict[t_n] for t_n in topic_nums_to_compare[:-1]]
            metric_vals += coherences

            ax = sns.lineplot(x=topic_nums_to_compare[:-1], y=coherences, label='{}: Topic Coherence'.format(m.upper()))

        # If both metrics can be calculated, then an optimal number of topics can be derived
        if 'stability' in metrics and 'coherence' in metrics:
            coh_sta_diffs = [coherences[i] - mean_stabilities[i] for i in range(len(topic_nums_to_compare))[:-1]]
            coh_sta_max = max(coh_sta_diffs)
            coh_sta_max_idxs = [i for i, j in enumerate(coh_sta_diffs) if j == coh_sta_max]
            model_ideal_topic_num_index = coh_sta_max_idxs[0] # take lower topic numbers if more than one max
            model_ideal_topic_num = topic_nums_to_compare[model_ideal_topic_num_index]

            plot_model_ideal_topic_num = model_ideal_topic_num
            if plot_model_ideal_topic_num == topic_nums_to_compare[-1]-1:
                # Prevent the line from not appearing on the plot
                plot_model_ideal_topic_num = plot_model_ideal_topic_num - 0.005

            ax.axvline(x=plot_model_ideal_topic_num, 
                      label='{} Ideal Num Topics: {}'.format(m.upper(), model_ideal_topic_num), 
                      color='black')

            ideal_topic_num_dict[m] = (model_ideal_topic_num, coh_sta_max)

    # Set plot limits
    y_max = max(metric_vals) + (0.10 * max(metric_vals))
    ax.set_ylim([0, y_max])
    ax.set_xlim([topic_nums_to_compare[0], topic_nums_to_compare[-1]-1])
    
    ax.axes.set_title('Method Metrics per Number of Topics', fontsize=25)
    ax.set_ylabel('Metric Level', fontsize=20)
    ax.set_xlabel('Number of Topics', fontsize=20)
    plt.legend(fontsize=20, ncol=len(method))

    if save_file == True:
        plt.savefig('topic_number_metrics_{}.png'.format(time.strftime("%Y%m%d-%H%M%S")), bbox_inches='tight', dpi=250)
    elif type(save_file) == str: # a save path has been provided
        if save_file[-4:] == '.zip':
            with zipfile.ZipFile(save_file, mode="a") as zf:
                plt.plot([0, 0])
                buf = io.BytesIO()
                plt.savefig(buf, bbox_inches='tight', dpi=250)
                plt.close()
                zf.writestr(zinfo_or_arcname="topic_number_metrics.png", data=buf.getvalue())
                zf.close()
        else:
            if os.path.exists(save_file):
                plt.savefig(save_file + '/topic_number_metrics.png', bbox_inches='tight', dpi=250)
            else:
                plt.savefig('topic_number_metrics_{}.png'.format(time.strftime("%Y%m%d-%H%M%S")), bbox_inches='tight', dpi=250)

    # Return the ideal model and its topic number, as well as the best LDA topic number for pyLDAvis
    if return_ideal_metrics:
        if 'lda' in method:
            ideal_lda_num_topics = ideal_topic_num_dict['lda'][0]
        else:
            ideal_lda_num_topics = False

        ideal_topic_num_dict = {k: v[0] for k, v in sorted(ideal_topic_num_dict.items(), key=lambda item: item[1][1])[::-1]}
        ideal_model_and_num_topics = next(iter(ideal_topic_num_dict.items()))
        ideal_model, ideal_num_topics = ideal_model_and_num_topics[0], ideal_model_and_num_topics[1]
        
        return ideal_model, ideal_num_topics, ideal_lda_num_topics
    
    else:
        return ax


def gen_word_cloud(text_corpus,
                   input_language=None,
                   ignore_words=None,
                   incl_mc_questions=False,
                   min_freq=2,
                   min_word_len=4,
                   sample_size=1,
                   height=500,
                   save_file=False):
    """
    Generates a word cloud for a group of words

    Parameters
    ----------
        text_corpus : list or list of lists
            The text_corpus that should be plotted

        input_language : str (default=None)
            The spoken language in which the survey was conducted

        incl_mc_questions : bool (default=False)
            Whether to include the multiple choice questions (True) or just the free answer questions
            Note: included so that it can be passed to prepare_survey_data if a path is provided

        ignore_words : str or list (default=None)
            Words that should be removed (such as the name of the publisher)

        min_freq : int (default=2)
            The minimum allowable frequency of a word inside the text corpus

        min_word_len : int (default=4)
            The smallest allowable length of a word

        sample_size : float (default=None: sampling for non-BERT techniques)
            The size of a sample for BERT models

        height : int (default=500)
            The height of the resulting figure
            Note: the width will be the golden ratio times the height

        save_file : bool or str (default=False)
            Whether to save the figure as a png or a path in which to save it

    Returns
    -------
        A word cloud based on the occurences of words in a list without removed words
    """
    text_corpus = _prepare_corpus_path(text_corpus=text_corpus, 
                                       clean_texts=None,
                                       input_language=input_language, 
                                       incl_mc_questions=incl_mc_questions, 
                                       min_freq=min_freq, 
                                       min_word_len=min_word_len, 
                                       sample_size=sample_size)[0]

    display_string = _combine_tokens_to_str(responses=text_corpus, ignore_words=ignore_words)

    width = int(height * ((1 + math.sqrt(5)) / 2)) # width is the height multiplied by the golden ratio
    wordcloud = WordCloud(width=width, height=height, random_state=None, max_font_size=100).generate(display_string)
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')

    if save_file == True:
        plt.savefig('word_cloud_{}.png'.format(time.strftime("%Y%m%d-%H%M%S")), bbox_inches='tight', dpi=200)
    elif type(save_file) == str: # a save path has been provided
        if save_file[-4:] == '.zip':
            with zipfile.ZipFile(save_file, mode="a") as zf:
                plt.plot([0, 0])
                buf = io.BytesIO()
                plt.savefig(buf, bbox_inches='tight', dpi=200)
                plt.close()
                zf.writestr(zinfo_or_arcname="word_cloud.png", data=buf.getvalue())
                zf.close()
        else:
            if os.path.exists(save_file):
                plt.savefig(save_file + '/word_cloud.png', bbox_inches='tight', dpi=200)
            else:
                plt.savefig('word_cloud_{}.png'.format(time.strftime("%Y%m%d-%H%M%S")), bbox_inches='tight', dpi=200)

    plt.show()


def pyLDAvis_topics(method='lda',
                    text_corpus=None, 
                    input_language=None,
                    num_topics=15,
                    incl_mc_questions=False,
                    min_freq=2,
                    min_word_len=4,
                    sample_size=1,
                    save_file=False,
                    display_ipython=False):
    """
    Returns the outputs of an LDA model plotted using pyLDAvis

    Parameters
    ----------
        method : str or list (default=LDA)
            The modelling method or methods to compare

            Option:
                LDA: Latent Dirichlet Allocation
                    - Survey data is classified into a given number of categories
                    - These categories are then used to classify individual entries given the percent they fall into categories

        text_corpus : list, list of lists, or str
            The text corpus over which analysis should be done
            Note 1: generated using prepare_survey_data
            Note 2: if a str is provided, then the data will be loaded from a path

        input_language : str (default=None)
            The spoken language in which the survey was conducted

        num_topics : int (default=15)
            The number of categories for LDA and BERT based approaches

        incl_mc_questions : bool (default=False)
            Whether to include the multiple choice questions (True) or just the free answer questions
            Note: included so that it can be passed to prepare_survey_data if a path is provided

        min_freq : int (default=2)
            The minimum allowable frequency of a word inside the text corpus

        min_word_len : int (default=4)
            The smallest allowable length of a word

        sample_size : float (default=None: sampling for non-BERT techniques)
            The size of a sample for BERT models

        save_file : bool or str (default=False)
            Whether to save the HTML file to the current working directory or a path in which to save it

        display_ipython : bool (default=False)
            Whether iPython's display function should be used if in that working environment

    Returns
    -------
        A visualization of the topics and their main keywords via pyLDAvis
    """
    method = method.lower()
    input_language = input_language.lower()

    if input_language in lem_lang_abbr_dict.keys():
        input_language = lem_lang_abbr_dict[input_language]

    text_corpus, clean_texts = _prepare_corpus_path(text_corpus=text_corpus,
                                                    clean_texts=None,
                                                    input_language=input_language, 
                                                    incl_mc_questions=incl_mc_questions, 
                                                    min_freq=min_freq, 
                                                    min_word_len=min_word_len, 
                                                    sample_size=sample_size)

    tm = TopicModel(num_topics=num_topics, method=method)
    tm.fit(texts=clean_texts, 
           text_corpus=text_corpus, 
           method=method, 
           m_clustering=None)

    def in_ipython():
        """
        Allows for direct display in a Jupyter notebook
        """
        try:
            shell = get_ipython().__class__.__name__
            if shell == 'ZMQInteractiveShell':
                return True   # Jupyter notebook or qtconsole
            elif shell == 'TerminalInteractiveShell':
                return False  # Terminal running IPython
            else:
                return False  # Other type (?)
        except NameError:
            return False      # Probably standard Python interpreter

    vis = pyLDAvis.gensim.prepare(tm.lda_model, tm.bow_corpus, tm.dirichlet_dict)

    if save_file == True:
        pyLDAvis.save_html(vis, 'lda_topics_{}.html'.format(time.strftime("%Y%m%d-%H%M%S")))
    elif type(save_file) == str:
        if save_file[-4:] == '.zip':
            pyLDAvis.save_html(vis, 'lda_topics.html')
            with zipfile.ZipFile(save_file, mode='a') as zf:
                zf.write(filename="lda_topics.html")
                os.remove('lda_topics.html') 
                zf.close()
        else:
            if os.path.exists(save_file):
                pyLDAvis.save_html(vis, save_file + '/lda_topics.html')
            else:
                pyLDAvis.save_html(vis, '/lda_topics_{}.html'.format(time.strftime("%Y%m%d-%H%M%S")))

    else:
        if in_ipython() == True and display_ipython == True:
            pyLDAvis.enable_notebook()
            # Display in an ipython notebook
            display(pyLDAvis.display(vis))
        else:
            # Opens HTML
            pyLDAvis.show(vis)


def translate_output(outputs, input_language, output_language):
    """
    Translates model outputs using https://github.com/ssut/py-googletrans
    """
    translator = Translator()

    if type(outputs[0]) == list:
        translated_outputs = []
        for sub_output in outputs:
            translated_outputs.append([translator.translate(text=o, src=input_language, dest=output_language).text for o in sub_output])

    elif type(outputs[0]) == str: 
        translated_outputs = [translator.translate(text=o, src=input_language, dest=output_language).text for o in outputs]

    return translated_outputs


def _order_by_pos(outputs, output_language):
    """
    Orders a keyword output by the part of speech of the words

    Order is: nouns, adjectives, adverbs and vergs

    Parameters
    ----------
        outputs : list
            The keywords that have been generated

        output_language : str
            The spoken language in which the results should be given

    Returns
    -------
        ordered_outputs : list
            The given keywords ordered by their pos
    """
    if output_language in lem_lang_abbr_dict.keys():
        output_language = lem_lang_abbr_dict[output_language]

    if output_language in lem_lang_abbr_dict.values(): # we can use spacy to detect parts of speech
        nlp = spacy.load(output_language)
        nlp_outputs = [nlp(o)[0] for o in outputs]

        # Those parts of speech to be considered (others go to an 'Other' category)
        pos_order = ['NOUN', 'PROPN', 'ADJ', 'ADV', 'VERB']
        ordered_outputs = [[o for o in nlp_outputs if o.pos_ == p]for p in pos_order]
        flat_ordered_outputs = [str(o) for sub in ordered_outputs for o in sub]

        other = []
        for o in outputs:
            if o not in flat_ordered_outputs:
                other.append(o)
        ordered_outputs.append(other)

        outputs_dict = {}
        for i in range(len(ordered_outputs)):
            if i == 0:
                outputs_dict['Nouns:'] =  ordered_outputs[i]
            if i == 1:
                outputs_dict['Nouns:'] += ordered_outputs[i] # proper nouns put in nouns
            if i == 2:
                outputs_dict['Adjectives:'] =  ordered_outputs[i]
            if i == 3:
                outputs_dict['Adverbs:'] =  ordered_outputs[i]
            if i == 4:
                outputs_dict['Verbs:'] =  ordered_outputs[i]
            if i == 5:
                outputs_dict['Other:'] =  ordered_outputs[i]

        outputs_dict = {k: v for k, v in outputs_dict.items() if v != []} # remove if no entries
        
        return outputs_dict

    else:
        return outputs


def gen_survey_keywords(method='lda_bert',
                        text_corpus=None,
                        clean_texts=None,
                        input_language=None,
                        output_language=None,
                        num_keywords=15,
                        num_topics=15,
                        corpuses_to_compare=None,
                        return_topics=False,
                        incl_mc_questions=False,
                        ignore_words=None,
                        min_freq=2,
                        min_word_len=4,
                        sample_size=1):
    """
    Generates keywords given survey data, metadata, and model parameter inputs

    Parameters
    ----------
        method : str (default=lda_bert)
            The modelling method

            Options:
                frequency: a count of the most frequent words
                TFIDF: Term Frequency Inverse Document Frequency
                    - Allows for words within one survey to be compared to those of another
                    - Gives a better idea of what users specifically want from a given publication
                LDA: Latent Dirichlet Allocation
                    - Survey data is classified into a given number of categories
                    - These categories are then used to classify individual entries given the percent they fall into categories
                BERT: Bidirectional Encoder Representations from Transformers
                    - Words are classified via Google Neural Networks
                    - Word classifications are then used to derive topics
                LDA_BERT: Latent Dirichlet Allocation with BERT embeddigs
                    - The combination of LDA and BERT via an autoencoder

        text_corpus : list, list of lists, or str
            The text corpus over which analysis should be done
            Note 1: generated using prepare_survey_data
            Note 2: if a str is provided, then the data will be loaded from a path

        clean_texts : list
            Text strings that are formatted for cluster models

        input_language : str (default=None)
            The spoken language in which the survey was conducted

        output_language : str (default=None: same as input_language)
            The spoken language in which the results should be given

        num_topics : int (default=15)
            The number of categories for LDA and BERT based approaches

        num_keywords : int (default=15)
            The number of keywords that should be generated

        corpuses_to_compare : list : contains lists (default=None)
            A list of other survey text corpuses that the main corpus should be compared to using TFIDF

        return_topics : bool (default=False)
            Whether to return the topics that are generated by an LDA model

        incl_mc_questions : bool (default=False)
            Whether to include the multiple choice questions (True) or just the free answer questions
            Note: included so that it can be passed to prepare_survey_data if a path is provided

        ignore_words : str or list (default=None)
            Words that should be removed (such as the name of the publisher)

        min_freq : int (default=2)
            The minimum allowable frequency of a word inside the text corpus

        min_word_len : int (default=4)
            The smallest allowable length of a word

        sample_size : float (default=None: sampling for non-BERT techniques)
            The size of a sample for BERT models

    Returns
    -------
        output_keywords : list or list of lists
            - A list of togs that should be used to present the publisher
            - A list of lists where sub_lists are the keywords best assosciated with the data entry
    """
    input_language = input_language.lower()
    method = method.lower()

    valid_methods = ['frequency', 'tfidf', 'lda', 'bert', 'lda_bert']

    assert method in valid_methods, "The value for the 'method' argument is invalid. Please choose one of {}.".format(valid_methods)

    if input_language in lem_lang_abbr_dict.keys():
        input_language = lem_lang_abbr_dict[input_language]

    if output_language == None:
        output_language = input_language
    else:
        output_language = output_language.lower()
        if output_language in lem_lang_abbr_dict.keys():
            output_language = lem_lang_abbr_dict[output_language]

    if ignore_words is not None:
        if type(ignore_words) == str:
            ignore_words = [ignore_words]
    else:
        ignore_words = []

    # Generate text corpus from df or a path
    text_corpus, clean_texts = _prepare_corpus_path(text_corpus=text_corpus,
                                                    clean_texts=clean_texts,
                                                    input_language=input_language, 
                                                    incl_mc_questions=incl_mc_questions, 
                                                    min_freq=min_freq, 
                                                    min_word_len=min_word_len, 
                                                    sample_size=sample_size)

    if method == 'frequency' or method == 'tfidf':
        if method == 'frequency':
            word_counts = Counter(item for sublist in text_corpus for item in sublist)
            sorted_word_counts = {k: v for k, v in sorted(word_counts.items(), key=lambda item: item[1])[::-1]}
            top_word_counts = {k: v for k, v in sorted_word_counts.items() \
                if k in [key for key in sorted_word_counts.keys() if key not in ignore_words][:num_keywords]}

            keywords = list(top_word_counts.keys())

        elif method == 'tfidf': # Term Frequency Inverse Document Frequency
            # Format the other surveys to compare
            if type(corpuses_to_compare) == str:
                try:
                    os.path.exists(corpuses_to_compare) # a path has been provided
                    corpuses_to_compare = prepare_survey_data(data=corpuses_to_compare,
                                                              input_language=input_language,
                                                              incl_mc_questions=incl_mc_questions,
                                                              min_freq=min_freq,
                                                              min_word_len=min_word_len,
                                                              sample_size=sample_size)[0]
                except:
                    pass

            elif type(corpuses_to_compare) == list:
                try:
                    os.path.exists(corpuses_to_compare[0])
                    corpus_paths = [c for c in corpuses_to_compare]
                    for c in corpus_paths:
                        corpuses_to_compare.append(prepare_survey_data(data=c,
                                                                       input_language=input_language,
                                                                       incl_mc_questions=incl_mc_questions,
                                                                       min_freq=min_freq,
                                                                       min_word_len=min_word_len,
                                                                       sample_size=sample_size)[0])
                    
                    corpuses_to_compare = [c for c in corpuses_to_compare if c not in corpus_paths][0]
                
                except:
                    pass

            if type(corpuses_to_compare[0]) == str: # only one corpus to compare
                corpuses_to_compare = [corpuses_to_compare]
            
            # Combine the main corpus and those to compare
            comparative_corpus = [corpuses_to_compare]
            comparative_corpus.insert(0, text_corpus)

            comparative_string_corpus = []
            for c in comparative_corpus:
                combined_tokens = _combine_tokens_to_str(c)
                    
                comparative_string_corpus.append(combined_tokens)
            
            tfidf_vectorizer = TfidfVectorizer(use_idf=True, smooth_idf=True, sublinear_tf=True)
            model =  tfidf_vectorizer.fit_transform(comparative_string_corpus) # pylint: disable=unused-variable
            corpus_scored = tfidf_vectorizer.transform(comparative_string_corpus)
            terms = tfidf_vectorizer.get_feature_names()
            scores = corpus_scored.toarray().flatten().tolist()
            keywords_and_scores = list(zip(terms, scores))

            keywords = [word[0] for word in sorted(keywords_and_scores, key=lambda x: x[1], reverse=True)[:num_keywords]\
                        if word not in ignore_words]
            
            # Check that more words than the number that appear in the text is not given
            frequent_words = gen_survey_keywords(method='frequency',
                                                 text_corpus=text_corpus, 
                                                 input_language=input_language,
                                                 output_language=output_language,
                                                 num_keywords=num_keywords,
                                                 num_topics=num_topics,
                                                 corpuses_to_compare=corpuses_to_compare,
                                                 return_topics=False,
                                                 incl_mc_questions=incl_mc_questions,
                                                 ignore_words=ignore_words,
                                                 min_freq=min_freq,
                                                 min_word_len=min_word_len)

            if len(keywords) > len(frequent_words):
                keywords = keywords[:len(frequent_words)]
    
    elif method == 'lda' or method == 'bert' or method == 'lda_bert':
        # Create and fit a topic model on the data
        bert_model = None
        if method == 'bert' or method == 'lda_bert':
            # Multilingual BERT model trained on the top 100+ Wikipedias for semantic textual similarity
            bert_model = SentenceTransformer('xlm-r-bert-base-nli-stsb-mean-tokens')
        
        tm = TopicModel(num_topics=num_topics, method=method, bert_model=bert_model)
        tm.fit(texts=clean_texts, 
               text_corpus=text_corpus, 
               method=method, 
               m_clustering=None)

        ordered_topic_words, selection_indexes = _order_and_subset_by_coherence(model=tm,
                                                                                num_topics=num_topics,
                                                                                num_keywords=num_keywords)

        if return_topics:
            # Return topics to inspect them
            if output_language != input_language:
                ordered_topic_words = translate_output(outputs=ordered_topic_words, 
                                                        input_language=input_language, 
                                                        output_language=output_language)
            
            return ordered_topic_words
        
        else:
            # Reverse all selection variables so that low level words come from strong topics
            selection_indexes = selection_indexes[::-1]
            ordered_topic_words = ordered_topic_words[::-1]

            flat_ordered_topic_words = [word for topic in ordered_topic_words for word in topic]
            set_ordered_topic_words = list(set(flat_ordered_topic_words))
            set_ordered_topic_words = [t_w for t_w in set_ordered_topic_words if t_w not in ignore_words]
            if len(set_ordered_topic_words) <= num_keywords:
                print('\n')
                print("WARNING: the number of distinct topic words is less than the desired number of keywords.")
                print("All topic words will be returned.")
                keywords = set_ordered_topic_words

            else:
                # Derive keywords from Dirichlet or cluster algorithms
                t_n = 0
                keywords = []
                while len(keywords) < num_keywords:
                    sel_idxs = selection_indexes[t_n]

                    for s_i in sel_idxs:
                        if ordered_topic_words[t_n][s_i] not in keywords and ordered_topic_words[t_n][s_i] not in ignore_words:
                            keywords.append(ordered_topic_words[t_n][s_i])
                        else:
                            sel_idxs.append(sel_idxs[-1] + 1)
                        
                        if len(sel_idxs) >= len(ordered_topic_words[t_n]): 
                            # The indexes are now more than the keywords, so move to the next topic
                            break

                    t_n += 1
                    if t_n == len(ordered_topic_words):
                        # The last topic has been gone through, so return to the first
                        t_n = 0
            
            # Fix for if too many were selected
            keywords = keywords[:num_keywords]

            # As a final check, if there are not enough words, then add non-included most frequent ones in order
            if len(keywords) < num_keywords:
                frequent_words = gen_survey_keywords(method='frequency',
                                                     text_corpus=text_corpus, 
                                                     input_language=input_language,
                                                     output_language=output_language,
                                                     num_keywords=num_keywords,
                                                     num_topics=num_topics,
                                                     corpuses_to_compare=corpuses_to_compare,
                                                     return_topics=False,
                                                     incl_mc_questions=incl_mc_questions,
                                                     ignore_words=ignore_words,
                                                     min_freq=min_freq,
                                                     min_word_len=min_word_len)

                for word in frequent_words:
                    if word not in keywords and len(keywords) < len(frequent_words):
                        keywords.append(word)

    if output_language != input_language:
        translated_keywords = translate_output(outputs=keywords, 
                                                 input_language=input_language, 
                                                 output_language=output_language)

        return translated_keywords

    else:
        return keywords


def prompt_for_ignore_words(ignore_words=None):
    """
    Prompts the user for words that should be ignored in kewword generation
    """
    if ignore_words == None:
        ignore_words = []

    ignore_words = [w.replace("'", "") for w in ignore_words]

    words_added = False # whether to run the models again
    more_words = True
    while more_words != False:
        more_words = input("\nAre there words that should be removed [y/n]? ")
        if more_words == 'y':
            new_words_to_ignore = input("Type or copy word(s) to be removed: ")
            # Remove commas if the user has used them to separate words, as well as apostraphes
            new_words_to_ignore = [char for char in new_words_to_ignore if char != ',' and char != "'"]
            new_words_to_ignore = ''.join([word for word in new_words_to_ignore])
            
            if ' ' in new_words_to_ignore:
                new_words_to_ignore = new_words_to_ignore.split(' ')
            elif type(new_words_to_ignore) == str:
                new_words_to_ignore = [new_words_to_ignore]

            ignore_words += new_words_to_ignore
            words_added = True # we need to run the models again
            more_words = False

        elif more_words == 'n':
            more_words = False

        else:
            print('Invalid input')
    
    return ignore_words, words_added


def gen_analysis_files(method=['lda', 'lda_bert'],
                       text_corpus=None, 
                       clean_texts=None,
                       input_language=None,
                       output_language=None,
                       num_keywords=15,
                       topic_nums_to_compare=None,
                       corpuses_to_compare=None,
                       incl_mc_questions=False,
                       ignore_words=None,
                       min_freq=2,
                       min_word_len=4,
                       sample_size=1,
                       fig_size=(20,10),
                       zip_results=True):
    """
    Generates a .zip file of all analysis elements

    Parameters
    ----------
        Most parameters for the following steady_survey.py functions:
            _prepare_corpus_path
            graph_topic_num_evals
            pyLDAvis_topics
            gen_survey_keywords
            prompt_for_ignore_words
            gen_word_cloud

        zip_results : bool (default=True)
            Whether to zip the results from the analysis

    Returns
    -------
        A .zip file in the current working directory
    """
    def get_varname(p):
        """
        Returns a variables name (for the purpose of converting a df name to that of the zip - if necessary)
        """
        for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
            m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
            if m:
                return m.group(1)

    if os.path.exists(text_corpus):
        dest_name = text_corpus.split('/')[-1].split('.')[0] + '_analysis'
    elif type(text_corpus) == pd.DataFrame:
        dest_name = get_varname(text_corpus) + '_analysis'

    if zip_results:
        dest_name += '.zip'
        if os.path.exists(os.getcwd() + '/' + dest_name):
            os.remove(os.getcwd() + '/' + dest_name)
    else:
        # Create a directory
        dest_name = os.getcwd() + '/'  + dest_name
        os.makedirs(dest_name)
        if os.path.exists(dest_name):
            os.rmdir(dest_name)

    if input_language in lem_lang_abbr_dict.keys():
        input_language = lem_lang_abbr_dict[input_language]

    if output_language == None:
        output_language = input_language
    else:
        output_language = output_language.lower()
        if output_language in lem_lang_abbr_dict.keys():
            output_language = lem_lang_abbr_dict[output_language]

    text_corpus, clean_texts = _prepare_corpus_path(text_corpus=text_corpus, 
                                                    clean_texts=clean_texts,
                                                    input_language=input_language, 
                                                    incl_mc_questions=incl_mc_questions, 
                                                    min_freq=min_freq, 
                                                    min_word_len=min_word_len, 
                                                    sample_size=sample_size)

    # Graph metrics and derive the best model and number of topics from them
    best_method, model_ideal_topic_num, ideal_lda_num_topics = \
        graph_topic_num_evals(method=method,
                              text_corpus=text_corpus,
                              clean_texts=clean_texts, 
                              input_language=input_language,
                              num_keywords=num_keywords,
                              topic_nums_to_compare=topic_nums_to_compare,
                              incl_mc_questions=incl_mc_questions,
                              min_freq=min_freq,
                              min_word_len=min_word_len,
                              sample_size=sample_size,
                              metrics=True,
                              fig_size=fig_size,
                              save_file=dest_name,
                              return_ideal_metrics=True)

    if ideal_lda_num_topics != False:
        # LDA was tested, so also include the pyLDAvis html using its best number of topics
        pyLDAvis_topics(method='lda',
                        text_corpus=text_corpus, 
                        input_language=input_language,
                        num_topics=ideal_lda_num_topics,
                        incl_mc_questions=incl_mc_questions,
                        min_freq=min_freq,
                        min_word_len=min_word_len,
                        sample_size=sample_size,
                        save_file=dest_name,
                        display_ipython=False)

    # Generate most frequent keywords and words based on the best model and topic number
    most_fred_kw = gen_survey_keywords(method='frequency',
                                       text_corpus=text_corpus, 
                                       clean_texts=clean_texts,
                                       input_language=input_language,
                                       output_language=output_language,
                                       num_keywords=num_keywords,
                                       num_topics=model_ideal_topic_num,
                                       corpuses_to_compare=None,
                                       return_topics=False,
                                       incl_mc_questions=incl_mc_questions,
                                       ignore_words=ignore_words,
                                       min_freq=min_freq,
                                       min_word_len=min_word_len,
                                       sample_size=sample_size)

    model_kw = gen_survey_keywords(method=best_method,
                                   text_corpus=text_corpus, 
                                   clean_texts=clean_texts,
                                   input_language=input_language,
                                   output_language=output_language,
                                   num_keywords=num_keywords,
                                   num_topics=model_ideal_topic_num,
                                   corpuses_to_compare=None,
                                   return_topics=False,
                                   incl_mc_questions=incl_mc_questions,
                                   ignore_words=ignore_words,
                                   min_freq=min_freq,
                                   min_word_len=min_word_len,
                                   sample_size=sample_size)

    # Ask user if words should be ignored, and iterate until no more words should be
    more_words_to_ignore = True
    first_iteration = True
    new_words_to_ignore = ignore_words # initialize so that it can be added to
    while more_words_to_ignore != False:
        if first_iteration == True:
            print("The most frequent keywords are:\n")
            print(most_fred_kw)
            print('')
            print("The {} keywords are:\n".format(best_method.upper()))
            print(model_kw)
        else:
            print('\n')
            print("The new most frequent keywords are:\n")
            print(most_fred_kw)
            print('')
            print("The new {} keywords are:\n".format(best_method.upper()))
            print(model_kw)

        new_words_to_ignore, words_added = prompt_for_ignore_words(ignore_words=new_words_to_ignore)
        first_iteration = False

        if words_added == True:
            most_fred_kw = gen_survey_keywords(method='frequency',
                                               text_corpus=text_corpus, 
                                               clean_texts=clean_texts,
                                               input_language=input_language,
                                               output_language=output_language,
                                               num_keywords=num_keywords,
                                               num_topics=model_ideal_topic_num,
                                               corpuses_to_compare=None,
                                               return_topics=False,
                                               incl_mc_questions=incl_mc_questions,
                                               ignore_words=new_words_to_ignore,
                                               min_freq=min_freq,
                                               min_word_len=min_word_len,
                                               sample_size=sample_size)

            model_kw = gen_survey_keywords(method=best_method,
                                           text_corpus=text_corpus, 
                                           clean_texts=clean_texts,
                                           input_language=input_language,
                                           output_language=output_language,
                                           num_keywords=num_keywords,
                                           num_topics=model_ideal_topic_num,
                                           corpuses_to_compare=None,
                                           return_topics=False,
                                           incl_mc_questions=incl_mc_questions,
                                           ignore_words=new_words_to_ignore,
                                           min_freq=min_freq,
                                           min_word_len=min_word_len,
                                           sample_size=sample_size)

        else:
            more_words_to_ignore = False

    # Make a word cloud that doesn't include the words that should be ignored
    gen_word_cloud(text_corpus=text_corpus,
                   input_language=input_language,
                   ignore_words=new_words_to_ignore,
                   min_freq=min_freq,
                   min_word_len=min_word_len,
                   sample_size=sample_size,
                   height=500,
                   save_file=dest_name)

    # Order words by part of speech and format them for a .txt file output
    ordered_most_freq_kw = _order_by_pos(outputs=most_fred_kw, output_language=output_language)
    ordered_model_kw = _order_by_pos(outputs=model_kw, output_language=output_language)

    keywords_dict = {'Most Frequent Keywords': ordered_most_freq_kw, 
                     '{} Keywords'.format(best_method.upper()): ordered_model_kw}

    def add_to_zip_str(input_obj, new_char):
        """
        Adds characters to a string that will be zipped
        """
        input_obj += new_char
        return input_obj

    def add_to_txt_file(input_obj, new_char):
        """
        Adds characters to a string that will be zipped
        """
        input_obj.write(new_char)
        return input_obj

    if zip_results == True:
        edit_fxn = add_to_zip_str
        input_obj = ''

    else:
        edit_fxn = add_to_txt_file
        txt_file = "survey_keywords.txt"
        input_obj = open(txt_file, "w")

    for model_key, model_val in keywords_dict.items():
        if type(keywords_dict[model_key]) == dict:
            input_obj = edit_fxn(input_obj=input_obj, new_char=str(model_key))
            input_obj = edit_fxn(input_obj=input_obj, new_char='\n\n')
            for pos_key in list(model_val.keys()):
                input_obj = edit_fxn(input_obj=input_obj, new_char=str(pos_key))
                input_obj = edit_fxn(input_obj=input_obj, new_char='\n')
                input_obj = edit_fxn(input_obj=input_obj, new_char='-' * len(pos_key))
                input_obj = edit_fxn(input_obj=input_obj, new_char='\n')
                for pos_word in model_val[pos_key]:
                    input_obj = edit_fxn(input_obj=input_obj, new_char=str(pos_word))
                    input_obj = edit_fxn(input_obj=input_obj, new_char='\n')
                input_obj = edit_fxn(input_obj=input_obj, new_char='\n')

            if model_key != list(keywords_dict.keys())[-1]:
                input_obj = edit_fxn(input_obj=input_obj, new_char='=' * len(model_key))
                input_obj = edit_fxn(input_obj=input_obj, new_char='\n\n')

        elif type(keywords_dict[model_key]) == list:
            input_obj = edit_fxn(input_obj=input_obj, new_char=str(model_key))
            input_obj = edit_fxn(input_obj=input_obj, new_char='\n\n')
            for word in keywords_dict[model_key]:
                input_obj = edit_fxn(input_obj=input_obj, new_char=str(word))
                input_obj = edit_fxn(input_obj=input_obj, new_char='\n')
            input_obj = edit_fxn(input_obj=input_obj, new_char='\n')

            if model_key != list(keywords_dict.keys())[-1]:
                input_obj = edit_fxn(input_obj=input_obj, new_char='=' * len(model_key))
                input_obj = edit_fxn(input_obj=input_obj, new_char='\n\n')

    if zip_results == True:                    
        with zipfile.ZipFile(dest_name, mode='a') as zf:
            zf.writestr(zinfo_or_arcname="survey_keywords.txt", data=input_obj)
            zf.close()
            print('\n')
            print('Analysis zip folder created in the local directory.')
    else:
        input_obj.close()
        print('\n')
        print('Analysis folder created in the local directory.')


class Autoencoder:
    """
    Autoencoder for learning latent space representation architecture (simplified for only one hidden layer)

    Note: is used to combine LDA and BERT vectors
    """
    def __init__(self, latent_dim=32, activation='relu', epochs=200, batch_size=128): # increase epochs to run model more iterations
        self.latent_dim = latent_dim
        self.activation = activation
        self.epochs = epochs
        self.batch_size = batch_size
        self.autoencoder = None
        self.encoder = None
        self.decoder = None
        self.his = None

    def _compile(self, input_dim):
        """
        Compile the computational graph
        """
        input_vec = Input(shape=(input_dim,))
        encoded = Dense(units=self.latent_dim, activation=self.activation)(input_vec)
        decoded = Dense(units=input_dim, activation=self.activation)(encoded)
        self.autoencoder = Model(input_vec, decoded)
        self.encoder = Model(input_vec, encoded)
        encoded_input = Input(shape=(self.latent_dim,))
        decoder_layer = self.autoencoder.layers[-1]
        self.decoder = Model(encoded_input, decoder_layer(encoded_input))
        self.autoencoder.compile(optimizer='adam', loss=keras.losses.mean_squared_error)

    def fit(self, X):
        """
        Fit the model
        """
        if not self.autoencoder:
            self._compile(X.shape[1])
        X_train, X_test = train_test_split(X)
        self.his = self.autoencoder.fit(X_train, X_train,
                                        epochs=self.epochs,
                                        batch_size=self.batch_size,
                                        shuffle=True,
                                        validation_data=(X_test, X_test), 
                                        verbose=0)


class TopicModel:
    def __init__(self, num_topics=15, method='lda_bert', bert_model=None):
        """
        Parameters
        ----------
            num_topics : int (default=15)
                The number of categories for LDA and BERT based approaches
                
            method : str (default=lda_bert)
                The modelling method

            bert_model : sentence_transformers.SentenceTransformer.SentenceTransformer
                A sentence transformer model
        """
        modeling_methods = ['lda', 'bert', 'lda_bert']
        if method not in modeling_methods:
            ValueError("The indicated method is invalid. Please choose from {}.".format(modeling_methods))
            
        self.num_topics = num_topics
        self.bert_model = bert_model
        self.dirichlet_dict = None
        self.bow_corpus = None
        self.text_corpus = None
        self.cluster_model = None
        self.lda_model = None
        self.vec = {}
        self.gamma = 15  # parameter for reletive importance of LDA
        self.method = method.lower()
        self.autoencoder = None
        self.id = method + '_' + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    def _vectorize(self, texts, text_corpus, method=None):
        """
        Get vector representations from selected methods
        """
        if method == None:
            method = self.method

        self.text_corpus = text_corpus
        self.dirichlet_dict = corpora.Dictionary(text_corpus)
        self.bow_corpus = [self.dirichlet_dict.doc2bow(text) for text in text_corpus]

        if method == 'lda':
            if not self.lda_model:
                self.lda_model = LdaModel(corpus=self.bow_corpus, 
                                          num_topics=self.num_topics, 
                                          id2word=self.dirichlet_dict,
                                          chunksize=len(self.bow_corpus),
                                          passes=20, # increase to run model more iterations
                                          alpha='auto',
                                          random_state=None)

            def get_vec_lda(model, bow_corpus, num_topics):
                """
                Get the LDA vector representation 

                Returns
                -------
                    vec_lda : np.array (n_doc * n_topic)
                        The probabilistic topic assignments for all documents
                """
                n_doc = len(bow_corpus)
                vec_lda = np.zeros((n_doc, num_topics))
                for i in range(n_doc):
                    # Get the distribution for the i-th document in bow_corpus
                    for topic, prob in model.get_document_topics(bow=bow_corpus[i], minimum_probability=0):
                        vec_lda[i, topic] = prob

                return vec_lda

            vec = get_vec_lda(self.lda_model, self.bow_corpus, self.num_topics)
            
            return vec

        elif method == 'bert':
            model = self.bert_model
            vec = np.array(model.encode(texts, show_progress_bar=False))
            
            return vec

             
        elif method == 'lda_bert':
            vec_lda = self._vectorize(texts=texts, text_corpus=text_corpus, method='lda')
            vec_bert = self._vectorize(texts=texts, text_corpus=text_corpus, method='bert')
            vec_bert = vec_bert[:len(vec_lda)] # Fix if BERT vecctor larger than LDA's
            vec_lda_bert = np.c_[vec_lda * self.gamma, vec_bert]
            self.vec['LDA_BERT_FULL'] = vec_lda_bert
            if not self.autoencoder:
                self.autoencoder = Autoencoder()
                self.autoencoder.fit(vec_lda_bert)
            
            vec = self.autoencoder.encoder.predict(vec_lda_bert)
            
            return vec

        
    def fit(self, texts, text_corpus, method=None, m_clustering=None):
        """
        Fit the topic model for selected method given the preprocessed data

        Returns
        -------
            self : LDA or cluster model
                A fitted model
        """
        if method == None:
            method = self.method

        if m_clustering == None:
            m_clustering = KMeans

        self.text_corpus = text_corpus
        if not self.dirichlet_dict:
            self.dirichlet_dict = corpora.Dictionary(text_corpus)
            self.bow_corpus = [self.dirichlet_dict.doc2bow(text) for text in text_corpus]

        if method == 'lda':
            if not self.lda_model:
                self.lda_model = LdaModel(corpus=self.bow_corpus, 
                                          num_topics=self.num_topics, 
                                          id2word=self.dirichlet_dict,
                                          chunksize=len(self.bow_corpus),
                                          passes=20, # increase to run model more iterations
                                          alpha='auto',
                                          random_state=None)

        else:
            self.cluster_model = m_clustering(self.num_topics)
            self.vec[method] = self._vectorize(texts=texts, 
                                               text_corpus=self.text_corpus, 
                                               method=method)
            self.cluster_model.fit(self.vec[method])
            
        
    def predict(self, texts, text_corpus, out_of_sample=None):
        """
        Predict topics for texts
        """
        out_of_sample = out_of_sample is not None

        if out_of_sample:
            bow_corpus = [self.dirichlet_dict.doc2bow(text) for text in text_corpus]
            if self.method != 'lda':
                vec = self._vectorize(texts, text_corpus)

        else:
            bow_corpus = self.bow_corpus
            vec = self.vec.get(self.method, None)

        if self.method == 'lda':
            lbls = np.array(list(map(lambda x: sorted(self.lda_model.get_document_topics(bow=x, minimum_probability=0),
                                                     key=lambda x: x[1], reverse=True)[0][0],
                                    bow_corpus)))
        else:
            lbls = self.cluster_model.predict(vec)

        return lbls