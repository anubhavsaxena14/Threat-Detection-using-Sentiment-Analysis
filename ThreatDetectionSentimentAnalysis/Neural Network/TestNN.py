from pprint import pprint
import  json
import csv


def number_of_threat(review):
    output_json = json.load(open('result.json'))
    count = 0
    for word in review.split():
        for majorkey, subdict in output_json.iteritems():
           if word == majorkey:
               count+=1
    return count


def threat_score(review):
    output_json = json.load(open('result.json'))
    count = 0.0
    for word in review.split():
        for majorkey, subdict in output_json.iteritems():
           if word == majorkey:
               #print(subdict)
                count += float(subdict)
    return count



if __name__ == "__main__":

    with open ('test.txt','w') as f:
        with open("testdata.txt") as file:
            reader = csv.reader(file)
            for row in reader:
                #print(row)
                text = ''.join(row)
                new_text = text.replace(',', '')
                new_text = new_text.replace('.', '')
                new_text = new_text.replace(' .', '')
                #pprint(new_text)
                output_json = json.load(open('output.json'))
                threat_score = 0.0
                number_of_threat = 0
                for word in new_text.split():
                    for majorkey, subdict in output_json.iteritems():
                       if word == majorkey:
                           #print(subdict)
                            threat_score+=float(subdict)
                            number_of_threat+=1
                #pprint(threat_score)
                #pprint(number_of_threat)



                charLength = float(len(text))
                wordLength = float(len(text.split()))
                average = float(charLength/wordLength)
                #pprint('Character Length-> %d'%charLength)
                #pprint('Word Length-> %d'%wordLength)
                system = charLength/544, wordLength/92, average/6, threat_score, number_of_threat
                f.write(str(system)+'\n')




