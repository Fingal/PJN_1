import random
with open('sample_indexes','wb') as file:
    sample_indexes=[random.sample(range(len(answers)),10000) for answers in sorted_answers]
    pickle.dump(sample_indexes,file)