import pandas as pd
import nltk
import swifter
from rake_nltk import Rake
nltk.download('stopwords')
nltk.download('punkt')

FILENAME = ''
INPUT_COLUMN_NAME = ''
OUTPUT_COLUMN_NAME = ''
OUTPUT_FILENAME_CSV='.csv'
OUTPUT_FILENAME_EXCEL='.xlsx'
r = Rake()

def rakeprocessing(text):
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases_with_scores()

if FILENAME.split('.')[-1] == 'csv':
    df=pd.read_csv(FILENAME,engine='python')
elif FILENAME.split('.')[-1] == 'xlsx':
    df=pd.read_csv(FILENAME)
    

df[OUTPUT_COLUMN_NAME] = df[INPUT_COLUMN_NAME].swifter.apply(lambda x:rakeprocessing(x))

df.to_csv(OUTPUT_FILENAME_CSV)

df.to_excel(OUTPUT_FILENAME_EXCEL)








r = Rake()

# Extraction given the text.
r.extract_keywords_from_text(<text to process>)

# Extraction given the list of strings where each string is a sentence.
r.extract_keywords_from_sentences(<list of sentences>)

# To get keyword phrases ranked highest to lowest.
r.get_ranked_phrases()

# To get keyword phrases ranked highest to lowest with scores.
r.get_ranked_phrases_with_scores()