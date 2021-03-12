import random

possible_chars='abcdefghijklmnopqrstuvwxyz '

test1_plaintexts = [
    'cabooses meltdowns bigmouth makework flippest neutralizers gipped mule antithetical imperials carom masochism stair retsina dullness adeste corsage saraband promenaders gestational mansuetude fig redress pregame borshts pardoner reforges refutations calendal moaning doggerel dendrology governs ribonucleic circumscriptions reassimilating machinize rebuilding mezcal fluoresced antepenults blacksmith constance furores chroniclers overlie hoers jabbing resigner quartics polishers mallow hovelling ch',
    'biorhythmic personalizing abjure greets rewashed thruput kashmir chores fiendishly combatting alliums lolly milder postpaid larry annuli codgers apostatizing scrim carillon rust grimly lignifying lycanthrope samisen founds millimeters pentagon humidification checkup hilts agonise crumbs rejected kangaroo forenoons grazable acidy duellist potent recyclability capture memorized psalmed meters decline deduced after oversolicitousness demoralizers ologist conscript cronyisms melodized girdles nonago',
    'hermitage rejoices oxgall bloodstone fisticuff huguenot janitress assailed eggcup jerseyites fetas leipzig copiers pushiness fesse precociously modules navigates gaiters caldrons lisp humbly datum recite haphazardly dispassion calculability circularization intangibles impressionist jaggy ascribable overseen copses devolvement permutationists potations linesmen hematic fowler pridefully inversive malthus remainders multiplex petty hymnaries cubby donne ohioans avenues reverts glide photos antiaci',
    'leonardo oxygenate cascade fashion fortifiers annelids co intimates cads expanse rusting quashing julienne hydrothermal defunctive permeation sabines hurries precalculates discourteously fooling pestles pellucid circlers hampshirites punchiest extremist cottonwood dadoes identifiers retail gyrations dusked opportunities ictus misjudge neighborly aulder larges predestinate bandstand angling billet drawbridge pantomimes propelled leaned gerontologists candying ingestive museum chlorites maryland s',
    'undercurrents laryngeal elevate betokened chronologist ghostwrites ombres dollying airship probates music debouching countermanded rivalling linky wheedled heydey sours nitrates bewares rideable woven rerecorded currie vasectomize mousings rootstocks langley propaganda numismatics foetor subduers babcock jauntily ascots nested notifying mountainside dirk chancellors disassociating eleganter radiant convexity appositeness axonic trainful nestlers applicably correctional stovers organdy bdrm insis'
]

random.seed()

def distribution(s):
    count = {}
    for i in s:
        if count.__contains__(i):
            count[i] += 1
        else:
            count[i] = 1
    print('{:<8}{:<8}{:>14}'.format('letter', 'count', 'percentage'))
    for i in count:
        if i == ' ':
            print('{:<8}{:<8}{:>12.2f}%'.format('<space>', count[i], count[i]/len(s) * 100))
        else:
            print('{:<8}{:<8}{:>12.2f}%'.format(i, count[i], count[i]/len(s) * 100))


def schedule_key(i,t,l):
#    return i % t
#    schedulers = [
#        lambda i,t: i % t,
#        lambda i,t: (2*i) % t,
#        lambda i,t: (i*i) % t,
#        lambda i,t: t - 1 - (i % t),
#        lambda i,t: (i*3) % t,
#        lambda i,t: (i >> 1) % t,
#        lambda i,t: t - 1 - ((i*2) % t)
#    ]
    schedulers = [
        lambda i,t: i % (t+1),
        lambda i,t: (2*i) % (t+1),
        lambda i,t: (i*i) % (t+1),
        lambda i,t: t - 1 - (i % (t+1)),
        lambda i,t: (i*3) % (t+1),
        lambda i,t: (i >> 1) % (t+1),
        lambda i,t: t - 1 - ((i*2) % (t+1))
    ]
   
    if i < 20:
        sched = schedulers[0]
    elif i < 50:
        sched = schedulers[1]
    elif i < 100:
        sched = schedulers[2]
    elif i < 150:
        sched = schedulers[3]
    elif i < 250:
        sched = schedulers[4]
    elif i < 350:
        sched = schedulers[5]
    elif i < 450:
        sched = schedulers[6]
    else :
        scheduler_index = (i - 450) % len(schedulers)
        sched = schedulers[scheduler_index]
    return sched(i,t)    
#    return i % (t + 2)    


def valid_key_index(j,t):
    return j > -1 and j < t

def shift(plaintext, key, t):
    p_len = len(plaintext)
    p_i = 0
    c_i = 0
    while p_i < p_len:
        j = schedule_key(c_i,t,p_len)
        if valid_key_index(j,t):
            p = ord(plaintext[p_i])
            p = 26 if p == ord(' ') else p - ord('a')
            c = possible_chars[(p + key[j]) % 27] 
            p_i += 1
        else:
            c = random.choice(possible_chars)
        yield (c, p_i-1 if valid_key_index(j,t) else -1, j)
        c_i += 1

def encrypt(plaintext):
    t = random.randint(1,24)
    key = [random.randint(0,26) for i in range(t)]
    print('Plaintext: ' + plaintext + '\n')
#    distribution(plaintext)
    print(f'L={len(plaintext)}')
    print('Key: [' + ','.join(str(k) for k in key) + ']\n')
    print(f'Key length: {len(key)}')
    output = list(shift(plaintext, key, t))
    ciphertext = ''.join(c for c,pi,j in output)
    print('Ciphertext: ' + ciphertext + '\n')
#    distribution(ciphertext)
    print(f'Cipher length={len(ciphertext)}')
    print('Shifts: [' + ','.join(f'({pi},{j})' for c,pi,j in output) + ']')

def generate_test1_cipher():
    plain = random.choice(test1_plaintexts)
    encrypt(plain)
    

if __name__ == '__main__':
    generate_test1_cipher()
