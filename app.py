from DBp1part3 import  create_app
app = create_app()
from nltk.stem import WordNetLemmatizer
if __name__ == '__main__':
    app.run(debug=True)

