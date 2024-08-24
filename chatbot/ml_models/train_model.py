from ..models import Chat
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

#fetching data from the chat model
chats=Chat.objects.all().values_list('message', 'sentiment_score')

#convert to dataframe
df=pd.DataFrame(list(chats), columns=['message', 'sentiment_score'])

df['is_positive']=df['sentiment_score']>0

#Vectorization
tfidf=TfidfVectorizer(max_features=1000)
X=tfidf.fit_transform(df['message'])
y=df['is_positive']

#split data
X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.2, random_state=42)

#train model
model=RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

#save model and vectorizer to use in Django views

# joblib.dump(model, 'sentiment_model.pkl')
# joblib.dump(tfidf, 'tfidf_vectorizer.pkl')