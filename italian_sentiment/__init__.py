import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import spacy
import numpy as np
from keras.layers import Bidirectional, Dense, Embedding, Input, LSTM, Dropout, Conv1D, AveragePooling1D, Flatten
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model
from keras import backend as K
import pickle
from .utility_parse import translate_emoji

class SentimentAnalyzer:
    def __init__(self, dictionary_file='dictionary.pkl', model_weights_file='model_lstm.h5'):
        self.SEQUENCE_LENGTH_LIMIT = 35
        self.EMBEDDING_DIM = 300
        self.MAX_NB_WORDS = 200000
        self.NB_WEMBS = self.MAX_NB_WORDS
        dictionary_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', dictionary_file)
        self.load_word_embeddings(dictionary_file_path)
        self.nlp = spacy.load('it_core_news_sm')
        model_weights_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', model_weights_file)
        if not os.path.exists(model_weights_path):
            raise FileNotFoundError(f"File '{model_weights_file}' not found.")
        self.model = self.create_model()
        self.model.load_weights(model_weights_path)

    def load_word_embeddings(self, dictionary_file):
        if not os.path.exists(dictionary_file):
            raise FileNotFoundError(f"File '{dictionary_file}' not found.")
        with open(dictionary_file, 'rb') as f:
            self.word_embeddings = pickle.load(f)

    def preprocess_text(self, text):
        translated_text = translate_emoji(text)
        doc = self.nlp(translated_text.lower())
        wemb_idxs = [self.get_word_embedding_index(token.text.lower()) for token in doc]
        wemb_idxs = pad_sequences([wemb_idxs], maxlen=self.SEQUENCE_LENGTH_LIMIT, value=self.NB_WEMBS)
        return wemb_idxs

    def get_word_embedding_index(self, word):
        return self.word_embeddings.get(word, self.word_embeddings['unknown'])

    def create_model(self):
        input_text = Input(shape=(self.SEQUENCE_LENGTH_LIMIT,))
        embedded_text = Embedding(self.NB_WEMBS + 1, self.EMBEDDING_DIM, input_length=self.SEQUENCE_LENGTH_LIMIT,
                                  trainable=False)(input_text)
        embedded_text = Dropout(0.5)(Dense(64, activation='relu')(embedded_text))
        conv_layer = Conv1D(filters=32, kernel_size=2, padding='valid', activation='relu')(embedded_text)
        lstm_layer = Bidirectional(LSTM(32, return_sequences=True, recurrent_dropout=0.5), merge_mode='concat')(conv_layer)
        lstm_layer = AveragePooling1D(pool_size=2, strides=None, padding='valid')(lstm_layer)
        lstm_layer = Bidirectional(LSTM(16, return_sequences=True, recurrent_dropout=0.5), merge_mode='concat')(lstm_layer)
        lstm_layer = AveragePooling1D(pool_size=2, strides=None, padding='valid')(lstm_layer)
        flattened_output = Flatten()(lstm_layer)
        predictions = Dense(2, activation='sigmoid')(flattened_output)
        model = Model(inputs=[input_text], outputs=predictions)
        model.compile(loss='binary_crossentropy', optimizer='nadam', metrics=['accuracy'])
        return model

    def predict_sentiment(self, sentences):
        results = []
        for sentence in sentences:
            processed_text = self.preprocess_text(sentence)
            preds = self.model.predict([processed_text], verbose=0)
            K.clear_session()
            sentiment = 'positive' if preds[0][0] > preds[0][1] else 'negative'
            result = {
                'original_text': sentence,
                'sentiment': sentiment,
                'pos': preds[0][0],
                'neg': preds[0][1]
            }
            results.append(result)
        return results

