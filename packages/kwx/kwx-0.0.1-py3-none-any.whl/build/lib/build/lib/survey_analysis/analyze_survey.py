# Requires Python version 3.7

"""
Note on data input:

Due to variable survey questions, the order of the columns must be set before. 
See steady_survey.load_survey_data for column selection.

The English order of the columns must be:
0. User ID #
1. Which of these benefits of membership would be most valuable to you? (Put 'Other' responses in)
2. Which of these benefits of membership would be the least valuable to you? (Put 'Other' responses in)
3. Which of these personal changes through membership would be most valuable to you? (Put 'Other' responses in)
4. Which of these personal changes through membership would be least valuable to you? (Put 'Other' responses in)
5. What would be the one important reason for you to become a member? (most_important)
6. How would you describe our mission in one sentence? (mission_description)
7. What higher purpose do you think we stand for? (higher_purpose)
8. At what price would you describe the membership as expensive but you would still buy it?	
9. At what price would the membership be too expensive so that you would not consider buying it?	
10. At what price would the membership be a bargain, i.e. a great buy for the money?	
11. At what price would the membership be too cheap for you to doubt its quality and not buy it?	
12. How likely are you to become a member at the high price?	
13. How likely are you to become a member at the low price?	
14. How long have you been in contact with this podcast approximately?	
15. Start Date (UTC)	
16. Submit Date (UTC)	
17. Network ID

All other questions may or may not appear in the survey, and should be put at the end. 
These can be loaded with load_survey_data as "extra_col_1" columns with numbers at the end, and then renamed.

clean_and_tokenize_texts, the function after load_survey_data, selects 'most_important', 'mission_description', and 'higher_purpose'
"""

"""
Models:
    frequency : most frequent words
        - Is always ran as a comparison
    tfidf : survey unique keywords 
        - Needs corpuses_to_compare to be paths for surveys in the same language
    lda : topic modeling
    bert : topic modeling with multilingual Google embeddings
    lda_bert : combination of the above two
"""

import os
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning) 
import steady_survey

survey_data_path = os.getcwd() + '/survey_data/' + 'telex.xlsx'
survey_language = 'hungarian' # international two letter abbreviation or full language name (in English)

steady_survey.gen_analysis_files(method=['lda', 'lda_bert'], # frequency, tfidf, lda, bert, lda_bert
                                 text_corpus=survey_data_path, # the path to the xlsx or csv survey data
                                 clean_texts=None,  # the texts as whole strings (for use in recursion)
                                 input_language=survey_language, # survey language
                                 output_language=None, # language to translate into
                                 num_keywords=15, # the number of words to produce
                                 topic_nums_to_compare=None, # a list of integers (default takes 1-num_keywords)
                                 corpuses_to_compare=None, # paths to xlsx or csv data in the same language (for tfidf)
                                 incl_mc_questions=False, # whether the multiple choice questions should be included
                                 ignore_words=None, # which words should automatically be ignored (this is updated via the prompt)
                                 min_freq=2, # the minimum amount of times a word must appear in the responses
                                 min_word_len=4, # the minimum word length
                                 sample_size=0.25, # a percent of the survey data to randomly sample
                                 fig_size=(20,10), # the size of figures desired
                                 zip_results=True) # whether the resulting folder should be zipped