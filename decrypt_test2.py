from decrypt_2 import *
import time
import random
from collections import defaultdict
from copy import deepcopy



class TrieNode:
    def __init__(self):
        self.children = defaultdict(lambda: None)
        self.word = None
class Trie:
    
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word, real_word):
        curr = self.root
        for i in range(len(word)):
            char = word[i]
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
            i+=1
        curr.word = real_word

    def print_trie(self):
        curr = self.root
        next_nodes = []
        curr_nodes = [curr]
        while len(curr_nodes) > 0:
            for node in curr_nodes:
                
                for child in node.children:
                    print(child, end=" ")
                    next_nodes.append(node.children[child])
                if len(node.children):
                    print()
            curr_nodes = next_nodes
            next_nodes = []
        
    def get_word(self, text, start_pos):
        curr = self.root
        for i  in range(start_pos, len(text)):
            char = text[i]
            if char not in curr.children:
                return 
            curr = curr.children[char]
            if curr.word:
                return curr.word


class Decryption:
    def __init__(self, t):
        self.t = t
        self.decryption = []
        self.num_random = 0
        self.max_random_chars = 50

    def add_rand(self, val):
        self.num_random += val
        self.num_random = min(self.num_random, self.max_random_chars)

    def add_word(self, pos, word):
        self.decryption.append((pos, word))
    
    def add_words(self, decoded_lst):
        self.decryption.extend(decoded_lst)

