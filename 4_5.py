from collections import defaultdict

import random

'''
I have combined 4) and 5)
now 4)decrypt_key returns 5 decrypted cipher text
'''

def convert_string_to_vec_chars(string):
    return list(string)

plain_text1 = "cabooses meltdowns bigmouth makework flippest neutralizers gipped mule antithetical imperials carom masochism stair retsina dullness adeste corsage saraband promenaders gestational mansuetude fig redress pregame borshts pardoner reforges refutations calendal moaning doggerel dendrology governs ribonucleic circumscriptions reassimilating machinize rebuilding mezcal fluoresced antepenults blacksmith constance furores chroniclers overlie hoers jabbing resigner quartics polishers mallow hovelling ch"

plain_text2 = "biorhythmic personalizing abjure greets rewashed thruput kashmir chores fiendishly combatting alliums lolly milder postpaid larry annuli codgers apostatizing scrim carillon rust grimly lignifying lycanthrope samisen founds millimeters pentagon humidification checkup hilts agonise crumbs rejected kangaroo forenoons grazable acidy duellist potent recyclability capture memorized psalmed meters decline deduced after oversolicitousness demoralizers ologist conscript cronyisms melodized girdles nonago"

plain_text3 = "hermitage rejoices oxgall bloodstone fisticuff huguenot janitress assailed eggcup jerseyites fetas leipzig copiers pushiness fesse precociously modules navigates gaiters caldrons lisp humbly datum recite haphazardly dispassion calculability circularization intangibles impressionist jaggy ascribable overseen copses devolvement permutationists potations linesmen hematic fowler pridefully inversive malthus remainders multiplex petty hymnaries cubby donne ohioans avenues reverts glide photos antiaci"

plain_text4 = "leonardo oxygenate cascade fashion fortifiers annelids co intimates cads expanse rusting quashing julienne hydrothermal defunctive permeation sabines hurries precalculates discourteously fooling pestles pellucid circlers hampshirites punchiest extremist cottonwood dadoes identifiers retail gyrations dusked opportunities ictus misjudge neighborly aulder larges predestinate bandstand angling billet drawbridge pantomimes propelled leaned gerontologists candying ingestive museum chlorites maryland s"

plain_text5 = "undercurrents laryngeal elevate betokened chronologist ghostwrites ombres dollying airship probates music debouching countermanded rivalling linky wheedled heydey sours nitrates bewares rideable woven rerecorded currie vasectomize mousings rootstocks langley propaganda numismatics foetor subduers babcock jauntily ascots nested notifying mountainside dirk chancellors disassociating eleganter radiant convexity appositeness axonic trainful nestlers applicably correctional stovers organdy bdrm insis"

alphabet ='abcdefghijklmnopqrstuvwxyz '

plain_text_1 = convert_string_to_vec_chars(plain_text1)
plain_text_2 = convert_string_to_vec_chars(plain_text2)
plain_text_3 = convert_string_to_vec_chars(plain_text3)
plain_text_4 = convert_string_to_vec_chars(plain_text4)
plain_text_5 = convert_string_to_vec_chars(plain_text5)

#PYTHON STRING IS IMMUTABLE SO USE LIST OF CHARACTERS INSTEAD
def find_distribution_n_grams(text, n_gram):
    dist = defaultdict(lambda : 0)
    for i in range(len(text) - n_gram + 1):
        chars = text[i: i + n_gram]
        dist[chars] += 1
    return dist

def get_terms_ordered_by_dec_freq(dist):
    n_gram_list = []
    for key in dist:
        n_gram_list.append(key)
    n_gram_list.sort(lambda n_gram_1, n_gram_2: dist[n_gram_1] > dist[n_gram_2])
    return n_gram_list

