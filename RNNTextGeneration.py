from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import Dropout
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.callbacks import ModelCheckpoint
import numpy as np
import sys


class RNNTextGeneration:

    learning_data_root = 'data/learning/'
    models_root = learning_data_root+'models/'

    # Same as in the RNN function, has to be changed afterwards
    filename = learning_data_root+"raw_review.txt"
    raw_text = open(filename, encoding='utf-8').read()
    chars = sorted(list(set(raw_text)))

    # Info to check if we loaded the right file
    n_chars = len(raw_text)
    n_vocab = len(chars)
    print("Total Characters: ", n_chars)
    print("Total Vocab: ", n_vocab)

    int_to_char = dict((i, c) for i, c in enumerate(chars))
    char_to_int = dict((c, i) for i, c in enumerate(chars))

    dropoutRate = 0.4
    hiddenDim = 256

    # load the network weights
    filename = models_root+"weights-improvement-04-2.8221.hdf5"
    model = Sequential()
    model.add(LSTM(hiddenDim, input_shape=(100, 1), return_sequences=True))
    model.add(Dropout(dropoutRate))
    model.add(LSTM(hiddenDim))
    model.add(Dropout(dropoutRate))                 
    model.add(Dense(191, activation='softmax'))
    model.load_weights(filename)
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    # Prediction text pieces
    predictionTextPieces = ["The restaurant is really good for lunch",
                            "The restaurant is great for dinner",
                            "The restaurant takes reservations",
                            "The restaurant has outdoor seating",
                            "Unfortunately, the restaurant is expensive",
                            "The restaurant has alcohol",
                            "The restaurant has table service",
                            "The restaurant's ambience is classy",
                            "The restaurant is good for kids"]

    def append_final_reviews(self, review):
        review_file = open(learning_data_root+"generated_reviews.txt", "a")
        review_file.write(review + "\n")

    def generate_text(self, predictions, threshold, length_of_sequence):
        complete_review = ""
        for i in range(predictions):
            if predictions[i] > threshold:
                predicted_text = self.generate_text_intern(self.predictionTextPieces[i], length_of_sequence)
                complete_review = complete_review + predicted_text
        self.append_final_reviews(complete_review)
        return complete_review
        # Adar maybe a safe function to append the complete review into a text file

    def generate_text_intern(self, sentence, length_of_sequence):
        # Turns the sentence into integer for the model
        pattern = [self.char_to_int[char] for char in sentence]
        for i in range(length_of_sequence):
            x = np.reshape(pattern, (1, len(pattern), 1))
            x = x / float(self.n_vocab)
            prediction = self.model.predict(x, verbose=0)
            index = np.argmax(prediction)
            result = self.int_to_char[index]
            seq_in = [self.int_to_char[value] for value in pattern]
            sys.stdout.write(result)
            pattern.append(index)
            pattern = pattern[1:len(pattern)]
        # Turns the prediction into readable text
        predicted_text = [self.int_to_char[value] for value in pattern]
        return predicted_text

