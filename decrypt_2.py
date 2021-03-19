from decrypter import *
from collections import defaultdict
from encryption_test import Cipher_Generator 

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


    




    

        