#each group is defined by shared_n_gram
#so group = shared_n_gram
def get_grouped_n_grams_ordered_by_dec_freq(dist):
    n_gram_list = defaultdict(lambda: [])
    for key in dist:
        shared_n_gram = key[:-1]
        n_gram_list[ shared_n_gram ].append(key)
    for group in n_gram_list:
        n_gram_list[ group ].sort(lambda n_gram_1, n_gram_2: dist[n_gram_1] > dist[n_gram_2])
    return n_gram_list

'''
CHECK FOR WHEN THERE ARE NOT ENOUGH CHARS IN PLAINTEXT
'''

def get_n_gram_converter(ordered_n_gram_cipher, ordered_n_gram_plain):
    n_gram_converter = defaultdict()
    for i in range(len(ordered_n_gram)):
        n_gram_term = ordered_n_gram[i]
        index = i
        if index >= len(ordered_n_gram_plain):
            index = len(ordered_n_gram_plain) - 1
        n_gram_converter[ n_gram_term ] = ordered_n_gram_plain[ index ]
    return n_gram_converter

def map_two_distributions(n_gram_converter, decrypted_ciphertext):

    for i in range(start, len(ciphertext) - n_gram + 1, t):
        n_gram_term = ciphertext[ i: i + n_gram]
        decrypted_ciphertext[ i: i + n_gram] = n_gram_converter[ n_gram_term ]

def concate_2_defaultdict(org_dict, add_dict):
    for key,val in add_dict.items():
        org_dict[ key ] = val

def convert_list_chars_to_string(lst):
    return "".join(lst)

def change_char_at(string, index, char):
    return string[:index] + char + string[index+1:]

def add_to_n_gram_converter( cipher_shared_group, plain_shared_group, grouped_n_gram_freq_cipher, grouped_n_gram_freq_plain):

    ordered_n_gram_cipher = grouped_n_gram_freq_cipher[ cipher_shared_group ]
    ordered_n_gram_plain = grouped_n_gram_freq_plain[ plain_shared_group ]
    n_gram_converter_for_curr_group = get_n_gram_converter(ordered_n_gram_cipher, ordered_n_gram_plain)
    
    return n_gram_converter_for_curr_group


def try_1_edit_distance_away_groups(shared_n_gram_group, grouped_n_gram_freq_cipher, grouped_n_gram_freq_plain, n_gram_converter):
    
    #Try each possible 1 edit distance away
    for i in range(len(shared_n_gram_group)):
        
        #try to replace char with any letter in alphabet
        for char in alphabet:
            
            new_shared_n_gram_group = change_char_at(shared_n_gram_group, i, char)

            #If the new shared_group is present in plaintext
            #map frequency of original group in ciphertext
            #with this new shared_group in plaintext
            if new_shared_n_gram_group in grouped_n_gram_freq_plain:
                ordered_n_gram_cipher = grouped_n_gram_freq_cipher[ shared_n_gram_group ]
                ordered_n_gram_plain = grouped_n_gram_freq_plain[ new_shared_n_gram_group ]
                n_gram_converter_for_curr_group = get_n_gram_converter(ordered_n_gram_cipher, ordered_n_gram_plain)
                concate_2_defaultdict(n_gram_converter, n_gram_converter_for_curr_group)
                return True
    return False

def try_decode_2_gram(shared_n_gram_group, grouped_n_gram_freq_cipher, grouped_2_gram_freq_plain, n_gram_converter):
    second_to_last_char = shared_n_gram_group[-2]
    
    if second_to_last_char in grouped_2_gram_freq_plain:
        ordered_2_gram_cipher = grouped_n_gram_freq_cipher[ shared_n_gram_group ].copy()
        ordered_2_gram_cipher = [ n_gram[-2:] for n_gram in ordered_2_gram_cipher ]

        ordered_2_gram_plain = grouped_2_gram_freq_plain[ second_to_last_char ]

        two_gram_converter_for_curr_group = get_n_gram_converter(ordered_2_gram_cipher, ordered_2_gram_plain)

        for two_gram_cipher, two_gram_plain in two_gram_converter_for_curr_group:
            n_gram_cipher = shared_n_gram_group[:-2] + two_gram_cipher
            if n_gram_cipher in n_gram_converter:
                continue
            n_gram_plain = shared_n_gram_group[:-2] + two_gram_plain
            n_gram_converter[ n_gram_cipher ] = n_gram_plain

        return True

    return False


