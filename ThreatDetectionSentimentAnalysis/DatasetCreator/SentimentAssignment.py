

from __future__ import print_function
import json

if __name__=="__main__":

    pos = {}
    f = file("Threat.yml").read()
    for word in f.split():
        print('%s'%word)
        pos[word] = raw_input('Enter the threat level:')

    #print(pos)
    print(json.dumps(pos))

    with open('result.json', 'w') as fp:
       json.dump(pos, fp)



    count = 0
    output_json = json.load(open('result.json'))

    for majorkey, subdict in output_json.iteritems():
        #print(majorkey, subdict)
        count+= float(subdict)

    print(count)

