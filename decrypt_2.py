# from decrypter import *
from collections import defaultdict
from encryption_test import Cipher_Generator 

plain_text1 = "cabooses meltdowns bigmouth makework flippest neutralizers gipped mule antithetical imperials carom masochism stair retsina dullness adeste corsage saraband promenaders gestational mansuetude fig redress pregame borshts pardoner reforges refutations calendal moaning doggerel dendrology governs ribonucleic circumscriptions reassimilating machinize rebuilding mezcal fluoresced antepenults blacksmith constance furores chroniclers overlie hoers jabbing resigner quartics polishers mallow hovelling ch"

plain_text2 = "biorhythmic personalizing abjure greets rewashed thruput kashmir chores fiendishly combatting alliums lolly milder postpaid larry annuli codgers apostatizing scrim carillon rust grimly lignifying lycanthrope samisen founds millimeters pentagon humidification checkup hilts agonise crumbs rejected kangaroo forenoons grazable acidy duellist potent recyclability capture memorized psalmed meters decline deduced after oversolicitousness demoralizers ologist conscript cronyisms melodized girdles nonago"

plain_text3 = "hermitage rejoices oxgall bloodstone fisticuff huguenot janitress assailed eggcup jerseyites fetas leipzig copiers pushiness fesse precociously modules navigates gaiters caldrons lisp humbly datum recite haphazardly dispassion calculability circularization intangibles impressionist jaggy ascribable overseen copses devolvement permutationists potations linesmen hematic fowler pridefully inversive malthus remainders multiplex petty hymnaries cubby donne ohioans avenues reverts glide photos antiaci"

plain_text4 = "leonardo oxygenate cascade fashion fortifiers annelids co intimates cads expanse rusting quashing julienne hydrothermal defunctive permeation sabines hurries precalculates discourteously fooling pestles pellucid circlers hampshirites punchiest extremist cottonwood dadoes identifiers retail gyrations dusked opportunities ictus misjudge neighborly aulder larges predestinate bandstand angling billet drawbridge pantomimes propelled leaned gerontologists candying ingestive museum chlorites maryland s"

plain_text5 = "undercurrents laryngeal elevate betokened chronologist ghostwrites ombres dollying airship probates music debouching countermanded rivalling linky wheedled heydey sours nitrates bewares rideable woven rerecorded currie vasectomize mousings rootstocks langley propaganda numismatics foetor subduers babcock jauntily ascots nested notifying mountainside dirk chancellors disassociating eleganter radiant convexity appositeness axonic trainful nestlers applicably correctional stovers organdy bdrm insis"

alphabet ='abcdefghijklmnopqrstuvwxyz '



words = [
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

class Decrypter_2:
    def __init__(self):
        self.cipher_generator = Cipher_Generator()
        self.plaintexts = [ plain_text1, plain_text2, plain_text3,
            plain_text4, plain_text5 ]
        self.letter_to_index = {}
        for i in range(len(alphabet)):
            letter = alphabet[i]
            self.letter_to_index[letter] = i

    #O(L)
    def calc_edit_distance(self, decrypted_ciphertext, plaintext):
        distance = 0
        com_length = min(len(decrypted_ciphertext), len(plaintext))
        for i in range(com_length):
            distance += decrypted_ciphertext[i] != plaintext[i]
        distance += len(decrypted_ciphertext) - com_length + len(plaintext) - com_length
        return distance
    
    #O(1)
    def single_decode(self, cipher_char, key_digit):
        alpha_len = len(alphabet)
        return alphabet[ (self.letter_to_index[ cipher_char ] + alpha_len - key_digit )%  alpha_len ]
    #O(t)
    def decode(self, ciphertext, key, pos):
        #alphabet[ (self.letter_to_index[ciphertext[pos + i]] + alpha_len - key[i] )%  alpha_len ]
        t = len(key)
        len_decode = min( len(ciphertext) - pos, t)
        return [ self.single_decode(ciphertext[i+pos], key[i]) for i in range(len_decode) ]


    




    

        