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

    most_freq = list(map(lambda x: (x.plaintext, max(x.find_ngram_freq(6).values())),
                        shuffled_shifts))
   
    reps = list(map(lambda x: x[1], most_freq))
    max_rep = max(most_freq, key=lambda x: x[1])   
    reps = sorted(reps)

    if reps[4] == reps[3]:
        return None
    avg = mean(reps[:4])

    if max_rep[1] > 2*avg:
        return max_rep[0]

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
        partitions.append((psd.plaintext, lengths))
    

    for i in range(24):
        #start comparing each plaintext's max partition for a shift set of size i
        target = 4.5 if i < 12 else 7.5
        dist = [(part[0], part[1][i]) for part in partitions]
        sorted_dist = sorted(dist, key=lambda x: x[1])
        raw_dist = [d[1] for d in sorted_dist]
        med = raw_dist[2]
        mad = median(abs(x-med) for x in raw_dist)
        
        if mad > 0:
            zscores = [(d[0],.6745*abs(d[1]-med)/mad,d[1]) for d in sorted_dist]
            max_zscore = max(zscores, key=lambda x: x[2])
#            print(dist)
#            print([z[1] for z in zscores])
#            print(max_zscore)
#            print(max_zscore[1]/sum(z[1] for z in zscores))
            if max_zscore[1] > target:
               return (max_zscore[0],max_zscore[1]/sum(z[1] for z in zscores))
    return (None,None)

def guess_test1_plaintext(ciphertext):
    guess = guess_basic_no_random_test1(ciphertext)
    if guess is not None:
        return (guess,1)

    guess = guess_cyclical_random_test1(ciphertext)
    if guess is not None:
        return (guess,1)

    return guess_noncyclical_random_test1(ciphertext)

def guess_plaintext(ciphertext):
    test1_guess, confidence = guess_test1_plaintext(ciphertext)
    if test1_guess is not None:
        return test1_guess

    return None

if __name__ == '__main__':
    ciphertext = str.rstrip(next(sys.stdin))
    guess = guess_plaintext(ciphertext)
    print(guess)

