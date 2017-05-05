from pprint import pprint
import  json
import csv
import numpy as np
from pprint import pprint
import nltk
import yaml
import sys
import os
import re

class Splitter(object):

    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, text):
        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        return tokenized_sentences


class POSTagger(object):

    def __init__(self):
        pass

    def pos_tag(self, sentences):
        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        #adapt format
        pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
        return pos

class DictionaryTagger(object):

    def __init__(self, dictionary_paths):
        files = [open(path, 'r') for path in dictionary_paths]
        dictionaries = [yaml.load(dict_file) for dict_file in files]
        map(lambda x: x.close(), files)
        self.dictionary = {}
        self.max_key_size = 0
        for curr_dict in dictionaries:
            for key in curr_dict:
                if key in self.dictionary:
                    self.dictionary[key].extend(curr_dict[key])
                else:
                    self.dictionary[key] = curr_dict[key]
                    self.max_key_size = max(self.max_key_size, len(key))

    def tag(self, postagged_sentences):
        return [self.tag_sentence(sentence) for sentence in postagged_sentences]

    def tag_sentence(self, sentence, tag_with_lemmas=False):
        tag_sentence = []
        N = len(sentence)
        if self.max_key_size == 0:
            self.max_key_size = N
        i = 0
        while (i < N):
            j = min(i + self.max_key_size, N) #avoid overflow
            tagged = False
            while (j > i):
                expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
                expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
                if tag_with_lemmas:
                    literal = expression_lemma
                else:
                    literal = expression_form
                if literal in self.dictionary:
                    #self.logger.debug("found: %s" % literal)
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                    taggings = [tag for tag in self.dictionary[literal]]
                    tagged_expression = (expression_form, expression_lemma, taggings)
                    if is_single_token: #if the tagged literal is a single token, conserve its previous taggings:
                        original_token_tagging = sentence[original_position][2]
                        tagged_expression[2].extend(original_token_tagging)
                    tag_sentence.append(tagged_expression)
                    tagged = True
                else:
                    j = j - 1
            if not tagged:
                tag_sentence.append(sentence[i])
                i += 1
        return tag_sentence

def value_of(sentiment):
    if sentiment == 'positive': return -1
    if sentiment == 'negative': return 1
    return 0

def value_of_threat(sentiment):
    if sentiment == 'positive': return -1
    if sentiment == 'negative': return 1
    if sentiment == 'threat': return 1
    return 0

def sentence_score(sentence_tokens, previous_token, acum_score):
    if not sentence_tokens:
        return acum_score
    else:
        current_token = sentence_tokens[0]
        tags = current_token[2]
        token_score = sum([value_of(tag) for tag in tags])
        if previous_token is not None:
            previous_tags = previous_token[2]
            if 'inc' in previous_tags:
                token_score *= 2.0
            elif 'dec' in previous_tags:
                token_score /= 2.0
            elif 'inv' in previous_tags:
                token_score *= -1.0
        return sentence_score(sentence_tokens[1:], current_token, acum_score + token_score)

def threatening_score(sentence_tokens, previous_token, acum_score):
    if not sentence_tokens:
        return acum_score
    else:
        current_token = sentence_tokens[0]
        tags = current_token[2]
        token_score = sum([value_of_threat(tag) for tag in tags])
        if previous_token is not None:
            previous_tags = previous_token[2]
            if 'inc' in previous_tags:
                token_score *= 2.0
            elif 'dec' in previous_tags:
                token_score /= 2.0
            elif 'inv' in previous_tags:
                token_score *= -1.0
        return threatening_score(sentence_tokens[1:], current_token, acum_score + token_score)

def threat_score(review):
    return sum([threatening_score(sentence, None, 0.0) for sentence in review])
def sentiment_score(review):
    return sum([sentence_score(sentence, None, 0.0) for sentence in review])


