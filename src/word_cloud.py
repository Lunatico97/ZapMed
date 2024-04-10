import nltk ;
from wordcloud import WordCloud ;
from nltk.tokenize import word_tokenize ;
from nltk.corpus import stopwords, wordnet ;
from nltk.stem.wordnet import WordNetLemmatizer ;

def filterText(processedText):
    nltk.download('stopwords') ;
    nltk.download('punkt') ;
    lm = WordNetLemmatizer() ;
    newWords = [] ;
    stopWords = set(stopwords.words('english')) ;
    for text in processedText:
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