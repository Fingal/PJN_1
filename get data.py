__author__ = 'Fingal'
import pickle
import datetime
import text

path = 'pickled/{}'
data = []
size=0
comunnity = 0
for i in range(0, 12000):
    try:
        post = {}
        loaded = pickle.load(open(path.format(i), 'rb'))
        post['question'] = {}
        post['question']['votes'] = loaded['question']['votes']
        post['question']['votes'] = loaded['question']['votes']
        post['question']['time'] = loaded['question']['time']
        post['question']['favorites'] = loaded['question']['favorites_count']
        post['question'].update(text.text_counter(loaded['question']['text']))
        post['answers'] = [dict(votes=answer['votes'], reputation=answer['user'].get('reputation', 0),
                                 time_lag=int((answer.get('time', datetime.datetime(1, 1, 1)) - loaded['question'].get(
                                     'time', datetime.datetime(1, 1, 1))).total_seconds() / 60),
                           **text.text_counter(answer['text'])) for answer in loaded['answers'] if answer.get('user', False)]
        size+=len(post['answers'])
        data.append(post)
    except Exception as e:
        comunnity += 1
with open('all_data',mode='wb') as file:
    pickle.dump(data,file)
print(comunnity,size)
