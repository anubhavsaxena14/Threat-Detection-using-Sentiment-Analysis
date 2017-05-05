import numpy as np

def nonlin(x, deriv=False):
    if deriv == True:
        return x*(1-x)
    return 1/(1+np.exp(-x))

def train():

    list_of_lists = []

    with open('inputparameters.txt') as f:
        for line in f:
            for ch in ['(', ')']:
                line = line.replace(ch, '')
            inner_list = [elt.strip() for elt in line.split(',')]
            inner_list2 = list(map(float, inner_list))
            list_of_lists.append(inner_list2)

    list1 = []
    list2 = []
    for i in list_of_lists:
        max1 = len(i)-1
        list1.append(i[:max1])
        list2.append(i[max1:])

    X = np.array(list1)
    Y = np.array(list2)

    np.random.seed(1)


    syn0 = 2*np.random.random((5,6)) - 1
    syn1 = 2*np.random.random((6,1)) - 1

    for i in range(100000):

        l0 = X
        l1 = nonlin(np.dot(l0, syn0))
        l2 = nonlin(np.dot(l1, syn1))

        l2_error = Y - l2

        l2_delta = l2_error * nonlin(l2, deriv=True)

        l1_error = l2_delta.dot(syn1.T)

        l1_delta = l1_error * nonlin(l1, deriv=True)*.5

        syn0 += np.dot(l0.T, l1_delta)
        syn1 += np.dot(l1.T, l2_delta)

    np.set_printoptions(suppress=True)

    return syn0, syn1, l2

def test(syn0, syn1):

   list_of_lists = []

   with open('testinput.txt') as f:
        for line in f:
            for ch in ['(', ')']:
                line = line.replace(ch, '')
            inner_list = [elt.strip() for elt in line.split(',')]
            inner_list2 = list(map(float, inner_list))
            list_of_lists.append(inner_list2)

   X = np.array(list_of_lists)
   l0 = X
   l1 = nonlin(np.dot(l0, syn0))
   l2 = nonlin(np.dot(l1, syn1))
   np.set_printoptions(suppress=True)

   return l2



if __name__ == "__main__":

    syn0, syn1, l2 = train()
    #print("Weights after training SYN0: ", syn0, "\n")
    #print("Weights after training SYN1: ", syn1, "\n")
    #np.set_printoptions(suppress=True)
    #print("Output After Training:\n", l2)
    l1 = test(syn0, syn1)
    print("Output:",l1)
    Y = [[1],[1],[0],[1],[1],[1],[0],[1],[0],[1],[0],[0],[1],[1],[0],[0],[1],[0]] #expected output of the test data
    l = abs(Y - l1)*10
    #print("Error:", l)
    line = 0
    count = 0
    line = len(l)
    print(line)
    for i in l:
        #print(i)
        if(int(i)>0):
            #print(i)
            count+=1

    print(count)
    accuracy = (count*100)/line
    print("Accuracy: ", accuracy)
    
