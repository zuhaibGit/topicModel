import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim import corpora, models
import gensim
import string
import pyLDAvis.gensim
import re


def parseXml(xmlFile):
    """
    The passed xml file consists of 114 chapters.
    Each chapter consists of a number of verses.
    The function does the following:
        - Parse xml file into element tree
        - Go through each element
        - Extract and join each verses's text
        - Assign the joined text to "doc"
        - Remove any instances of "\n" and "\t"
        - Return a list of documents
    Each docment contains the full text of a chapter.

    To re-map a doc to a chapter, use (index of doc + 1)
    as the id. Example: the first chapter has a Chapter
    id of 1 in the xml file and an index of 0 in the "docs"
    list of documents.
    """
    tree = ET.parse(xmlFile)
    root = tree.getroot()

    docs = []
    for child in root:
	    doc = "".join(child.itertext())
	    doc = doc.replace("\n", "")
	    doc = doc.replace("\t", "")
	    doc = doc.replace(".", ". ")

	    docs.append(doc)
    return(docs)


def clean(docs):
    """
    To clean the documents:
        - Tokenize each document
        - Remove stop words from each document
        - Remove punctuation
    """
    stop = set(stopwords.words('english')) #stop words
    punc = set(string.punctuation)
    moreStop = ["allah", "ye", "shall", "lord", "thee", "thy", "thou", "say", "said", "us", "indeed", "may", "hath"]
    for word in moreStop:
        stop.add(word) #add more stop words

    # https://stackoverflow.com/questions/4328500/how-can-i-strip-all-punctuation-from-a-string-in-javascript-using-regex
    regex = re.compile('[%s]' % re.escape("!\"#$%&()*+,-./:;<=>?@[\]^_`{|}~"))

    cleanDocs = []
    for doc in docs:
        cleanDoc = doc.lower()  # convert to lower
        cleanDoc = regex.sub('', cleanDoc) #remove punctuation
        cleanDoc = ''.join(i for i in cleanDoc if not i.isdigit()) #remove remove any digit
        cleanDoc = cleanDoc.split() #split into list
        cleanDoc = [word for word in cleanDoc if word not in stop]
        cleanDoc = [word for word in cleanDoc if word not in punc]
        cleanDocs.append(cleanDoc)

    return(cleanDocs)


"""def applyLDA(cleanDocs):
    
    Apply the model to the data:
        - Construct doc-term matrix
        - Convert dictionary into bag-of-words
        - Apply the LDA model
    
    dictionary = corpora.Dictionary(cleanDocs)
    corpus = [dictionary.doc2bow(doc) for doc in cleanDocs]
    model = gensim.models.ldamodel.LdaModel(corpus, num_topics = 15, id2word = dictionary, passes = 30)

    return(model)
"""

xmlFile = "English-Yusuf-Ali.xml"
docs = parseXml(xmlFile)
cleanDocs = clean(docs)
#model = applyLDA(cleanDocs)
dictionary = corpora.Dictionary(cleanDocs)
corpus = [dictionary.doc2bow(doc) for doc in cleanDocs]
model = gensim.models.ldamodel.LdaModel(corpus, num_topics=15, id2word=dictionary, passes=30)

topics = model.print_topics(num_topics = 15, num_words = 8)
for topic in topics:
    print(topic)
pyLDAvis.gensim.prepare(model, corpus, dictionary)