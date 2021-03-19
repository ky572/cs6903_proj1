import sys
from statistics import stdev, median, mean

test1_plaintexts = [
    'cabooses meltdowns bigmouth makework flippest neutralizers gipped mule antithetical imperials carom masochism stair retsina dullness adeste corsage saraband promenaders gestational mansuetude fig redress pregame borshts pardoner reforges refutations calendal moaning doggerel dendrology governs ribonucleic circumscriptions reassimilating machinize rebuilding mezcal fluoresced antepenults blacksmith constance furores chroniclers overlie hoers jabbing resigner quartics polishers mallow hovelling ch',
    'biorhythmic personalizing abjure greets rewashed thruput kashmir chores fiendishly combatting alliums lolly milder postpaid larry annuli codgers apostatizing scrim carillon rust grimly lignifying lycanthrope samisen founds millimeters pentagon humidification checkup hilts agonise crumbs rejected kangaroo forenoons grazable acidy duellist potent recyclability capture memorized psalmed meters decline deduced after oversolicitousness demoralizers ologist conscript cronyisms melodized girdles nonago',
    'hermitage rejoices oxgall bloodstone fisticuff huguenot janitress assailed eggcup jerseyites fetas leipzig copiers pushiness fesse precociously modules navigates gaiters caldrons lisp humbly datum recite haphazardly dispassion calculability circularization intangibles impressionist jaggy ascribable overseen copses devolvement permutationists potations linesmen hematic fowler pridefully inversive malthus remainders multiplex petty hymnaries cubby donne ohioans avenues reverts glide photos antiaci',
    'leonardo oxygenate cascade fashion fortifiers annelids co intimates cads expanse rusting quashing julienne hydrothermal defunctive permeation sabines hurries precalculates discourteously fooling pestles pellucid circlers hampshirites punchiest extremist cottonwood dadoes identifiers retail gyrations dusked opportunities ictus misjudge neighborly aulder larges predestinate bandstand angling billet drawbridge pantomimes propelled leaned gerontologists candying ingestive museum chlorites maryland s',
    'undercurrents laryngeal elevate betokened chronologist ghostwrites ombres dollying airship probates music debouching countermanded rivalling linky wheedled heydey sours nitrates bewares rideable woven rerecorded currie vasectomize mousings rootstocks langley propaganda numismatics foetor subduers babcock jauntily ascots nested notifying mountainside dirk chancellors disassociating eleganter radiant convexity appositeness axonic trainful nestlers applicably correctional stovers organdy bdrm insis'
]

def get_alpha_index(ch):
    return 26 if ch == ' ' else ord(ch) - ord('a')

def find_shift(p, c):
    po = get_alpha_index(p)
    co = get_alpha_index(c)
    if co >= po:
        return co - po
    return 27 - po + co

def list_shifts(ptext, ctext):
    p_len = len(ptext)
    return list(map(find_shift, ptext, ctext[:p_len]))

def find_ngram_frequency(n, seq):
    ngrams = {}
    l = len(seq)
    for i in range(0,l-n+1):
        ngram = tuple(seq[i:i+n])
        if ngram not in ngrams:
            ngrams[ngram] = 1
        else:
            ngrams[ngram] += 1
    return ngrams

def find_element_frequency(seq):
    elems = {}
    l = len(seq)
    for e in seq:
        if e not in elems:
            elems[e] = 1
        else:
            elems[e] += 1
    return elems

def search_through_shifts(start_index, shift_dict, next_lists, current_list):
    i = start_index
    shift_count = len(shift_dict)
#    current_dict = dict(shift_dict)
    current_shifts = set()
    new_shift_indices = []
    l = len(current_list)
    print(f'Starting at {start_index} with {len(next_lists)} remaining and {len(shift_dict)} previous shifts')
#    while len(current_dict) < 25 and i < l:
    while shift_count + len(current_shifts) < 25 and i < l:
        #scan through current list until you reach the end, or you counted more than 24 shifts
        #as you scan, add the shifts to the dictionary, or increment their count
        s = current_list[i]
        if s not in shift_dict and s not in current_shifts:
            current_shifts.add(s)
            new_shift_indices.append(i)
#        if s not in current_dict:
#            current_dict[s] = 1
#            new_shift_indices.append(i)
#        else:
#            current_dict[s] += 1
        i += 1
    #out of the loop, either we exceeded 24 or we reached the end
#    if len(current_dict) > 24:
    if shift_count + len(current_shifts) > 24:
        #we exceeded 24 distinct shifts
        #if next_lists is empty, then return None
