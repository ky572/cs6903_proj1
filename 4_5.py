from collections import defaultdict
'''
4) Decrypt_key(t, num_chars_per_entry_in_distribution, ciphertext):
Have distributions of 2 characters at a time
Given a key length t, generate t distributions
Compare distributions with english/ plaintext distributions and deduce the t shifts
Return these t shifts
'''

plain_text1 = "cabooses meltdowns bigmouth makework flippest neutralizers gipped mule antithetical imperials carom masochism stair retsina dullness adeste corsage saraband promenaders gestational mansuetude fig redress pregame borshts pardoner reforges refutations calendal moaning doggerel dendrology governs ribonucleic circumscriptions reassimilating machinize rebuilding mezcal fluoresced antepenults blacksmith constance furores chroniclers overlie hoers jabbing resigner quartics polishers mallow hovelling ch"

plain_text2 = "biorhythmic personalizing abjure greets rewashed thruput kashmir chores fiendishly combatting alliums lolly milder postpaid larry annuli codgers apostatizing scrim carillon rust grimly lignifying lycanthrope samisen founds millimeters pentagon humidification checkup hilts agonise crumbs rejected kangaroo forenoons grazable acidy duellist potent recyclability capture memorized psalmed meters decline deduced after oversolicitousness demoralizers ologist conscript cronyisms melodized girdles nonago"

plain_text3 = "hermitage rejoices oxgall bloodstone fisticuff huguenot janitress assailed eggcup jerseyites fetas leipzig copiers pushiness fesse precociously modules navigates gaiters caldrons lisp humbly datum recite haphazardly dispassion calculability circularization intangibles impressionist jaggy ascribable overseen copses devolvement permutationists potations linesmen hematic fowler pridefully inversive malthus remainders multiplex petty hymnaries cubby donne ohioans avenues reverts glide photos antiaci"

plain_text4 = "leonardo oxygenate cascade fashion fortifiers annelids co intimates cads expanse rusting quashing julienne hydrothermal defunctive permeation sabines hurries precalculates discourteously fooling pestles pellucid circlers hampshirites punchiest extremist cottonwood dadoes identifiers retail gyrations dusked opportunities ictus misjudge neighborly aulder larges predestinate bandstand angling billet drawbridge pantomimes propelled leaned gerontologists candying ingestive museum chlorites maryland s"

plain_text5 = "undercurrents laryngeal elevate betokened chronologist ghostwrites ombres dollying airship probates music debouching countermanded rivalling linky wheedled heydey sours nitrates bewares rideable woven rerecorded currie vasectomize mousings rootstocks langley propaganda numismatics foetor subduers babcock jauntily ascots nested notifying mountainside dirk chancellors disassociating eleganter radiant convexity appositeness axonic trainful nestlers applicably correctional stovers organdy bdrm insis"


