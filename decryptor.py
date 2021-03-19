import sys
from statistics import stdev, median, mean

test1_plaintexts = [
    'cabooses meltdowns bigmouth makework flippest neutralizers gipped mule antithetical imperials carom masochism stair retsina dullness adeste corsage saraband promenaders gestational mansuetude fig redress pregame borshts pardoner reforges refutations calendal moaning doggerel dendrology governs ribonucleic circumscriptions reassimilating machinize rebuilding mezcal fluoresced antepenults blacksmith constance furores chroniclers overlie hoers jabbing resigner quartics polishers mallow hovelling ch',
    'biorhythmic personalizing abjure greets rewashed thruput kashmir chores fiendishly combatting alliums lolly milder postpaid larry annuli codgers apostatizing scrim carillon rust grimly lignifying lycanthrope samisen founds millimeters pentagon humidification checkup hilts agonise crumbs rejected kangaroo forenoons grazable acidy duellist potent recyclability capture memorized psalmed meters decline deduced after oversolicitousness demoralizers ologist conscript cronyisms melodized girdles nonago',
    'hermitage rejoices oxgall bloodstone fisticuff huguenot janitress assailed eggcup jerseyites fetas leipzig copiers pushiness fesse precociously modules navigates gaiters caldrons lisp humbly datum recite haphazardly dispassion calculability circularization intangibles impressionist jaggy ascribable overseen copses devolvement permutationists potations linesmen hematic fowler pridefully inversive malthus remainders multiplex petty hymnaries cubby donne ohioans avenues reverts glide photos antiaci',
    'leonardo oxygenate cascade fashion fortifiers annelids co intimates cads expanse rusting quashing julienne hydrothermal defunctive permeation sabines hurries precalculates discourteously fooling pestles pellucid circlers hampshirites punchiest extremist cottonwood dadoes identifiers retail gyrations dusked opportunities ictus misjudge neighborly aulder larges predestinate bandstand angling billet drawbridge pantomimes propelled leaned gerontologists candying ingestive museum chlorites maryland s',
    'undercurrents laryngeal elevate betokened chronologist ghostwrites ombres dollying airship probates music debouching countermanded rivalling linky wheedled heydey sours nitrates bewares rideable woven rerecorded currie vasectomize mousings rootstocks langley propaganda numismatics foetor subduers babcock jauntily ascots nested notifying mountainside dirk chancellors disassociating eleganter radiant convexity appositeness axonic trainful nestlers applicably correctional stovers organdy bdrm insis'
]

def find_element_frequency(seq):
    elems = {}
    l = len(seq)
    for e in seq:
        if e not in elems:
            elems[e] = 1
        else:
            elems[e] += 1
    return elems

def find_ngram_frequency(n, seq, ngrams):
    l = len(seq)
    for i in range(0,l-n+1):
        ngram = tuple(seq[i:i+n])
        if ngram not in ngrams:
            ngrams[ngram] = 1
        else:
            ngrams[ngram] += 1
    return ngrams

class PlainShiftData:
    def __init__(self, plain, shuffled_shifts):
        self.plaintext = plain
        self.shuffled_shifts = shuffled_shifts
        self.shift_freqs = None
        self.joined_shifts = None

    def get_joined_shifts(self):
        if self.joined_shifts is None:
            self.joined_shifts = [s for sublist in self.shuffled_shifts for s in sublist]
        return self.joined_shifts

    def get_shift_freqs(self):
        if self.shift_freqs is None:
            self.shift_freqs = sorted(find_element_frequency(self.get_joined_shifts()).items(),
                                  key=lambda x: x[1],
                                  reverse=True)
        return self.shift_freqs

    def find_ngram_freq(self, n):
        ngrams = {}
        for s in self.shuffled_shifts:
            ngrams = find_ngram_frequency(n, s, ngrams)
        return ngrams

def print_shift_freqs(psd):
    print((psd.plaintext, psd.get_shift_freqs()))

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