class Decrypt_test2(Decrypter_2):
    
    def __init__(self, root = None, allow_slack = False, max_random_chars = 50):
        super().__init__()
        words_freq = defaultdict(lambda: 0)
        for word in words:
            words_freq[len(word)] += 1
        words.sort(key = lambda x : -words_freq[x])
        self.max_key_length = 24
        self.max_prev_decryptions = 40
        self.allow_slack = allow_slack
        self.trie = self.add_words_in_dict()
        self.max_random_chars = max_random_chars
        
    
    def add_words_in_dict(self):
        trie = Trie()
        for word in words:
            if self.allow_slack:
                for i in range(len(word)):
                    for char1 in alphabet[:-1]:
                        for j in range(i+1, len(word)):
                            for char in alphabet[:-1]:
                                new_word = word[:i] + char1 + word[i+1:j] + char + word[j+1:]
                                trie.add_word(new_word, word)
            else:
                trie.add_word(word, word)
        return trie

    def get_key(self, ciphertext, plaintext, start, end):
       
        key_lst = []
        for i in range(start, end):
            key_distance =  self.letter_to_index[ ciphertext[i] ]  - self.letter_to_index[ plaintext[i - start] ] 
            if key_distance < 0:
                key_distance += len(alphabet)
            key_distance %= len(alphabet)
            key_lst.append( key_distance )
        return key_lst
    
    def get_words_from_decryption(self, decryption, start_pos = 0):
        all_words = []
        i = 0
        while i < len(decryption):
            word = self.trie.get_word(decryption, i)
            if word:
                all_words.append((start_pos + i, word + ' '))
                i += len(word)
            else:
                i+=1
        return all_words

    # def generate_words
    def find_best_decryption(self, decryptions):
        max_length = max([len(decryptions[i].decryption) for i in range(len(decryptions))])
        # print(f'max_length: {max_length}')
        num_of_max_decryptions = 0
        min_dup = float('inf')
        best_decryption = None
        # best_length = None
        for decryption_pair in decryptions:

            decryption = decryption_pair.decryption
            t = decryption_pair.decryption
        
            num_of_max_decryptions += 1
            dec = []
            num_dup = 0
            size = 0
            decrypted_length = 0
            for decrypted in decryption:
                
                if size < decrypted[0]:
                    dec.append((size,' '*(decrypted[0]-size))) #empty string for not decrypted words
                    size = decrypted[0]
                    
                size += len(decrypted[1])
                dec.append(decrypted)
                decrypted_length += len(decrypted[1])

            decrypted_length -= 1
            if best_decryption == None or len(best_decryption) < len(dec) or\
                ( len(best_decryption) < len(dec) and num_dup < min_dup ):
                min_dup = num_dup
                best_decryption = dec
                best_num_words = len(decryption)
                # best_length = decrypted_length

        #can even check for key pattern 
        # print(best_decryption)
        return " ".join([ decryption[1][:-1]  for decryption in best_decryption]) if best_decryption else ""

    def remove_dup(self, decryptions, new_decryptions, best_decryption_pair):
       
        #remove duplicate for each new_decryptions

        for decryption in new_decryptions:
            t = decryption.t
            new_decryption = []
            for word_pair in decryption.decryption:
                if len(new_decryption) == 0 or word_pair != new_decryption[-1]:
                    new_decryption.append(word_pair)

            new_decrypted = Decryption(t)
            new_decrypted.add_words(new_decryption)
            if best_decryption_pair == None or len(best_decryption_pair.decryption) < len(new_decryption):
                best_decryption_pair = new_decrypted
            
            decryptions.append(new_decrypted)

        decryptions.sort(key=lambda x: -len(x.decryption))

        return best_decryption_pair

    def decrypt_first_two(self, ciphertext, best_decryption_pair=None, max_random_chars = 50):
        max_random_chars = self.max_random_chars
        start_time = time.time()
        #each is pair of ( key_repetion, list of pairs of (pos, word) )
        decryptions = set()
        #first run 40*40*12*50*500
        for first_word in words:
            for second_word in words:
                curr_decrypt_length = len(first_word) + len(second_word) + 2
                
                plaintext = first_word+' ' + second_word + ' '
                key = self.get_key(ciphertext, plaintext, 0, len(plaintext))
                best_decrypted = None
                for t in range(1,self.max_key_length+1):

                    key_copy = key[: t]
                    decryption = Decryption(t)
                    decryption.add_word(0, first_word+' ')
                    decryption.add_word(len(first_word)+1, second_word + ' ')

                    for i in range(curr_decrypt_length, len(ciphertext), t):
                        best_shift = None
                        shift_num = None
                        remain_ran = max_random_chars - decryption.num_random
                        for shift in range(remain_ran+1):
                        
                            start_pos = i + shift
                            curr_decoded = self.decode(ciphertext, key_copy, start_pos)
                            words_from_decoded = self.get_words_from_decryption(curr_decoded, start_pos)
                            if best_shift == None or len(words_from_decoded) > len(best_shift):
                                best_shift = words_from_decoded
                                shift_num = shift
                            
                        if best_shift != None:
                            decryption.add_words(best_shift)
                            decryption.add_rand(shift_num)

                    # if len(decryption.decryption) == 2:
                    #     continue

                    if best_decrypted == None or len(decryption.decryption) > len(best_decrypted.decryption):
                        best_decrypted = decryption

                    if best_decryption_pair == None or len(best_decryption_pair.decryption) < len(decryption.decryption):
                        best_decryption_pair = decryption
                if best_decrypted != None:
                    # decryptions.append(best_decrypted)
                    decryptions.add(best_decrypted)
                    

        decryptions = list(decryptions)      
        if len(decryptions) > self.max_prev_decryptions:
            decryptions.sort(key=lambda x: -len(x.decryption))

        decryptions = decryptions[:self.max_prev_decryptions]
        end_time = time.time()
        # pairs = set()
        
        # for decryption in decryptions:
        #     print(decryption.decryption[0][1] + decryption.decryption[1][1], len(decryption.decryption))
        #     pairs.add(( decryption.decryption[0][1], decryption.decryption[1][1]) ) 
        # for pair in pairs:
        #     print(pair)