def decrypt_key(t, n_gram, ciphertext):

    #calculate distribution of plaintext1
    dists =  [defaultdict(lambda : 0) for i in range(6)]
    plain_texts = [ plain_text1, plain_text2, plain_text3,
        plain_text4, plain_text5 ]
    for plaintext_dist_index in range(5):
        text = plain_texts[plaintext_dist_index]
        for i in range(len(text) - n_gram + 1):
            chars = text[i: i + n_gram]
            dists[plaintext_dist_index][chars] += 1
    
    
    #create a list of n_grams for each plaintext distribution
    #in the order of highest frequency to lowest frequency
    n_gram_lists = []
    for dist in dists:
        n_gram_list = []
        for key in dist:
            n_gram_list.append(key)
        n_gram_list.sort(lambda n_gram_1, n_gram_2: dist[n_gram_1] > dist[n_gram_2])
        n_gram_lists.append(n_gram_list)
    
    #t - n_gram + 1 distributions of ciphertext
    cipher_dists =  [ defaultdict(lambda : 0) for i in range(t - n_gram + 1) ]
    for start in range(t - n_gram + 1):
        for i in range(start, len(ciphertext) - n_gram + 1, t):
            chars = ciphertext[i: i + n_gram]
            cipher_dists[start][chars] += 1
    
    decrypted_ciphertext = [ ciphertext.copy() for i in range(5) ] 
    
    #decrypt from first to t - n_gram + 1 distributions

    for start in range( t - n_gram + 1):
        

        #if it's the first distribution, decrypt as normal
        if start == 0:
            cipher_dist = defaultdict(lambda : 0)
            #get the start_th distribution of ciphertext
            for i in range(start, len(ciphertext) - n_gram + 1, t):
                chars = ciphertext[i: i + n_gram]
                cipher_dist[chars] += 1
            
            #put all n_grams in ciphertext in order of their frequency 
            #highest to lowest
            #and map them to an index corresponding 
            #to their order 

            ordered_n_gram_by_freq = []
            for key in cipher_dist:
                ordered_n_gram_by_freq.append(key)
            
            ordered_n_gram_by_freq.sort(lambda n_gram1, n_gram2: cipher_dist[ n_gram1 ] >  cipher_dist[ n_gram2 ])

            n_gram_to_index = defaultdict()
            for i in range(len(ordered_n_gram_by_freq)):
                n_gram_term = ordered_n_gram_by_freq[i]
                n_gram_to_index[ n_gram_term ] = i

            for i in range(start, len(ciphertext) - n_gram + 1, t):
                for ptext_index in range(5):
                    n_gram_term = ciphertext[ptext_index][ i: i + n_gram]
                    n_gram_index = n_gram_to_index[ n_gram_term ]
                    decrypted_ciphertext[ptext_index][ i: i + n_gram] = n_gram_lists[ ptext_index ][n_gram_index]

            continue

        #get the distribution of 5 plaintexts, except the decrypted possibilities
        #according to a shared portion of the n_gram
        
        for ptext_index in range(5):
            
            ciphertext_to_use = decrypted_ciphertext[ptext_index]
            cipher_dist = defaultdict(lambda : 0)
            #get the start_th distribution of ciphertext
            for i in range(start, len(ciphertext_to_use) - n_gram + 1, t):
                chars = ciphertext_to_use[i: i + n_gram]
                cipher_dist[chars] += 1

            ordered_n_gram_by_freq = []
            for key in cipher_dist:
                ordered_n_gram_by_freq.append(key)
            
            ordered_n_gram_by_freq.sort(lambda n_gram1, n_gram2: cipher_dist[ n_gram1 ] >  cipher_dist[ n_gram2 ])


            ####TO BE REVIEWED
            n_gram_dist = defaultdict(lambda: [])
            n_gram_to_index = defaultdict()

            for n_gram_key in n_gram_list:
                shared_n_gram_portion  = n_gram_key[:-1]
                
                n_gram_dist[ shared_n_gram_portion ].append(n_gram_key)

            for i in range(len(ordered_n_gram_by_freq)): 
                n_gram_term = ordered_n_gram_by_freq[ i ]
                n_gram_to_index[ n_gram_key ] = len( n_gram_dist[ shared_n_gram_portion ] )

            ####TO BE REVIEWED

            for i in range(start, len(ciphertext) - n_gram + 1, t):
                
                n_gram_term = ciphertext[ptext_index][ i: i + n_gram]
                shared_portion_with_prev_n_gram = decrypted_ciphertext[ptext_index][ i: i + n_gram-1]
                n_gram_list = n_gram_dist[ shared_portion_with_prev_n_gram ]

                if n_gram_term not in n_gram_to_index:
                    
                n_gram_index = n_gram_to_index[ n_gram_term ]
                decrypted_n_gram = n_gram_list[ n_gram_index ]
                last_char_to_decrypt_non_shared = decrypted_n_gram[ -1 ]
                decrypted_ciphertext[ptext_index][ i + n_gram - 1] = last_char_to_decrypt_non_shared

        


    
    
'''
5) Decrypt_ciphertext(key, ciphertext):
Given the key and ciphertext, decrypt ciphertext and return the plaintext out of 5 given with the smallest edit distance away from the decrypted ciphertext
'''