class BigramTrigram(object):

    """
    This method searches each biagram and trigram in dictionaries and calculate threat score
    :return: ThreatCount, PositiveCount, NegativeCount
    """
    def countThreat(self, sentence):
        dictTag = ['Dicts/threatWords.yml', 'Dicts/Positive.yml', 'Dicts/Decreasing.yml', 'Dicts/Inverting.yml']
        files = [open(path, 'r') for path in dictTag]
        dictionaries = [yaml.load(dict_file) for dict_file in files]

        tokens = nltk.word_tokenize(sentence)
        #print(tokens)
        bigrams = [" ".join(pair) for pair in nltk.bigrams(tokens)]
        #print(bigrams)
        trigrams = [" ".join(trio) for trio in nltk.trigrams(tokens)]
        #print(trigrams)

        bigramThreatCount = 0
        bigramPositiveCount = 0
        bigramNegativeCount = 0

        trioThreatCount = 0
        trioPositiveCount = 0
        trioNegativeCount = 0

        for bigram in bigrams:
            for dictionary in dictionaries:
                if bigram in dictionary and dictionary[bigram] == ['threat']:
                    bigramThreatCount += 1
                if bigram in dictionary and dictionary[bigram] == ['positive']:
                    bigramPositiveCount += 1
                if bigram in dictionary and dictionary[bigram] == ['negative']:
                    bigramNegativeCount += 1

        for trigram in trigrams:
            for dictionary in dictionaries:
                if trigram in dictionary and dictionary[trigram] == ['threat']:
                    trioThreatCount += 1
                if trigram in dictionary and dictionary[trigram] == ['positive']:
                    trioPositiveCount += 1
                if trigram in dictionary and dictionary[trigram] == ['negative']:
                    trioNegativeCount += 1

        threatCount = bigramThreatCount + trioThreatCount
        positiveCount = bigramPositiveCount + trioPositiveCount
        negativeCount =  bigramNegativeCount + trioNegativeCount
        return threatCount, positiveCount, negativeCount




if __name__ == "__main__":

    with open ('inputparams.txt','w') as f: #create new file for writing input parameters
        with open("Input.txt") as file: #read input file
            reader = csv.reader(file)
            for row in reader:
                #print(row)
                text = ''.join(row)
                new_text = text.replace(',', '')
                new_text = new_text.replace('.', '')
                #pprint(new_text)
                output_json = json.load(open('threat.json')) #read the threat.json file
                threat_scores = 0.0
                number_of_threat = 0
                for word in new_text.split(): #check if word is in threat.json file
                    for majorkey, subdict in output_json.iteritems():
                       if word == majorkey:
                           #print(subdict)
                            threat_scores+=float(subdict)
                            number_of_threat+=1
                #pprint(threat_score)
                #pprint(number_of_threat)

                if threat_scores >= 0.8: #assign expected output value of the input sentences
                    output = 1
                else:
                    output = 0
                charLength = float(len(text))
                wordLength = float(len(text.split()))
                averages = float(charLength/wordLength)
                #pprint('Character Length-> %d'%charLength)
                #pprint('Word Length-> %d'%wordLength)

                """ Tag the words as threat and calulate threat score"""
                splitter = Splitter()
                postagger = POSTagger()
                bigramtagger = BigramTrigram()

                dicttagger = DictionaryTagger([ 'Dicts/threatWords.yml','Dicts/Positive.yml', 'Dicts/Negative.yml',
                                                'Dicts/Increasing.yml', 'Dicts/Decreasing.yml', 'Dicts/Inverting.yml'])


                splitted_sentences = splitter.split(text)

                pos_tagged_sentences = postagger.pos_tag(splitted_sentences)

                dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)

                #print("analyzing sentiment...")
                sentimentscore = sentiment_score(dict_tagged_sentences)

                dicttagger1 = DictionaryTagger([ 'Dicts/threatWords.yml','Dicts/Positive.yml', 'Dicts/Negative.yml',
                                                'Dicts/Increasing.yml', 'Dicts/Decreasing.yml', 'Dicts/Inverting.yml'])

                splitted_sentences1 = splitter.split(text)

                pos_tagged_sentences1 = postagger.pos_tag(splitted_sentences1)

                dict_tagged_sentences1 = dicttagger1.tag(pos_tagged_sentences1)

                threatCounts = bigramtagger.countThreat(text)
                #return: threat, positive, negative

                #print("threat tuple    ",threatCounts)
                #print("analyzing sentiment...")



                #print("analyzing threat...")
                threatscore = threat_score(dict_tagged_sentences1)

                finalScore = threatscore+threatCounts[2]+threatCounts[0]-threatCounts[1]
                #print(finalScore)

                average = number_of_threat/wordLength
                #print(threatscore)
                """form the input parameters for the NN"""
                system = sentimentscore, averages , finalScore, number_of_threat, average, output
                #write the value system in the file
                f.write(str(system)+'\n')




