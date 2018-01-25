import csv
import pickle
import time

nouns = {}
with open('noun.exc') as tsvfile:
    reader = csv.DictReader(tsvfile, dialect='excel-tab')
    for row in reader:
        nouns[row["variant"]] = row["root"]

adjs ={}
with open('adj.exc') as tsvfile:
    reader = csv.DictReader(tsvfile, dialect='excel-tab')
    for row in reader:
        adjs[row["variant"]] = row["root"]
advs ={}
with open('adv.exc') as tsvfile:
    reader = csv.DictReader(tsvfile, dialect='excel-tab')
    for row in reader:
        adjs[row["variant"]] = row["root"]
verbs ={}
with open('verb.exc') as tsvfile:
    reader = csv.DictReader(tsvfile, dialect='excel-tab')
    for row in reader:
        verbs[row["variant"]] = row["root"]


with open('nouns.pickle', 'wb') as handle:
    pickle.dump(nouns, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('adjs.pickle', 'wb') as handle:
    pickle.dump(adjs, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('advs.pickle', 'wb') as handle:
    pickle.dump(advs, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('verbs.pickle', 'wb') as handle:
    pickle.dump(verbs, handle, protocol=pickle.HIGHEST_PROTOCOL)


start = time.time()
b = {}
with open('nouns.pickle', 'rb') as handle:
    b = pickle.load(handle)

c = {}
with open('adjs.pickle', 'rb') as handle:
    c = pickle.load(handle)

d = {}
with open('advs.pickle', 'rb') as handle:
    d = pickle.load(handle)

e = {}
with open('verbs.pickle', 'rb') as handle:
    e = pickle.load(handle)


end = time.time()
print(end - start)

