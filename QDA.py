__author__ = 'Fingal'
import pickle
import random
from sklearn.qda import QDA


def important_data(answer):
    return [answer['time_lag'], answer['paragraphs'], answer['words'], answer['codes'], answer['code_lines'], answer['reputation'],
            answer['question']['words'], answer['question']['votes'], answer['question']['code_lines'],
            answer['question']['paragraphs'], answer['question']['codes']]

data = pickle.load(open('all_data', 'rb'))
all_answers = [dict(question=post['question'], **item) for post in data for item in post['answers']]
sorted_answers = [list(filter(lambda x: x['votes'] > 300, all_answers)),
                  list(filter(lambda x: x['votes'] > 200, all_answers)),
                  list(filter(lambda x: x['votes'] > 150, all_answers)),
                  list(filter(lambda x: x['votes'] > 100, all_answers)),
                  list(filter(lambda x: x['votes'] > 75, all_answers)),
                  list(filter(lambda x: x['votes'] > 50, all_answers)),
                  list(filter(lambda x: x['votes'] > 25, all_answers)),
                  list(filter(lambda x: x['votes'] > 0, all_answers)),
                  list(filter(lambda x: x['votes'] < 0, all_answers)), ]
lengths = map(len, sorted_answers)
sample_indexes = []
with open('sample_indexes', 'rb') as file:
    sample_indexes = pickle.load(file)
l = [[sorted_answers[i][index] for index in indexes] for i, indexes in enumerate(sample_indexes)]
answers = [[item['time_lag'], item['paragraphs'], item['words'], item['codes'], item['code_lines'], item['reputation'],
            item['question']['words'], item['question']['votes'], item['question']['code_lines'],
            item['question']['paragraphs'], item['question']['codes']] for tables in l for item in tables]
Y=[value for i in range(len(sorted_answers)) for value in [i+1] * 1000 ]
clf = QDA()
clf.fit(answers,Y)
clf.predict(important_data(sorted_answers[0][20]))