#        print(f'decrypt_first_two: {len(decryptions)}, time passed: {end_time - start_time}')
        return decryptions, best_decryption_pair
    
    def decrypt_third(self, ciphertext, decryptions, best_decryption_pair, max_random_chars=50):
        max_random_chars = self.max_random_chars
        start_time = time.time()
        new_decryptions = set()
        decryptions_less_than_two_words_3 = 0

        #limit to x=40 decryptions to keep run time limit to
        #40*x*11 * 50 *500
        for decryption_template in decryptions:
            t = decryption_template.t
            if t == None or decryption_template == None:
                # print(f'decrypt_third, Error: t: {t==None}, decryption: {decryption_template==None}')
                continue
            for third_word in words:
                

                first_two_word_length = decryption_template.decryption[1][0] +  len(decryption_template.decryption[1][1])
               
                #all decryptions must currently have more than 2 words
                if len(decryption_template.decryption) > 2:
                    if len(third_word) + 1 + first_two_word_length > decryption_template.decryption[2][0]:
                        # new_decryptions.append(decryption_template)
                        new_decryptions.add(decryption_template)
                        # continue #cannot fit
                else:
                    decryptions_less_than_two_words_3 += 1

                remain_start = max_random_chars - decryption_template.num_random
                if remain_start == 0:
                    t_range = (1,25)
                else:
                    t_range = (t, t+1)

                for t in range(t_range[0], t_range[1]):
                    decryption = deepcopy(decryption_template)
                    best_decoded = None
                    
                    for start_random in range(remain_start+1):
                        start_third = first_two_word_length + start_random
                        end_third = start_third + len(third_word) + 1
                        third_decoded = [(start_third, third_word)]
                        if len(decryption.decryption) > 2 and end_third > decryption.decryption[2][0]:
                            break #break as early as possible
                        plaintext = third_word + ' '
                        key_third = self.get_key(ciphertext, plaintext, start_third, end_third)
                        start_second = decryption.decryption[1][0]
                        plaintext = decryption.decryption[1][1]
                        end_second = start_second + len(decryption.decryption[1][1]) 
                        key_prev = self.get_key(ciphertext, plaintext, start_second, end_second)
                        key = key_prev + key_third # skip random characters between second and third
                    
                        decoded_lst = []
                        num_random = 0
                        for i in range(end_third, len(ciphertext), t):
                        
                            best_shift = None
                            shift_num = None
                            remain_ran = max_random_chars - start_random - num_random
                            for end_random in range(remain_ran + 1):

                                start_pos = i + end_random
                                curr_decoded = self.decode(ciphertext, key, start_pos)
                                words_from_decoded = third_decoded + self.get_words_from_decryption(curr_decoded, start_pos)
                                if best_shift == None or len(words_from_decoded) > len(best_shift):
                                    best_shift = words_from_decoded
                                    shift_num = end_random
                                    
                            if best_shift != None:
                                decoded_lst.extend(best_shift)
                                num_random += shift_num

                        if(len(decoded_lst)) == 0:
                            continue
                        if best_decoded == None or len(best_decoded) < len(decoded_lst):
                            best_decoded = decoded_lst
                                

                    if best_decoded != None:
                        decryption.add_words(best_decoded)
                        decryption.add_rand(num_random)
                    
                    # new_decryptions.append(decryption)
                    decryption.decryption.sort(key=lambda x: x[0])
                    new_decryptions.add(decryption)
                #############

        new_decryptions = list(new_decryptions)
        decryptions = []
        best_decryption_pair = self.remove_dup(decryptions, new_decryptions, best_decryption_pair)
        decryptions = decryptions[:self.max_prev_decryptions]
        end_time = time.time()