def try_decode_1_gram(shared_n_gram_group, grouped_n_gram_freq_cipher, ordered_1_gram_plain, n_gram_converter):
    ordered_1_gram_cipher = grouped_n_gram_freq_cipher[ shared_n_gram_group ].copy()
    ordered_1_gram_cipher = [ n_gram[-1] for n_gram in ordered_1_gram_cipher ]
    one_gram_converter_for_curr_group = get_n_gram_converter(ordered_1_gram_cipher, ordered_1_gram_plain)

    for one_gram_cipher, one_gram_plain in one_gram_converter_for_curr_group:
        n_gram_cipher = shared_n_gram_group[:-1] + one_gram_cipher
        if n_gram_cipher in n_gram_converter:
            continue
        n_gram_plain = shared_n_gram_group[:-1] + one_gram_plain
        n_gram_converter[ n_gram_cipher ] = n_gram_plain

def get_grouped_n_gram_converter(grouped_n_gram_freq_cipher, grouped_n_gram_freq_plain, grouped_2_gram_freq_plain, ordered_1_gram_plain):
    n_gram_converter = defaultdict()
    for shared_n_gram_group in ordered_n_gram_by_freq_cipher:
        if shared_n_gram_group in n_gram_converter: #already decoded
            continue
        if shared_n_gram_group not in ordered_n_gram_by_freq_plain:
        
            if not try_1_edit_distance_away_groups(shared_n_gram_group, grouped_n_gram_freq_cipher, grouped_n_gram_freq_plain, n_gram_converter):
                #try decode with 2 grams
                if not try_decode_2_gram(shared_n_gram_group, grouped_n_gram_freq_cipher, grouped_2_gram_freq_plain, n_gram_converter):

                    #then try decode with 1 gram
                    try_decode_1_gram(shared_n_gram_group, grouped_n_gram_freq_cipher, ordered_1_gram_plain, n_gram_converter)

