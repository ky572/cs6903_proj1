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

def schedule_key(i,t,l):
    return i % t

def shift(plaintext, key, t):
    p_len = len(plaintext)
    p_i = 0
    c_i = 0
    while p_i < p_len:
        j = schedule_key(c_i,t,p_len)
        if j > -1 and j < t:
            p = ord(plaintext[p_i])
            p = 26 if p == ord(' ') else p - ord('a')
            c = possible_chars[(p + key[j]) % 27] 
            p_i += 1
        else:
            c = random.choice(possible_chars)
        yield c
        c_i += 1

def encrypt(plaintext):
    t = random.randint(1,24)
    key = [random.randint(0,26) for i in range(t)]
    print('Plaintext: ' + plaintext + '\n')
    print('Key: [' + ','.join(str(k) for k in key) + ']\n')
    print('Ciphertext: ' + ''.join(shift(plaintext, key, t)) + '\n')

def generate_test1_cipher():
    plain = random.choice(test1_plaintexts)
    encrypt(plain)
    

if __name__ == '__main__':
    generate_test1_cipher()
