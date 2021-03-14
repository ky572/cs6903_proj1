import random
import argparse

class Cipher_Generator:
    def __init__(self):
        global possible_chars, num_possible_chars
        possible_chars='abcdefghijklmnopqrstuvwxyz '
        num_possible_chars = 27

        self.test1_plaintexts = [
            'cabooses meltdowns bigmouth makework flippest neutralizers gipped mule antithetical imperials carom masochism stair retsina dullness adeste corsage saraband promenaders gestational mansuetude fig redress pregame borshts pardoner reforges refutations calendal moaning doggerel dendrology governs ribonucleic circumscriptions reassimilating machinize rebuilding mezcal fluoresced antepenults blacksmith constance furores chroniclers overlie hoers jabbing resigner quartics polishers mallow hovelling ch',
            'biorhythmic personalizing abjure greets rewashed thruput kashmir chores fiendishly combatting alliums lolly milder postpaid larry annuli codgers apostatizing scrim carillon rust grimly lignifying lycanthrope samisen founds millimeters pentagon humidification checkup hilts agonise crumbs rejected kangaroo forenoons grazable acidy duellist potent recyclability capture memorized psalmed meters decline deduced after oversolicitousness demoralizers ologist conscript cronyisms melodized girdles nonago',
            'hermitage rejoices oxgall bloodstone fisticuff huguenot janitress assailed eggcup jerseyites fetas leipzig copiers pushiness fesse precociously modules navigates gaiters caldrons lisp humbly datum recite haphazardly dispassion calculability circularization intangibles impressionist jaggy ascribable overseen copses devolvement permutationists potations linesmen hematic fowler pridefully inversive malthus remainders multiplex petty hymnaries cubby donne ohioans avenues reverts glide photos antiaci',
            'leonardo oxygenate cascade fashion fortifiers annelids co intimates cads expanse rusting quashing julienne hydrothermal defunctive permeation sabines hurries precalculates discourteously fooling pestles pellucid circlers hampshirites punchiest extremist cottonwood dadoes identifiers retail gyrations dusked opportunities ictus misjudge neighborly aulder larges predestinate bandstand angling billet drawbridge pantomimes propelled leaned gerontologists candying ingestive museum chlorites maryland s',
            'undercurrents laryngeal elevate betokened chronologist ghostwrites ombres dollying airship probates music debouching countermanded rivalling linky wheedled heydey sours nitrates bewares rideable woven rerecorded currie vasectomize mousings rootstocks langley propaganda numismatics foetor subduers babcock jauntily ascots nested notifying mountainside dirk chancellors disassociating eleganter radiant convexity appositeness axonic trainful nestlers applicably correctional stovers organdy bdrm insis'
        ]

        self.test2_words = [
            'awesomeness',
            'hearkened',
            'aloneness',
            'beheld',
            'courtship',
            'swoops',
            'memphis',
            'attentional',
            'pintsized',
            'rustics',
            'hermeneutics',
            'dismissive',
            'delimiting',
            'proposes',
            'between',
            'postilion',
            'repress',
            'racecourse',
            'matures',
            'directions',
            'pressed',
            'miserabilia',
            'indelicacy',
            'faultlessly',
            'chuted',
            'shorelines',
            'irony',
            'intuitiveness',
            'cadgy',
            'ferries',
            'catcher',
            'wobbly',
            'protruded',
            'combusting',
            'unconvertible',
            'successors',
            'footfalls',
            'bursary',
            'myrtle',
            'photocompose'
        ]
        random.seed()
        self.schedulers = [
            lambda i,t,l: i % t,
            lambda i,t,l: (2*i) % t,
            lambda i,t,l: (i*i) % t,
            lambda i,t,l: t - 1 - (i % t),
            lambda i,t,l: (i*3) % t,
            lambda i,t,l: (i >> 1) % t,
            lambda i,t,l: t - 1 - ((i*2) % t),
        ]
   
    def distribution(self,s):
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


    def cycle_through_schedulers(self,i,t,l):
        if i < 20:
            sched = self.schedulers[0]
        elif i < 50:
            sched = self.schedulers[1]
        elif i < 100:
            sched = self.schedulers[2]
        elif i < 150:
            sched = self.schedulers[3]
        elif i < 250:
            sched = self.schedulers[4]
        elif i < 350:
            sched = self.schedulers[5]
        elif i < 450:
            sched = self.schedulers[6]
        else :
            scheduler_index = (i - 450) % len(self.schedulers)
            sched = self.schedulers[scheduler_index]
        return sched(i,t,l)   

    def random_key(self, k, p_len):
        k_len = len(k)
        schedule = [random.randrange(k_len) for i in range(p_len)]
        def random_scheduler(i,t,l):
            return schedule[i]
        return random_scheduler

    def valid_key_index(self,j,t):
        return j > -1 and j < t

    def shift(self, plaintext, key, t, s_fn, insert_random):
        p_len = len(plaintext)
        p_i = 0
        c_i = 0
        random_indices = []
        if insert_random:
            num_random = random.randint(1,50)
            total_chars = p_len+num_random
            random_indices = sorted(random.sample(range(0,total_chars-1), num_random))
        random_indices = iter(random_indices)
        next_random = next(random_indices, None)
        while p_i < p_len:
            if c_i == next_random:
                c = random.choice(possible_chars)
                next_random = next(random_indices, None)
                j = -1
            else:
                j = s_fn(p_i,t,p_len)
                p = ord(plaintext[p_i])
                p = 26 if p == ord(' ') else p - ord('a')
                c = possible_chars[(p + key[j]) % 27] 
                p_i += 1

            yield (c, p_i-1 if j >= 0 else -1, j)
            c_i += 1

    def encrypt(self, plaintext,insert_random, random_sched):
        t = random.randint(1,24)
        key = [random.randint(0,26) for i in range(t)]
        if random_sched:
            s_fn = self.random_key(key, len(plaintext))
        else:
            sched_options = self.schedulers + [self.cycle_through_schedulers]
            si = random.randrange(len(sched_options))
            s_fn = sched_options[si]
#        print('Plaintext: ' + plaintext + '\n')
    #    distribution(plaintext)
#        print(f'L={len(plaintext)}')
#        print('Key: [' + ','.join(str(k) for k in key) + ']\n')
#        print(f'Key length: {len(key)}')
        output = list(self.shift(plaintext, key, t, s_fn, insert_random))
        ciphertext = ''.join(c for c,pi,j in output)
#        print('Ciphertext: ' + ciphertext + '\n')
    #    distribution(ciphertext)
#        print(f'Cipher length={len(ciphertext)}')
#        print('Shifts: [' + ','.join(f'({pi},{j})' for c,pi,j in output) + ']')
        return (key,ciphertext)

    def generate_test1_cipher(self, insert_random=True, random_sched=False):
        plain = random.choice(self.test1_plaintexts)
        key,cipher = self.encrypt(plain,insert_random,random_sched)
        return (plain,cipher,key)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--insert_random', action='store_true')
    parser.add_argument('--random_sched', action='store_true')
    args = parser.parse_args()
    gen = Cipher_Generator()
    p,c,key = gen.generate_test1_cipher(insert_random=args.insert_random, random_sched=args.random_sched)
    print(f'Plaintext: {p}')
    print(f'L={len(p)}')
    print(f"Key: [{','.join(str(k) for k in key)}]")
    print(f'Key length: {len(key)}')
    print(f'Ciphertext: {c}')
    print(f'Cipher length={len(c)}')
