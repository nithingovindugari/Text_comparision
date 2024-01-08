from flask import Flask, render_template, request
import re
from collections import Counter

# Initialize the Flask application
app = Flask(__name__)

# Function to preprocess text by removing punctuation and converting it to lowercase
def preprocess_text(text):
    # Regular expression to replace non-word characters with a space and convert to lowercase
    text = re.sub(r'\W+', ' ', text).lower()
    return text

# Function to calculate word frequencies in a text
def word_frequencies(text):
    # Splitting the text into words and counting the frequency of each word
    words = text.split()
    return Counter(words)

# Function to calculate similarity between two texts
def calculate_similarity(text1, text2):
    # Preprocessing both texts
    text1 = preprocess_text(text1)
    text2 = preprocess_text(text2)

    # Calculating word frequencies for both texts
    freq1 = word_frequencies(text1)
    freq2 = word_frequencies(text2)

    # Creating sets of unique words from both texts
    unique_words1 = set(freq1)
    unique_words2 = set(freq2)

    # Finding the intersection (common words) between the two sets
    intersection = unique_words1.intersection(unique_words2)
    # Determining the size of the smaller set of words
    smaller_set_size = min(len(unique_words1), len(unique_words2))

    # Handling edge case: if either text has no words, return a similarity of 0
    if smaller_set_size == 0:
        return 0
    # Calculating similarity as the ratio of intersection to the size of the smaller set
    similarity = len(intersection) / smaller_set_size
    return similarity

# Route for handling both GET and POST requests on the root URL
@app.route('/', methods=['GET', 'POST'])
def home():
    # Initialize variables to store texts and similarity score
    similarity_score = None
    text1 = ""
    text2 = ""

    # Handling POST request: when the form is submitted
    if request.method == 'POST':
        # Retrieving texts from the form fields
        text1 = request.form['text1']
        text2 = request.form['text2']
        # Calculating similarity score
        similarity_score = calculate_similarity(text1, text2)

    # Rendering HTML template, passing texts and similarity score to the template
    return render_template('form.html', text1=text1, text2=text2, similarity_score=similarity_score)

# Running the Flask app
if __name__ == '__main__':
    # Setting the debug mode to True for development and specifying the port to run the app
    app.run(debug=True, port=5001)
