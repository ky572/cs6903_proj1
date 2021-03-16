from collections import defaultdict

import random

'''
I have combined 4) and 5)
now 4)decrypt_key returns 5 decrypted cipher text
'''
global plain_text1, plain_text2, plain_text3, plain_text4, plain_text5, alphabet
global plain_text_1, plain_text_2, plain_text_3, plain_text_4, plain_text_5, words

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

class Decrypter:

    def __init__(self):
        global plain_text1, plain_text2, plain_text3, plain_text4, plain_text5, alphabet
        global plain_text_1, plain_text_2, plain_text_3, plain_text_4, plain_text_5, words

        plain_text_1 = self.convert_string_to_vec_chars(plain_text1)
        plain_text_2 = self.convert_string_to_vec_chars(plain_text2)
        plain_text_3 = self.convert_string_to_vec_chars(plain_text3)
        plain_text_4 = self.convert_string_to_vec_chars(plain_text4)
        plain_text_5 = self.convert_string_to_vec_chars(plain_text5)
        
        # print(plain_text1)

    #1
    def convert_string_to_vec_chars(self, string):
        return list(string)
    
    #2
    #PYTHON STRING IS IMMUTABLE SO USE LIST OF CHARACTERS INSTEAD
    '''
    text could be str or list of chars
    '''
    def find_distribution_n_grams(self, text, n_gram, start = 0, t = 1):
        dist = defaultdict(lambda : 0)
        # print(len(text), text, n_gram, start, t)
        for i in range(start, len(text) - n_gram + 1, t):
            chars = text[i: i + n_gram]
            # print(chars)
            if isinstance(chars, list): #use string for keys in dictionaries
                chars = self.convert_list_chars_to_string(chars)
            dist[chars] += 1
        return dist

    #3
    def get_terms_ordered_by_dec_freq(self, dist):
        n_gram_list = []
        for key in dist:
            n_gram_list.append(key)
        n_gram_list.sort(key=lambda n_gram: -dist[n_gram])
        return n_gram_list

    #4
    #each group is defined by shared_n_gram
    #so group = shared_n_gram
    #make sure this is list of strings

    def get_grouped_n_grams_ordered_by_dec_freq(self, dist):
        n_gram_list = defaultdict(lambda: [])
        for key in dist:
            shared_n_gram = key[:-1]
            n_gram_list[ shared_n_gram ].append(key)
        for group in n_gram_list:
            n_gram_list[ group ].sort(key=lambda n_gram: -dist[n_gram])
        return n_gram_list

    
    '''
    CHECK FOR WHEN THERE ARE NOT ENOUGH CHARS IN PLAINTEXT
    '''

    #5
    #make sure key is string
    def get_n_gram_converter(self, ordered_n_gram_cipher, ordered_n_gram_plain):
        n_gram_converter = defaultdict()
        for i in range(len(ordered_n_gram_cipher)):
            n_gram_term = ordered_n_gram_cipher[i]
            index = i
            if index >= len(ordered_n_gram_plain):
                index = len(ordered_n_gram_plain) - 1
            n_gram_converter[ n_gram_term ] = ordered_n_gram_plain[ index ]
        return n_gram_converter

    #6
    #decrypted_ciphertext is a list of chars
    #so make sure modify it by a sublist not string

    def map_two_distributions(self, n_gram_converter, decrypted_ciphertext, start, t, n_gram):

        for i in range(start, len(decrypted_ciphertext) - n_gram + 1, t):
            n_gram_term_lst = decrypted_ciphertext[ i: i + n_gram]
            n_gram_term = self.convert_list_chars_to_string(n_gram_term_lst)
            decrypted_n_gram = n_gram_converter[ n_gram_term ]
            if isinstance(decrypted_n_gram, str):
                decrypted_n_gram = self.convert_string_to_vec_chars(decrypted_n_gram)
            decrypted_ciphertext[ i: i + n_gram] = n_gram_converter[ n_gram_term ]

    #7
    def concate_2_defaultdict(self, org_dict, add_dict):
        for key,val in add_dict.items():
            org_dict[ key ] = val

    #8
    def convert_list_chars_to_string(self,lst):
        return "".join(lst)

    #9
    def change_char_at(self, string, index, char):
        return string[:index] + char + string[index+1:]

    #10
    '''
    shared_n_gram_group: string 
    grouped_n_gram_freq_cipher: defaultdict (key, val): (str, ordered list of n_gram terms)
    grouped_n_gram_freq_plain: defaultdict (key, val): (str, ordered list of n_gram terms)
    n_gram_converter: defaultdict (key, val): (str, str)
    '''
    def try_1_edit_distance_away_groups(self, shared_n_gram_group, grouped_n_gram_freq_cipher, grouped_n_gram_freq_plain, n_gram_converter):
        
        #Try each possible 1 edit distance away
        for i in range(len(shared_n_gram_group)):
            
            #try to replace char with any letter in alphabet
            for char in alphabet:
                
                new_shared_n_gram_group = self.change_char_at(shared_n_gram_group, i, char)

                #If the new shared_group is present in plaintext
                #map frequency of original group in ciphertext
                #with this new shared_group in plaintext
                if new_shared_n_gram_group in grouped_n_gram_freq_plain:
                    ordered_n_gram_cipher = grouped_n_gram_freq_cipher[ shared_n_gram_group ]
                    ordered_n_gram_plain = grouped_n_gram_freq_plain[ new_shared_n_gram_group ]
                    n_gram_converter_for_curr_group = self.get_n_gram_converter(ordered_n_gram_cipher, ordered_n_gram_plain)
                    self.concate_2_defaultdict(n_gram_converter, n_gram_converter_for_curr_group)
                    print(f'succeeded decoding group {shared_n_gram_group} using group {new_shared_n_gram_group} using try_1_edit_distance_away_groups.')
                    print(f'Len(plain_text_dist[group]: {len(ordered_n_gram_plain)}, Len(cipher_text_dist[group]: {len(ordered_n_gram_cipher)},')
                    return True
        return False

    #11
    '''
    2 grams are grouped by a single letter in front
    '''
    def try_decode_2_gram(self, shared_n_gram_group, grouped_n_gram_freq_cipher, grouped_2_gram_freq_plain, n_gram_converter):
        second_to_last_char = shared_n_gram_group[-2]
        shared_n_minus_1_group = shared_n_gram_group[:-1] 
        
        if second_to_last_char in grouped_2_gram_freq_plain:
            ordered_2_gram_cipher = grouped_n_gram_freq_cipher[ shared_n_gram_group ]
            ordered_2_gram_cipher = [ n_gram[-2:] for n_gram in ordered_2_gram_cipher ] #last 2 chars of n_gram is 2_gram to be decoded

            ordered_2_gram_plain = grouped_2_gram_freq_plain[ second_to_last_char ]

            two_gram_converter_for_curr_group = self.get_n_gram_converter(ordered_2_gram_cipher, ordered_2_gram_plain)

            for two_gram_cipher, two_gram_plain in two_gram_converter_for_curr_group.items():
                n_gram_cipher = shared_n_minus_1_group + two_gram_cipher
                if n_gram_cipher in n_gram_converter: #already decoded
                    continue
                n_gram_plain = shared_n_minus_1_group + two_gram_plain
                n_gram_converter[ n_gram_cipher ] = n_gram_plain

                print(f'succeeded decoding group {shared_n_gram_group} using group {n_gram_cipher} using try_decode_2_gram')
                print(f'Len(plain_text_dist[group]: {len(ordered_2_gram_plain)}, Len(cipher_text_dist[group]: {len(ordered_2_gram_cipher)},')
            return True

        return False

    #12
    #decode 1 last char of n_gram always work since
    #they don't depend on prefix and
    #only need to follow single letter distribution from the plaintext single letter distribution
    def try_decode_1_gram(self, shared_n_gram_group, grouped_n_gram_freq_cipher, ordered_1_gram_plain, n_gram_converter):
        ordered_1_gram_cipher = grouped_n_gram_freq_cipher[ shared_n_gram_group ]
        ordered_1_gram_cipher = [ n_gram[-1] for n_gram in ordered_1_gram_cipher ] #only decode last single char not in shared_n_gram_group
        one_gram_converter_for_curr_group = self.get_n_gram_converter(ordered_1_gram_cipher, ordered_1_gram_plain)

        for one_gram_cipher, one_gram_plain in one_gram_converter_for_curr_group.items():
            n_gram_cipher = shared_n_gram_group + one_gram_cipher
            if n_gram_cipher in n_gram_converter:# already decoded similar term
                continue
            n_gram_plain = shared_n_gram_group + one_gram_plain
            n_gram_converter[ n_gram_cipher ] = n_gram_plain
            print(f'succeeded decoding group {shared_n_gram_group} using group {n_gram_cipher} using try_decode_1_gram')
            print(f'Len(plain_text_dist[group]: {len(ordered_1_gram_plain)}, Len(cipher_text_dist[group]: {len(ordered_1_gram_cipher)},')
            return True
        return False

    #13
    '''
    grouped_n_gram_freq_cipher: default dict
    grouped_n_gram_freq_plain: default dict
    grouped_2_gram_freq_plain: default dict
    ordered_1_gram_plain: list
    '''
    def print_dict(self, the_dict):
        for key, val in the_dict.items():
            print(f'({key}, {val})')

    def get_grouped_n_gram_converter(self, grouped_n_gram_freq_cipher, grouped_n_gram_freq_plain, grouped_2_gram_freq_plain, ordered_1_gram_plain):
        n_gram_converter = defaultdict()
        for shared_n_gram_group in grouped_n_gram_freq_cipher:
            # if shared_n_gram_group in n_gram_converter: #already decoded
            #     continue
            if shared_n_gram_group not in grouped_n_gram_freq_plain:
            
                if not self.try_1_edit_distance_away_groups(shared_n_gram_group, grouped_n_gram_freq_cipher, grouped_n_gram_freq_plain, n_gram_converter):
                    #try decode with 2 grams
                    if not self.try_decode_2_gram(shared_n_gram_group, grouped_n_gram_freq_cipher, grouped_2_gram_freq_plain, n_gram_converter):

                        #then try decode with 1 gram
                        if not self.try_decode_1_gram(shared_n_gram_group, grouped_n_gram_freq_cipher, ordered_1_gram_plain, n_gram_converter):
                            print(f'cannot decode {shared_n_gram_group}')
                            # self.print_dict(grouped_n_gram_freq_cipher)
                            # self.print_dict(grouped_n_gram_freq_plain)
                            # self.print_dict(grouped_2_gram_freq_plain)
                            # print(f'ordered_1_gram_plain: {ordered_1_gram_plain}')
            else:
                ordered_n_gram_cipher = grouped_n_gram_freq_cipher[ shared_n_gram_group ]
                ordered_n_gram_plain = grouped_n_gram_freq_plain[ shared_n_gram_group ]
                n_gram_converter_for_curr_group = self.get_n_gram_converter(ordered_n_gram_cipher, ordered_n_gram_plain)
                self.concate_2_defaultdict(n_gram_converter, n_gram_converter_for_curr_group)
                            
        return n_gram_converter
                
    def print_conversion(self, decrypted_text, plaintext, n_gram_converter, start, t, n_gram):
        for i in range(start, len(decrypted_text) - n_gram +1, t):
            cipher_n_gram_term = decrypted_text[i: i+n_gram]
            if isinstance(cipher_n_gram_term, list):
                cipher_n_gram_term = self.convert_list_chars_to_string(cipher_n_gram_term)
            print(f'{cipher_n_gram_term}: ({n_gram_converter[cipher_n_gram_term]}, {plaintext[i:i+n_gram]})')
    #14
    def decrypt_key(self, t, ciphertext, n_gram = 2):

        #calculate distribution of plaintext1
        dists =  [ defaultdict(lambda : 0) for i in range(5) ]
        single_dists = [ defaultdict(lambda : 0) for i in range(5) ]
        two_gram_dists = [ defaultdict(lambda : 0) for i in range(5) ]

        #transform to list of characters for later modification
        ciphertext_lst = self.convert_string_to_vec_chars(ciphertext)

        #list of immutable string of 5 plaintexts
        plain_texts = [ plain_text1, plain_text2, plain_text3,
            plain_text4, plain_text5 ]

        for plaintext_dist_index in range(5):
            text = plain_texts[plaintext_dist_index]
            dists[ plaintext_dist_index ] = self.find_distribution_n_grams(text, n_gram)
            single_dists[ plaintext_dist_index ] = self.find_distribution_n_grams(text, 1)
            two_gram_dists[ plaintext_dist_index ] = self.find_distribution_n_grams(text, 2)
        
        
        #create a list of n_grams for each plaintext distribution
        #in the order of highest frequency to lowest frequency
        n_gram_freq_lists = []
        for dist in dists:
            n_gram_list = self.get_terms_ordered_by_dec_freq(dist) #return a list of ONE distribution
            n_gram_freq_lists.append(n_gram_list)
        
        
        #create a list of n_grams for each plaintext distribution
        #in the order of highest frequency to lowest frequency
        #grouped by shared_n_gram

        grouped_n_gram_freq_lists = []
        for dist in dists:
            n_gram_list = self.get_grouped_n_grams_ordered_by_dec_freq(dist) #return a dictionary of distributions with common prefix
            grouped_n_gram_freq_lists.append(n_gram_list)

        #only fill 2 grams if n_gram > 2
        two_gram_freq_lists = []
        if n_gram > 2:
            for dist in two_gram_dists:
                two_gram_freq_list = self.get_grouped_n_grams_ordered_by_dec_freq(dist) #return a dictionary of distributions with common prefix
                two_gram_freq_lists.append(two_gram_freq_list)
        else:
            two_gram_freq_lists = grouped_n_gram_freq_lists
        
        #SINGLE FREQ LISTS, n_gram = 1
        #USEFUL FOR RANDOM CASE
        single_freq_lists = []

        if n_gram == 1:
            single_freq_lists = n_gram_freq_lists
        else:
            for dist in single_dists:
                single_freq_list = self.get_terms_ordered_by_dec_freq(dist) #return a list of ONE distribution
                single_freq_lists.append(single_freq_list)
        
        decrypted_ciphertexts = [ ciphertext_lst.copy() for i in range(5) ]
        #decrypt from first to t - n_gram + 1 distributions

        for start in range( t - n_gram + 1):
            # print()
            # print("=================================================")
            # print(f'======================== decoding {start}th distribution ==============')
            ##decrypt without prefix
            if start == 0:
                
                cipher_dist = self.find_distribution_n_grams( ciphertext , n_gram, start, t)
        
                ordered_n_gram_cipher = self.get_terms_ordered_by_dec_freq(cipher_dist)

                # print('cipher_dist')
                # self.print_dict(cipher_dist)
                # print(f'ciphertext: {ciphertext}')
                
                for ptext_index in range(5):

                    # print(f'decoding for plaintext number {ptext_index+1} ')

                    ordered_n_gram_plain = n_gram_freq_lists[ ptext_index ]
                    # print(f"ordered_n_gram_cipher: {ordered_n_gram_cipher}")
                    # print(f"ordered_n_gram_plain: {ordered_n_gram_plain}")
                    n_gram_converter = self.get_n_gram_converter( ordered_n_gram_cipher, ordered_n_gram_plain)
                    # self.print_conversion(decrypted_ciphertexts[ ptext_index ], plain_texts[ptext_index], n_gram_converter, start, t, n_gram)
                    self.map_two_distributions( n_gram_converter, decrypted_ciphertexts[ ptext_index ], start, t, n_gram)

            else:

                #CASE 2
                #get the distribution of 5 plaintexts, except the decrypted possibilities
                #according to a shared portion of the n_gram

                #decrypt with n-1 prefix
                for ptext_index in range(5):
                    
                    # print(f'decoding for plaintext number {ptext_index+1} ')

                    #GET THE PLAIN DISTRIBUTION OF CIPHERTEXT
                    decrypted_ciphertext  = decrypted_ciphertexts[ ptext_index ]
                    
                    
                    #GET THE DISTRIBUTION OF CIPHERTEXT AND PLAINTEXT GROUPED BY SHARED N_GRAM
                    #can be modified to only get start-th distribution of plaintext
                    cipher_dist_n_gram = self.find_distribution_n_grams( decrypted_ciphertext , n_gram, start, t)
                    grouped_n_gram_freq_cipher = self.get_grouped_n_grams_ordered_by_dec_freq(cipher_dist_n_gram)
                    grouped_n_gram_freq_plain = grouped_n_gram_freq_lists[ ptext_index ]

                    #GET THE DISTRIBUTION OF PLAINTEXT GROUPED BY SHARED 2_GRAM
                    grouped_2_gram_freq_plain = two_gram_freq_lists[ ptext_index ]

                    #GET THE DISTRIBUTION OF PLAINTEXT GROUPED BY SHARED 1_GRAM
                    ordered_1_gram_plain = single_freq_lists[ ptext_index ]


                    #different n_gram_converter for each different distribution
                    #get_grouped_n_gram_converter(grouped_n_gram_freq_cipher, grouped_n_gram_freq_plain, grouped_2_gram_freq_plain, ordered_1_gram_plain)
                    n_gram_converter = self.get_grouped_n_gram_converter(grouped_n_gram_freq_cipher, grouped_n_gram_freq_plain, grouped_2_gram_freq_plain, ordered_1_gram_plain)
                    
                    # print('n_gram_converter')
                    # self.print_dict(n_gram_converter)
                    # print('grouped_n_gram_freq_cipher')
                    # self.print_dict(grouped_n_gram_freq_cipher)
                    # print('grouped_n_gram_freq_plain')
                    # self.print_dict(grouped_n_gram_freq_plain)

                    # self.print_conversion(decrypted_ciphertexts[ ptext_index ], plain_texts[ptext_index], n_gram_converter, start, t, n_gram)
                    self.map_two_distributions(n_gram_converter, decrypted_ciphertext, start, t, n_gram)

                # self.print_dict(n_gram_converter)
                
            # print("=================================================")
            # print()

        return [ self.convert_list_chars_to_string( decrypted_ciphertext ) for decrypted_ciphertext in decrypted_ciphertexts ]
    '''
    5) Decrypt_ciphertext(key, ciphertext):
    Given the key and ciphertext, decrypt ciphertext and return the plaintext out of 5 given with the smallest edit distance away from the decrypted ciphertext
    => changed to get_most_similar_plaintext(decrypted_ciphertexts)
    '''

    #15
    def calc_edit_distance(self, decrypted_ciphertext, plaintext):
        distance = 0
        com_length = min(len(decrypted_ciphertext), len(plaintext))
        for i in range(com_length):
            distance += decrypted_ciphertext[i] != plaintext[i]
        distance += len(decrypted_ciphertext) - com_length + len(plaintext) - com_length
        return distance

    #16
    def get_most_similar_plaintext(self, decrypted_ciphertexts, plain_texts):
        # plain_texts = [ plain_text1, plain_text2, plain_text3,
        #     plain_text4, plain_text5 ]
        costs = [ self.calc_edit_distance(decrypted_ciphertexts[i], plain_texts[i]) for i in range(len(plain_texts)) ]
        return plain_texts[ costs.index(min(costs)) ]

    #17 ------- to be finished -----------
    '''
    decrypt using 1 distribution of the words in dictionary, can decrypt with t distributions
    but each map to the same original distribution of the dictionary words
    '''
    def decrypt_type_two(self, t, ciphertext, n_gram):
        text = "".join(words)
        dist = self.find_distribution_n_grams(text, n_gram)
        two_gram_dist = self.find_distribution_n_grams(text, 2)
        one_gram_dist = self.find_distribution_n_grams(text, 1)

        n_gram_freq_list = self.get_terms_ordered_by_dec_freq(dist)
        grouped_n_gram_list = self.get_grouped_n_grams_ordered_by_dec_freq(dist)
        two_gram_list = self.get_grouped_n_grams_ordered_by_dec_freq(two_gram_dist)
        one_gram_list = self.get_terms_ordered_by_dec_freq(one_gram_dist)
        decrypted_ciphertext = self.convert_string_to_vec_chars(ciphertext)
        for start in range(t):
        #     print()
        #     print("=================================================")
        #     print(f'======================== decoding {start}th distribution ==============')

            if start == 0:
                #decrypt without prefix
                cipher_dist = self.find_distribution_n_grams( decrypted_ciphertext , n_gram, start, t)
        
                ordered_n_gram_cipher = self.get_terms_ordered_by_dec_freq(cipher_dist)

                ordered_n_gram_plain = n_gram_freq_list
                n_gram_converter = self.get_n_gram_converter( ordered_n_gram_cipher, ordered_n_gram_plain)
                self.map_two_distributions( n_gram_converter, decrypted_ciphertext, start, t, n_gram)
            else:
                
                
                #GET THE DISTRIBUTION OF CIPHERTEXT AND PLAINTEXT GROUPED BY SHARED N_GRAM
                #can be modified to only get start-th distribution of plaintext
                cipher_dist_n_gram = self.find_distribution_n_grams( decrypted_ciphertext , n_gram, start, t)
                grouped_n_gram_freq_cipher = self.get_grouped_n_grams_ordered_by_dec_freq(cipher_dist_n_gram)
                grouped_n_gram_freq_plain = grouped_n_gram_list

                #GET THE DISTRIBUTION OF PLAINTEXT GROUPED BY SHARED 2_GRAM
                grouped_2_gram_freq_plain = two_gram_list

                #GET THE DISTRIBUTION OF PLAINTEXT GROUPED BY SHARED 1_GRAM
                ordered_1_gram_plain = one_gram_list


                #different n_gram_converter for each different distribution
                #get_grouped_n_gram_converter(grouped_n_gram_freq_cipher, grouped_n_gram_freq_plain, grouped_2_gram_freq_plain, ordered_1_gram_plain)
                n_gram_converter = self.get_grouped_n_gram_converter(grouped_n_gram_freq_cipher, grouped_n_gram_freq_plain, grouped_2_gram_freq_plain, ordered_1_gram_plain)
                # print('n_gram_converter')
                # self.print_dict(n_gram_converter)
                self.map_two_distributions(n_gram_converter, decrypted_ciphertext, start, t, n_gram)
            # self.print_dict(n_gram_converter)
            # print("=================================================")
            # print()
        
        return self.correct_type_two_decrytion(self.convert_list_chars_to_string(decrypted_ciphertext))


    #18
    '''
    decrypted_text: str
    start_index: int

    Return:
    chose_word: list of chars
    '''
    def get_most_likely_word(self, decrypted_text, start_index):
        min_distance = float('inf')
        chose_word = None
        
        for word in words:
            end_index = min(start_index + len(word), len(decrypted_text) )
            distance = self.calc_edit_distance(word, decrypted_text[ start_index : end_index])
            if distance < min_distance:
                min_distance = distance
                chose_word = word
        return list(chose_word)

    #19
    '''
    decrypted_text: str
    Return:
    corrected_decryption: str
    '''
    def correct_type_two_decrytion(self, decrypted_text):
        corrected_decryption = []
        index = 0
        decrypted_text_length = len(decrypted_text)
        while index < decrypted_text_length:
            next_word = self.get_most_likely_word( decrypted_text, index )
            corrected_decryption.extend( next_word )
            index += len(next_word)
        
        if len(corrected_decryption) > 0 and corrected_decryption[-1] == ' ':
            corrected_decryption.pop()
        
        #fix words so that decrypted text has exact L length
        #to be finished

        return self.convert_list_chars_to_string(corrected_decryption)


# if __name__ == "__main__":
#     decrypter = Decrypter()
    # print(plain_text1)

