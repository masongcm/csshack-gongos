
#%% TKNSE FUNCTION

def tknse(s):
    """
    Tokenises a sentence string in a suitable to way to analyse
    both bible text and twitter data 
    (e.g. catching and filtering out mentions, URLs, ...)
    """
    
    import string
    from nltk import regexp_tokenize
    
    # define pattern for regexp
    pattern = [
    r'<[^>]+>', # HTML tags (drop)
    r'(?:@[\w_]+)', # @-mentions (catch and filter drop)
    #r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags (keep as words)
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs (catch and filter)
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers (drop)
    r'(?:[A-Z]\.)+', # abbreviations, e.g. U.S.A.
    #r'\$?\d+(?:\.\d+)?%?', # currency and percentages, e.g. $12.40, 82% (leave as numbers)
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
    ]
    pattern = r'('+'|'.join(pattern)+')' # collapse into single regex string
    tok = regexp_tokenize(s, pattern) # tokenise
    
    # filter out unwanted tokens 
    tok = list(filter(lambda w: 
        (w[0] not in ['@']) and # @-mentions
        (w[0:4].lower() != 'http') and # URLs
        (w.replace('.','',1).isdigit() == False) and # numbers
        (w not in string.punctuation)
        , tok)) 
    # to lower case
    tok = [w.lower() for w in tok] # lower case only
    return(tok)


#%% PREPROCESS FUNCTION

# This function gets a single line of text entry and returns a single line
# after it has (1) removed stopwords and (2) only used stems of words 
# (can choose either Porter or Snowball stemmer)

def preprocess(sentence,
               language,
               rstems = False, 
               lemmas = False):
    
    # Check arguments
    if isinstance(sentence, str)==False:
        raise ValueError('Argument must be a string scalar')
    
    # load packages
    from nltk.corpus import stopwords
    from nltk.stem import SnowballStemmer
        
    # Step (1): Tokenize
    tokens = tknse(sentence)
    
    # Step (2): Remove stopwords
    filtered_words = list(filter(lambda w: w not in set(stopwords.words(language)), tokens))

    # Step (3): Stem
    normalised_words=[SnowballStemmer(language).stem(word) for word in filtered_words]

    # Return
    if rstems==False: # return string with spaces between words
        return_string=[" ".join(normalised_words)]
    else : # return list of stems/lemmas
        return_string = normalised_words 
    return list(return_string)