#        print(f'decrypt_third: {len(decryptions)}, time passed: {end_time - start_time}')
#        print(f'Before decrypting third word, decryptions_less_than_two_words: {decryptions_less_than_two_words_3}')
        return decryptions, best_decryption_pair

    def decrypt_fourth(self, ciphertext, decryptions, best_decryption_pair, max_random_chars=50):
        max_random_chars = self.max_random_chars
        start_time = time.time()
        new_decryptions = set()

        decryptions_less_than_two_words = 0
        decryptions_less_than_3_words = 0

        #limit to x=40 decryptions to keep run time limit to
        #40*x*11 * 50 *500
    
        for decryption_template in decryptions:
            t = decryption_template.t
            if t == None or decryption_template == None:
                # print(f'decrypt_fourth, Error: t: {t==None}, decryption: {decryption_template==None}')
                continue
            for fourth_word in words:
                # decryption = decryption_template.copy()
                
                
                first_3_word_length = decryption_template.decryption[1][0] +  len(decryption_template.decryption[1][1])
               
                if len(decryption_template.decryption) > 2 :
                    first_3_word_length += decryption_template.decryption[2][0]
                    
                else: 
                    decryptions_less_than_two_words += 1
                    # continue

                
                   
                #all decryptions must currently have more than 3 words
                #but don't make this a harsh constraint
                if len(decryption_template.decryption) > 3:
                    
                    #but for sanity check
                    if len(fourth_word) + 1 + first_3_word_length > decryption_template.decryption[3][0]:
                        # new_decryptions.append(decryption_template)
                        new_decryptions.add(decryption_template)
                        # continue #cannot fit
                else:
                    decryptions_less_than_3_words += 1
                    # continue

                best_decoded = None
                
                #can reduce run time by checking num random chars
                #from prev decryption but that does not help
                #complexity much so ...
                remain_start = max_random_chars - decryption_template.num_random
                if remain_start == 0:
                    t_range = (1,25)
                else:
                    t_range = (t, t+1)
                for t in range(t_range[0], t_range[1]):
                    decryption = deepcopy(decryption_template)
                    for start_random in range(remain_start+1):
                        start_fourth = first_3_word_length + start_random
                        end_fourth = start_fourth + len(fourth_word) + 1
                        fourth_decoded = [(start_fourth, fourth_word)]
                        if len(decryption.decryption) > 3 and end_fourth > decryption.decryption[3][0]:
                            break #break as early as possible
                        plaintext = fourth_word + ' '
                        key_third = self.get_key(ciphertext, plaintext, start_fourth, end_fourth)
                        last_word_index = 2 if len(decryption.decryption) > 2 else 1
                        start_third = decryption.decryption[last_word_index][0]
                        plaintext = decryption.decryption[last_word_index][1] 
                        end_third = start_third + len(decryption.decryption[2][1])
                        key_prev = self.get_key(ciphertext, plaintext, start_third, end_third)
                        key = key_prev + key_third # skip random characters between second and third

                        decoded_lst = []
                        num_random = 0
                        for i in range(end_fourth, len(ciphertext), t):
                        
                            best_shift = None
                            shift_num = None
                            remain_ran = max_random_chars - num_random - start_random
                            for end_random in range( remain_ran + 1 ):

                                start_pos = i + end_random
                                curr_decoded = self.decode(ciphertext, key, start_pos)
                                words_from_decoded = fourth_decoded + self.get_words_from_decryption(curr_decoded, start_pos)
                                
                                if best_shift == None or len(words_from_decoded) > len(best_shift):
                                    best_shift = words_from_decoded
                                    shift_num = end_random

                            if best_shift != None:
                                decoded_lst.extend(best_shift)
                                num_random += shift_num

                        if(len(decoded_lst)) == 0:
                            continue
                        if best_decoded == None or len(best_decoded) < len(decoded_lst):
                            best_decoded = decoded_lst

                    
                    if best_decoded != None:
                        decryption.add_words(best_decoded)
                        decryption.add_rand(num_random)
                    
                    # new_decryptions.append(decryption)
                    decryption.decryption.sort(key=lambda x: x[0])
                    new_decryptions.add(decryption)
                ##############

        new_decryptions = list(new_decryptions)
        # print(len(new_decryptions))
        decryptions = []
        best_decryption_pair = self.remove_dup(decryptions, new_decryptions, best_decryption_pair)
        end_time = time.time()
#        print(f'decrypt_fourth: {len(decryptions)}, time passed: {end_time - start_time}')
#        print(f'Before decrypting fourth word, decryptions_less_than_two_words: {decryptions_less_than_two_words}')
#        print(f'Before decrypting fourth word, decryptions_less_than_three_words: {decryptions_less_than_3_words}')
        return decryptions, best_decryption_pair

    def decrypt(self, ciphertext, max_random_chars=50):
        self.max_random_chars = max_random_chars
        #first 2 words
        #constant of word length explode things up to 4.4*1e8 * 24 = 9 * 1e9 ~ 1e10
        decryptions, best_decryption_pair = self.decrypt_first_two(ciphertext)
        
        #third word
        decryptions, best_decryption_pair = self.decrypt_third(ciphertext, decryptions, best_decryption_pair)
        
        #fourth word
        decryptions, best_decryption_pair = self.decrypt_fourth(ciphertext, decryptions, best_decryption_pair)
        
        # print(f'Number of decryptions: {len(decryptions)}')
        if len(decryptions) == 0:
            decryptions = [best_decryption_pair]
        # decryption, best_length = self.find_best_decryption(decryptions)
        # return decryption, best_length/len(ciphertext)
        return self.find_best_decryption(decryptions)
