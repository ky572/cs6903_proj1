import sys
from statistics import stdev, median

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
#        ngram_freq = find_ngram_frequency(5, s)
#        print(str(sorted(ngram_freq.items(), key=lambda x: x[1], reverse=True)[:10]))

    most_freq = list(map(lambda x: (x[0], max(find_ngram_frequency(5, x[1]).values())),
                        shuffled_shifts))

#    for p,s in shuffled_shifts:
#        ngram_freq = find_ngram_frequency(5, s)
#        most_freq.append((p,max(ngram_freq)))
    reps = list(map(lambda x: x[1], most_freq))       
    std = stdev(reps)
    med = median(reps)
    max_rep = max(most_freq, key=lambda x: x[1])
    if max_rep[1] > med+std:
        return max_rep[0]

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

