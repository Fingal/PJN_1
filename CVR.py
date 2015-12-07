__author__ = 'Fingal'
import pickle
import random
import winsound
from sklearn.svm import SVR
import time
start = time.time()
def important_data(answer):
    return [answer['time_lag'], answer['paragraphs'], answer['words'], answer['codes'], answer['code_lines'],
            answer['reputation'],
            answer['question']['words'], answer['question']['votes'], answer['question']['code_lines'],
            answer['question']['paragraphs'], answer['question']['codes']]


data = pickle.load(open('all_data', 'rb'))
all_answers = [dict(question=post['question'], **item) for post in data for item in post['answers']]
sorted_answers = [list(filter(lambda x: x['votes'] >= 40, all_answers)),
                  list(filter(lambda x: 40 > x['votes'] >= 9, all_answers)),
                  list(filter(lambda x: 9 > x['votes'] >= 3, all_answers)),
                  list(filter(lambda x: 3 > x['votes'] >= 1, all_answers)),
                  list(filter(lambda x: 1 > x['votes'], all_answers))]
lengths = map(len, sorted_answers)
sample_indexes = []
if False:
    with open('sample_indexes_CVR','wb') as file:
        sample_indexes=random.sample(range(len(all_answers)),50000)
        pickle.dump(sample_indexes,file)
with open('sample_indexes_CVR', 'rb') as file:
    sample_indexes = pickle.load(file)
l = [all_answers[index] for index in sample_indexes]
answers = [[item['time_lag'], item['paragraphs'], item['words'], item['codes'], item['code_lines'], item['reputation'],
            item['question']['words'], item['question']['votes'], item['question']['code_lines'],
            item['question']['paragraphs'], item['question']['codes']] for item in l]
target = [item['votes'] for item in l]
clf = SVR()
clf.fit(answers, target)
with open('result_CVR','wb') as file:

    a=[(clf.predict(important_data(answer)),answer['votes']) for i,answer in enumerate(all_answers) if i not in sample_indexes]
    pickle.dump(a,file)
    winsound.Beep(442,1000)
    pickle.dump(clf,open('clf_CVR','wb'))
    print(time.time()-start,time.time()-start/60)
#[[len(list(filter(lambda x: x==i,row))) for i in range(1,6)] for row in a]__author__ = 'Fingal'
