from __future__ import print_function
import json

def merge_dicts(*dict_args):

    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

if __name__=="__main__":
    j = json.load(open('result.json'))
    j1 = json.load(open('result1.json'))
    j2 = json.load(open('result2.json'))
    j3 = json.load(open('result3.json'))

    z = merge_dicts(j, j1, j2, j3)
    with open('output.json', 'w') as outfile:
        json.dump(z, outfile)
    #print(z)