def decrypt_key(t, ciphertext, n_gram = 2):

    #calculate distribution of plaintext1
    dists =  [defaultdict(lambda : 0) for i in range(5)]
    single_dists = [defaultdict(lambda : 0) for i in range(5)]
    two_gram_dists = None
    if n_gram > 2:
        two_gram_dists = [defaultdict(lambda : 0) for i in range(5)]

    ciphertext_lst = convert_string_to_vec_chars(ciphertext)

    plain_texts = [ plain_text_1, plain_text_2, plain_text_3,
        plain_text_4, plain_text_5 ]

    for plaintext_dist_index in range(5):
        text = plain_texts[plaintext_dist_index]
        dists[ plaintext_dist_index ] = find_distribution_n_grams(text, n_gram)
        single_dists[ plaintext_dist_index ] = find_distribution_n_grams(text, 1)
        if n_gram > 2:
            two_gram_dists = find_distribution_n_grams(text, 2)
    
    
    #create a list of n_grams for each plaintext distribution
    #in the order of highest frequency to lowest frequency
    n_gram_freq_lists = []
    for dist in dists:
        n_gram_list = get_terms_ordered_by_dec_freq(dist)
        n_gram_lists.append(n_gram_list)
    
    #create a list of n_grams for each plaintext distribution
    #in the order of highest frequency to lowest frequency
    #grouped by shared_n_gram

    grouped_n_gram_freq_lists = []
    for dist in dists:
        n_gram_list = get_grouped_n_grams_ordered_by_dec_freq(dist)
        grouped_n_gram_freq_lists.append(n_gram_list)

    #only fill 2 grams if n_gram > 2
    two_gram_freq_lists = []
    if n_gram > 2:
        for dist in two_gram_dists:
            two_gram_freq_list = get_grouped_n_grams_ordered_by_dec_freq(dist)
            two_gram_freq_lists.append(two_gram_freq_list)
    
    #SINGLE FREQ LISTS, n_gram = 1
    #USEFUL FOR RANDOM CASE
    single_freq_lists = []

    for dist in single_dists:
        single_freq_list = get_terms_ordered_by_dec_freq(dist)
        single_freq_lists.append(single_freq_list)
    
    decrypted_ciphertexts = [ ciphertext_lst.copy() for i in range(5) ]
    #decrypt from first to t - n_gram + 1 distributions

    for start in range( t - n_gram + 1):
        

        #if it's the first distribution, decrypt as normal
        if start == 0:
            
            cipher_dist = find_distribution_n_grams( ciphertext , n_gram)
    
            ordered_n_gram_cipher = get_terms_ordered_by_dec_freq(cipher_dist)

            for ptext_index in range(5):
                ordered_n_gram_plain = n_gram_lists[ ptext_index ]
                n_gram_converter = get_n_gram_converter( ordered_n_gram_cipher, ordered_n_gram_plain):
                map_two_distributions( n_gram_converter, decrypted_ciphertexts[ ptext_index ])

            continue

        #get the distribution of 5 plaintexts, except the decrypted possibilities
        #according to a shared portion of the n_gram
        
        for ptext_index in range(5):
            
            #GET THE PLAIN DISTRIBUTION OF CIPHERTEXT
            decrypted_ciphertext  = decrypted_ciphertexts[ ptext_index ]
             
            
            #GET THE DISTRIBUTION OF CIPHERTEXT AND PLAINTEXT GROUPED BY SHARED N_GRAM
            cipher_dist_n_gram = find_distribution_n_grams( decrypted_ciphertext , n_gram)
            grouped_n_gram_freq_cipher = get_grouped_n_grams_ordered_by_dec_freq(cipher_dist)
            grouped_n_gram_freq_plain = grouped_n_gram_freq_lists[ ptext_index ]

            #GET THE DISTRIBUTION OF PLAINTEXT GROUPED BY SHARED 2_GRAM
            grouped_2_gram_freq_plain = two_gram_freq_lists[ ptext_index ]

            #GET THE DISTRIBUTION OF PLAINTEXT GROUPED BY SHARED 1_GRAM
            grouped_1_gram_freq_plain = single_freq_lists[ ptext_index ]


            #get_grouped_n_gram_converter(grouped_n_gram_freq_cipher, grouped_n_gram_freq_plain, grouped_2_gram_freq_plain, ordered_1_gram_plain)
            n_gram_converter = get_grouped_n_gram_converter(grouped_n_gram_freq_cipher, grouped_n_gram_freq_plain, grouped_2_gram_freq_plain, grouped_1_gram_freq_plain)

            map_two_distributions(n_gram_converter, decrypted_ciphertext)

    
    
    return [ convert_list_chars_to_string( decrypted_ciphertext ) for decrypted_ciphertext in decrypted_ciphertexts ]
'''
5) Decrypt_ciphertext(key, ciphertext):
Given the key and ciphertext, decrypt ciphertext and return the plaintext out of 5 given with the smallest edit distance away from the decrypted ciphertext
=> changed to get_most_similar_plaintext(decrypted_ciphertexts)
'''

def calc_edit_distance(decrypted_ciphertext, plaintext):
    distance = 0
    for i in range(len(decrypted_ciphertext)):
        distance += decrypted_ciphertext[i] != plaintext[i]
    return distance

def get_most_similar_plaintext(decrypted_ciphertexts):
    plain_texts = [ plain_text1, plain_text2, plain_text3,
        plain_text4, plain_text5 ]
    costs = [calc_edit_distance(decrypted_ciphertexts[i], plaintexts[i]) for i in range(5) ]
    return plain_texts[costs.index(min(costs))]
    

