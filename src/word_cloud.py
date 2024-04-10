import nltk ;
from wordcloud import WordCloud ;
from nltk.tokenize import word_tokenize ;
from nltk.corpus import stopwords, wordnet ;
from nltk.stem.wordnet import WordNetLemmatizer ;

def filterText(text):
    nltk.download('stopwords') ;
    nltk.download('punkt') ;
    nltk.download('wordnet') ;
    lm = WordNetLemmatizer() ;
    newWords = [] ;
    stopWords = set(stopwords.words('english')) ;
    words = word_tokenize(text) ;
    for i in words:
      i = i.lower() ;
      if i not in stopWords:
          i = lm.lemmatize(i) ;
          newWords.append(i) ;                       
    processedText = ' '.join(newWords) ;
    return processedText ;

def generateWordCloud(processedText):
    wc = WordCloud(background_color='black', max_words=30) ;         
    wc.generate(processedText) ;
    return wc ;