__author__ = 'Fingal'
import pickle
from sklearn.qda import QDA
import random
import operator
import sys
import threading
import winsound
from sklearn.svm import SVC
import time

start = time.time()


def important_data(answer):
    return [answer['time_lag'], answer['paragraphs'], answer['words'], answer['codes'], answer['code_lines'],
            answer['reputation'],
            answer['question_words'], answer['question_votes'], answer['question_code_lines'],
            answer['question_paragraphs'], answer['question_codes']]


data = pickle.load(open('all_data', 'rb'))
all_answers = [dict(question=post['question'], **item) for post in data for item in post['answers']]
keys=all_answers[0]['question'].keys()
for i, answer in enumerate(all_answers):
    for key in keys:
        answer['question_' + key] = answer['question'][key]
    del answer['question']
    all_answers[i] = answer
maximum = {i: max(all_answers, key=lambda x:x[i])[i] for i in all_answers[0].keys()}
maximum['votes']=1
all_answers = [{key: answer[key] / maximum[key] for key in
               ['time_lag', 'paragraphs', 'words', 'codes', 'code_lines', 'reputation', 'question_words',
                'question_votes', 'question_code_lines', 'question_paragraphs', 'question_codes','votes']} for answer in
              all_answers]
with open('all_data normalization', 'wb') as file:
    pickle.dump(all_answers,file)
sorted_answers = [list(filter(lambda x: x['votes'] >= 40, all_answers)),
                  list(filter(lambda x: 40 > x['votes'] >= 9, all_answers)),
                  list(filter(lambda x: 9 > x['votes'] >= 3, all_answers)),
                  list(filter(lambda x: 3 > x['votes'] >= 1, all_answers)),
                  list(filter(lambda x: 1 > x['votes'], all_answers))]
lengths = map(len, sorted_answers)
sample_indexes = []
if False:
    with open('sample_indexes', 'wb') as file:
        sample_indexes = [random.sample(range(len(answers)), 10000) for answers in sorted_answers]
        pickle.dump(sample_indexes, file)
with open('sample_indexes', 'rb') as file:
    sample_indexes = pickle.load(file)
l = [[sorted_answers[i][index] for index in indexes] for i, indexes in enumerate(sample_indexes)]
answers = [important_data(item) for tables in l for item in tables]
target = [value for i in range(len(sorted_answers)) for value in [i + 1] * len(sample_indexes[i])]
clf = SVC()
clf.fit(answers, target)
with open('result_norm', 'wb') as file:
    a = [[clf.predict(important_data(answer)) for j, answer in enumerate(answers) if j not in sample_indexes[i]] for
         i, answers in enumerate(sorted_answers)]
    print([[len(list(filter(lambda x: x == i, row))) for i in range(1, 6)] for row in a])
    pickle.dump(a, file)
    print([sum(result) / len(result) for result in a])
    winsound.Beep(442, 1000)
    pickle.dump(clf, open('clf_norm', 'wb'))
    print(time.time() - start, time.time() - start / 60)
    # [[len(list(filter(lambda x: x==i,row))) for i in range(1,6)] for row in a]