#        print(f'Exceeded 24 shifts at {i}')
#        print(f'Current dict: {str(current_dict)}')
#        print(f'Last added: {s}')
        if len(next_lists) == 0:
            return None
        #recurse through the next_lists until we get a non-None result
        #every time we get a None result, decrement i
        #in the end we either find a valid result, or we ran out of room to decrement
        
        for li in new_shift_indices[::-1]:
            current_shifts.remove(current_list[li])
            tail = search_through_shifts(li, shift_dict | current_shifts, next_lists[1:], next_lists[0])
 #       while i > start_index:
            #go back to the index before we added the last shift to the bag
 #           i -= 1
 #           current_dict[current_list[i]] -= 1
 #           if current_dict[current_list[i]] == 0:
 #               current_dict.pop(s)
#            tail = search_through_shifts(i, current_dict, next_lists[1:], next_lists[0])
            if tail is not None:
                return [(start_index, i) if i > start_index else None] + tail

        return None
        
    elif i >= l:
        #we reached the end and we haven't exceeded 24 distinct shifts, then we're done
        #return the start and end index of this partition, and None for the remaining lists
       return [(start_index, i)] + [None for n in next_lists]
    
    return None

def guess_basic_no_random_test1(ciphertext):
    #first pass, if plaintext and ciphertext lengths match
    #check how many distinct shift values are necessary
    for p in test1_plaintexts:
        if len(p) != len(ciphertext):
            continue
        shifts = list_shifts(p, ciphertext)
        if len(set(shifts)) < 25:
            return p
    return None 

def guess_cyclical_random_test1(ciphertext):
    #second pass, let's assume there are some random characters and the key is cyclical
    shuffled_shifts = []
    for p in test1_plaintexts:
        if len(p) >= len(ciphertext):
            continue
        shifts = []
        r = len(ciphertext) - len(p)
        for i in range(0,r+1):
            shifts.extend(list_shifts(p, ciphertext[i:i+len(p)]))
        shuffled_shifts.append((p,shifts))

#    shuffled_shifts = [(p,[]),(p,[]),(p,[])]
#    for p,s in shuffled_shifts:
#        print(p)
#        ngram_freq = find_ngram_frequency(6, s)
#        print(str(sorted(ngram_freq.items(), key=lambda x: x[1], reverse=True)[:10]))

    most_freq = list(map(lambda x: (x[0], max(find_ngram_frequency(6, x[1]).values())),
                        shuffled_shifts))

#    reps = list(map(lambda x: x[1], most_freq))       
#    std = stdev(reps)
#    med = median(reps)
#    max_rep = max(most_freq, key=lambda x: x[1])
#    if max_rep[1] > (med+(std*1.5)):
#        return max_rep[0]

#    reps = sorted(reps)
#    iqr = reps[3] - reps[1]
#    if max_rep[1] > 1.5*iqr:
#        return max_rep[0]
    
    reps = list(map(lambda x: x[1], most_freq))
    max_rep = max(most_freq, key=lambda x: x[1])   
    reps = sorted(reps)
    avg = mean(reps[:4])
    if max_rep[1] > 2*avg:
        return max_rep[0]
    return None

def get_shuffled_shifts(ciphertext):
    shuffled_shifts = []
    for p in test1_plaintexts:
        if len(p) >= len(ciphertext):
            continue
        shifts = []
        r = len(ciphertext) - len(p)
        for i in range(0,r+1):
            shifts.extend(list_shifts(p, ciphertext[i:i+len(p)]))
        shuffled_shifts.append((p,shifts))
    return shuffled_shifts

def find_indices_in_set(s, seq):
    l = len(seq)
    indices = []
    for i in range(l):
        e = seq[i]
        if e in s:
            indices.append(i)
    return indices

def find_longest_continuous_subarray(seq):
    max_len = 0
    l = len(seq)
    for i in range(l):
        
 
def guess_noncyclical_random_test1(ciphertext):
    #third pass, let's assume there are some random characters and the key is not cyclical
    
    shuffled_shifts = get_shuffled_shifts(ciphertext)    
       
    return map(lambda x: (x[0], sorted(find_element_frequency(x[1]).items(),
                                key=lambda y: y[1],
                                reverse=True)),
        shuffled_shifts)
    return None

def guess_test1_plaintext(ciphertext):
    guess = guess_basic_no_random_test1(ciphertext)
    if guess is not None:
        return guess

    guess = guess_cyclical_random_test1(ciphertext)
    if guess is not None:
        return guess

    return None

def guess_plaintext(ciphertext):
    test1_guess = guess_test1_plaintext(ciphertext)
    if test1_guess is not None:
        return test1_guess

    return None

if __name__ == '__main__':
    ciphertext = next(sys.stdin)
    guess = guess_plaintext(ciphertext)
    print(guess)

