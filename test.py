__author__ = 'Fingal'
import pickle
import pprint
path='pickled/{}'
points_normalised = []
for i in range(500,600):
    result=[]
    a=pickle.load(open(path.format(i),'rb'))
    a['question']['votes']
    for answer in a['answers']:
        result.append([answer['votes'],a['question']['votes'],a['question']['favorites_count']])
    points_normalised.append(result[:4])
pprint.pprint(points_normalised)