def get_shuffled_shifts(ciphertext):
    shuffled_shifts = []
    for p in test1_plaintexts:
        if len(p) >= len(ciphertext):
            continue
        shifts = []
        r = len(ciphertext) - len(p)
        for i in range(0,r+1):
            shifts.append(list_shifts(p, ciphertext[i:i+len(p)]))
        shuffled_shifts.append(PlainShiftData(p,shifts))
    return shuffled_shifts

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
    shuffled_shifts = get_shuffled_shifts(ciphertext)

#    shuffled_shifts = [(p,[]),(p,[]),(p,[])]
#    for p,s in shuffled_shifts:
#        print(p)
#        ngram_freq = find_ngram_frequency(6, s)
#        print(str(sorted(ngram_freq.items(), key=lambda x: x[1], reverse=True)[:10]))

    most_freq = list(map(lambda x: (x.plaintext, max(x.find_ngram_freq(6).values())),
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
#    print(most_freq)
    if reps[4] == reps[3]:
        return None
    avg = mean(reps[:4])
#    avg = mean(reps)
    if max_rep[1] > 2*avg:
        return max_rep[0]
#    std = stdev(reps)
#    if (max_rep[1] - avg)/std > 4:
#        return max_rep[0]
 
    return None

def find_indices_in_set(s, seq):
    l = len(seq)
    indices = []
    for i in range(l):
        e = seq[i]
        if e in s:
            indices.append(i)
    return indices

def find_longest_continuous_subarray(seq):
    max_len = 1
    curr_len = 1
    l = len(seq)
    if l == 0: 
        return 0
    last = seq[0]
    for i in range(1,l):
        curr = seq[i]
        if curr == last+1:
            curr_len += 1
        else:
            if curr_len > max_len:
                max_len = curr_len
            curr_len = 1
        last = curr
    return max_len
 
def guess_noncyclical_random_test1(ciphertext):
    #third pass, let's assume there are some random characters and the key is not cyclical
    
    shuffled_shifts = get_shuffled_shifts(ciphertext)    
    partitions = []
   
    for psd in shuffled_shifts:
        shift_set = set()
        lengths = []
        for rank in range(24):
            shift_set.add(psd.get_shift_freqs()[rank][0])
            lengths.append(max(find_longest_continuous_subarray(find_indices_in_set(shift_set, seq)) for seq in psd.shuffled_shifts))
#            lengths.append(find_longest_continuous_subarray(
#                find_indices_in_set(shift_set, psd.get_joined_shifts())))
#        print((psd.plaintext, lengths))
        partitions.append((psd.plaintext, lengths))
    
#    print(partitions)
    for i in range(24):
        #start comparing each plaintext's max partition for a shift set of size i
        dist = [(part[0], part[1][i]) for part in partitions]
        sorted_dist = sorted(dist, key=lambda x: x[1])
        raw_dist = [d[1] for d in sorted_dist]
#        iqr = sorted_dist[3][1] - sorted_dist[1][1]
#        outlier_cutoff = sorted_dist[3][1] + (1.5*iqr)
#        if sorted_dist[4][1] > outlier_cutoff:
#            print(f'Outlier found at {i}')
#            return sorted_dist[4][0]
#        avg = mean(d[1] for d in sorted_dist[:4])
#        if sorted_dist[4][1] > 2*avg:
#            print(f'Outlier found at {i}')
#            return sorted_dist[4][0]
        med = raw_dist[2]
        mad = median(abs(x-med) for x in raw_dist)
        if mad > 0:
            max_zscore = .6745*abs(sorted_dist[4][1]-med)/mad
            if max_zscore > 3.5:
                return sorted_dist[4][0]
        else:
            avg = mean(raw_dist)
            if sorted_dist[4][1] > 2*avg:
                return sorted_dist[4][0]
#    return partitions
    return None

def guess_test1_plaintext(ciphertext):
    guess = guess_basic_no_random_test1(ciphertext)
    if guess is not None:
        return guess

    guess = guess_cyclical_random_test1(ciphertext)
    if guess is not None:
        return guess

    guess = guess_noncyclical_random_test1(ciphertext)
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

