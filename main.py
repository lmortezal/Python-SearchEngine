import pandas as pd
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data from CSV file
def load_data(file_path, num_rows=500):
    df = pd.read_csv(file_path, nrows=num_rows)
    return df['article'].tolist()

# Preprocess data (tokenization, stop-word removal, and stemming)
def preprocess_data(data):
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()

    processed_data = []
    for document in data:
        tokens = word_tokenize(document.lower())
        filtered_tokens = [ps.stem(token) for token in tokens if token.isalnum() and token not in stop_words]
        processed_data.append(" ".join(filtered_tokens))

    return processed_data

# Indexing
def create_index(processed_data):
    index = {}
    for i, document in enumerate(processed_data):
        for term in document.split():
            if term not in index:
                index[term] = set()
            index[term].add(i)

    return index

# Boolean Retrieval
def boolean_retrieval(query, index, processed_data):
    query_terms = set(word_tokenize(query.lower()))
    result_set = set(range(len(processed_data)))

    for term in query_terms:
        if term in index:
            result_set = result_set.intersection(index[term])

    return result_set

# Vector-based Retrieval using TF-IDF
def vector_based_retrieval(query, processed_data):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_data)
    query_vector = vectorizer.transform([query])

    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
    return similarity_scores

# Main function
def main():
    file_path = os.path.dirname(os.path.realpath(__file__)) + "/dataset/"
    file_path = file_path + "test.csv"
    num_rows = 500

    # Load data
    data = load_data(file_path, num_rows)

    # Preprocess data
    processed_data = preprocess_data(data)

    # Indexing
    index = create_index(processed_data)

    # User query
    user_query = input("Enter your search query: ")

    # Stemming on the query
    user_query = " ".join([PorterStemmer().stem(word) for word in word_tokenize(user_query.lower())])

    # Boolean Retrieval
    boolean_results = boolean_retrieval(user_query, index, processed_data)

    # Vector-based Retrieval using TF-IDF
    tfidf_scores = vector_based_retrieval(user_query, processed_data)

    # Display results
    print("\nBoolean Retrieval Results:")
    print(boolean_results)

    print("\nTF-IDF Scores:")
    for i, score in enumerate(tfidf_scores):
        print(f"Document {i+1}: {score}")

if __name__ == "__main__":
    main()
