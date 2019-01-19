from rake_nltk import Rake

r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.

r.extract_keywords_from_text("Worked on a Document Matching problem, leveraging NLP and Deep Learning, Trained and optimized Machine Learning models to solve a sentence classification problem, aimed at performing better document matching. Performed feature engineering and regular tests in the end to end pipeline to optimize accuracy, Worked on data sourcing alongwith tokenizing and cleaning the same using various techniques such as stopword removal, morphy and lemmatizing, Skills learnt: Python for Machine Learning, Scikit-learn, Keras, Gensim, and NLP techniques such as TF-IDF and Word2vec")

phs = r.get_ranked_phrases_with_scores() # To get keyword phrases ranked highest to lowest.
for ph in phs:
    print(ph)
