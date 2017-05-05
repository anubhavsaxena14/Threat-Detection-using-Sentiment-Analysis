import nltk
import yaml

dictTag = ['Dicts/threatWords.yml', 'Dicts/Positive.yml', 'Dicts/Decreasing.yml', 'Dicts/Inverting.yml']

sentence = "i will kill you and will blow up your house in despair in prospect in store good boy in the cards"

files = [open(path, 'r') for path in dictTag]
dicts = [yaml.load(dict_file) for dict_file in files]
# with open('Dicts/threatWords.yml', 'r') as f:
#     doc = yaml.load(f)

tokens = nltk.word_tokenize(sentence)
print(tokens)

bigrams = [" ".join(pair) for pair in nltk.bigrams(tokens)]
print(bigrams)

trigrams = [" ".join(trio) for trio in nltk.trigrams(tokens)]
print(trigrams)

bigramThreatCount = 0
bigramPositiveCount = 0
bigramNegativeCount = 0

trioThreatCount = 0
trioPositiveCount = 0
trioNegativeCount = 0

for bigram in bigrams:
    for dicto in dicts:
        if bigram in dicto and dicto[bigram] == ['threat']:
            bigramThreatCount += 1
        if bigram in dicto and dicto[bigram] == ['positive']:
            bigramPositiveCount += 1
        if bigram in dicto and dicto[bigram] == ['negative']:
            bigramNegativeCount += 1

for trigram in trigrams:
    for dicto in dicts:
        if trigram in dicto and dicto[trigram] == ['threat']:
            trioThreatCount += 1
        if trigram in dicto and dicto[trigram] == ['positive']:
            trioPositiveCount += 1
        if trigram in dicto and dicto[trigram] == ['negative']:
            trioNegativeCount += 1

print("ThreatCount ", bigramThreatCount + trioThreatCount)
print("PositiveCount ", bigramPositiveCount + trioPositiveCount)
print("NegativeCount ", bigramNegativeCount + trioNegativeCount)

print('done')