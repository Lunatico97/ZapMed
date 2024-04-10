import nltk ;
from nltk.translate.bleu_score import corpus_bleu ; 
from nltk.corpus import stopwords ;
from collections import Counter ;

def generateBLEU(corpus, summary):
    # Split corpus into sentences
    references = corpus.split(".") ; 
    candidates = summary.split(".") ;
    bleu_score = corpus_bleu(references, candidates) ;
    return bleu_score ;

def lexicalRedundancy(corpus, summary):
    corpus_tokens = nltk.word_tokenize(corpus.lower()) ;
    summary_tokens = nltk.word_tokenize(summary.lower()) ;
    # Remove stop words
    stop_words = set(stopwords.words("english")) ;
    corpus_tokens_filtered = [token for token in corpus_tokens if token not in stop_words] ;
    summary_tokens_filtered = [token for token in summary_tokens if token not in stop_words] ;
    # Count word frequencies
    corpus_word_counts = Counter(corpus_tokens_filtered) ;
    summary_word_counts = Counter(summary_tokens_filtered) ;
    # Calculate lexical redundancy
    redundant_words = [word for word, count in summary_word_counts.items() if count / len(summary_tokens_filtered) > 0.15] ;
    return redundant_words ;