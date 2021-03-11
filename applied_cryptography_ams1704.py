# Applied Cryptography Project 1: Andrea
"""
def extract_exact_n_gram(text, n):
    # (text, n) -> dictionary of all n-grams and locations
    gram_list =  text.split # no strip no punct
    n_gram_dic = {}
    location = 0
    for i in range(len(gram_list) - (n-1)):
        n_gram_dic[gram_list[i]] = location # add word at index to dict
        location += len(gram_list[i]) # finds location of next n_gram
    return n_gram_dic

def extract_heuristic_n_gram(n, ciphertext, plaintext):
    R = len(ciphertext) - len(plaintext)
    # distance of n-grams is the length of n-gram
    
    NOT SURE WHY I'D DO IT OVER IF WE HAVE EXACT NGRAM

def extract_heuristic_n_gram(n_gram_dict, ciphertext, plaintext):
    # (n_gram_dict, ciphertext, plaintext) -> updated n_gram_dict
    # update key with space and add one to distance
    R = 0
    expected_R = len(ciphertext) - len(plaintext)
    for key, value in n_gram_dict:
        new_key = key.append(" ") # add space
        new_value = value + 1 # add one to value
        n_gram_dict[new_key] = new_value # updated key & value
        del n_gram_dict[key] # delete the old key
        R += new_value # keep track of R
    if R > expected_R:
        print("Error") # not sure what you want if it's longer than expected
    else:
        return n_gram_dict # return updated n_gram_dict


    #def factors(distance_repeats):
    #    total = len(ciphertext)
    #    for i in range(1, 25): # testing all possible length
    #def repeats(ciphertext):
    #lst int gaps bewteen repeats

    #extract_heuristic_n_gram()
    #random characters
4    #prob r evenly distributed
"""
import re
from itertools import takewhile

def exact_n_gram(ciphertext, n): # returns a list of the different distances of n_grams
    # first find repeats
    loc_first_n_gram = 0
    loc_second_n_gram = 0
    lst_distances = []
    for i in range(0, len(ciphertext)): # checking each chr as first letter in n_gram
        for x in range(0,24): # checking all possible lengths of n_gram
            # find in string
            n_gram = ciphertext[i:x] # string of potential n_gram
            for m in re.finditer(n_gram, ciphertext): # find two occurances
                loc_first_n_gram = m.start() # first occurance
                loc_second_n_gram = m.end() # second occurance
                distance_n_gram = loc_second_n_gram - loc_first_n_gram # find distance
                if distance_n_gram not in lst_distances: # if not already in the list
                    lst_distances += distance_n_gram # add to list of distances
    return lst_distances


def exact_n_gram2(ciphertext, n): # returns the distance of the first n_gram found
    # first find repeats
    loc_first_n_gram = 0
    loc_second_n_gram = 0
    for i in range(0, len(ciphertext)): # checking each chr as first letter in n_gram
        for x in range(0,24): # checking all possible lengths of n_gram
            # find in string
            n_gram = ciphertext[i:x] # string of potential n_gram
            for m in re.finditer(n_gram, ciphertext): # find two occurances
                loc_first_n_gram = m.start() # first occurance
                loc_second_n_gram = m.end() # second occurance
                distance_n_gram = loc_second_n_gram - loc_first_n_gram # find distance
                return distance_n_gram # return distance

def get_possible_key_lengths(distances):
    candidates = [1]
    counts = dict.fromkeys(range(2,24), 0)
    for dst in distances:
        for kl in range(2,24):
            if dst % kl == 0:
                counts[kl] += 1
    ranked_lengths = sorted(((k,v) for k, v in filter(lambda x: x[1] > 0,counts.items())), key=lambda x: x[1], reverse=True)
    if next(iter(ranked_lengths), None) is None:
        return candidates
    most_common = ranked_lengths[0][1]
    candidates.extend(k for k,v in takewhile(lambda x: x[1] > 0.5*most_common, ranked_lengths))
    return candidates
