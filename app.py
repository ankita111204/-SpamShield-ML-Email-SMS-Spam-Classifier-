import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem import PorterStemmer
from PIL import Image

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

ps = PorterStemmer()

image = Image.open('img.png')

st.image(image, caption='EMAIL')

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


# Load models
try:
    tfidf = pickle.load(open('vectorizer1.pkl', 'rb'))
    model = pickle.load(open('model1.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading model files: {e}")
    st.stop()

st.title('Email/SMS Spam Classifier')

input_sms = st.text_input("Enter the Message")

option = st.selectbox("You Got Message From :-", ["Via Email ", "Via SMS", "other"])


if st.checkbox("Check me"):
    st.write("")

if st.button('Classify'):
    # Preprocess
    transformed_sms = transform_text(input_sms)

    # Vectorize
    vector_input = tfidf.transform([transformed_sms])

    # Predict
    try:
        result = model.predict(vector_input)[0]
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        st.stop()
    print(result)
    # Display result
    if result=="spam":
        st.header("Spam Alert! This message will be moved to the SPAM section.")
    else:
        st.header("Not Spam. This message will go to your Inbox.")