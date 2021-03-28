from flask import Flask, request, redirect, render_template
from nltk.corpus import stopwords
import pickle, string

#Read model
count_vectorizer = pickle.load(open('count_vectorizer.pkl', 'rb'))
model = pickle.load(open('nb.pkl', 'rb'))

def clean(text):
    #lower text
    text = text.lower()
    #remove pontctuation
    text = ''.join([letter for letter in text if letter not in string.punctuation])
    #remove stop words
    text = ' '.join([word for word in text.split() if word not in stopwords.words('english')])
    return text

def predict(text):
    text = count_vectorizer.transform([text])
    pred = model.predict_proba(text)

    ham_proba = pred[0][0]
    spam_proba = pred[0][1]

    if spam_proba > ham_proba:
        return 'There is a {:.2%} probability it is a SPAM'.format(spam_proba)
    else:
        return 'There is a {:.2%} probability it is a NOT SPAM'.format(ham_proba)


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('page.html')

@app.route('/prediction', methods=['GET', 'POST'])
def result():
    msg = request.form.get('message')
    msg = clean(msg)
    pred = predict(msg)
    return render_template('page.html', pred=pred)

if __name__ == '__main__':
    app.run()