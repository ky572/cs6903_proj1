from decrypter import *
from encryption_test import Cipher_Generator 
from collections import defaultdict
import random

class Dectypter_Tester:

    def __init__(self):
        self.cipher_generator = Cipher_Generator()
        self.decrypter = Decrypter()
        # print(globals())
        # from decrypter import *
        # print(self.decrypter.plain_text1)
        random.seed()
        # global plain_text1, plain_text2, plain_text3, plain_text4, plain_text5, alphabet
        # global plain_text_1, plain_text_2, plain_text_3, plain_text_4, plain_text_5, words
        

    def run_tests(self):
        
        #ciphertext test:
        self.cipher_generator_test()

        #test decrypter's global variables
        print("plain_text1", plain_text1)
        print("plain_text2", plain_text2)
        print("plain_text3", plain_text3)
        print("plain_text4", plain_text4)
        print("plain_text5", plain_text5)


        # print("plain_text_1", plain_text_1)
        # print("plain_text_2", plain_text_2)
        # print("plain_text_3", plain_text_3)
        # print("plain_text_4", plain_text_4)
        # print("plain_text_5", plain_text_5)

        print("alphabet", alphabet)
        print("words", words)

        #test for 1
        self.convert_string_to_vec_chars_tester("hello world")

        #test for 2
        self.find_distribution_n_grams_tester()

        #test for 3
        self.get_terms_ordered_by_dec_freq_tester()

        #test for 4
        self.get_grouped_n_grams_ordered_by_dec_freq_tester()

        #test for 5
        self.get_n_gram_converter_tester()

        #test for 6
        self.map_two_distributions_tester()

        #test for 7
        self.concate_2_defaultdict_tester()

        #test for 8
        self.convert_list_chars_to_string_tester()

        #test for 9
        self.change_char_at_tester()

        #test for 10
        # self.try_1_edit_distance_away_groups_tester()

        #test for 11
        # self.try_decode_2_gram_tester()

        #test for 12
        # self.try_decode_1_gram_tester()

        #test for 13
        self.get_grouped_n_gram_converter_tester()

        #test for 14
        self.decrypt_key_tester()

        #test for 15
        self.calc_edit_distance_tester()

        #test for 16
        self.get_most_similar_plaintext_tester()

        #test for 17
        self.decrypt_type_two_tester()

        #test for 18
        self.get_most_likely_word_tester()

        #test for 19
        self.correct_type_two_decrytion_tester()



    def cipher_generator_test(self):
        print()
        print("===========================================================================")
        print("================ TEST FOR Cipher_Generator =====================")
        self.cipher_generator.generate_cipher(plain_text1)
        self.cipher_generator.generate_cipher(plain_text1, 5, True, 20)
        plaintext_test2 = self.cipher_generator.generate_test2(50)
        print('plaintext_test2:')
        print(plaintext_test2)
        print("===========================================================================")
        print()

    #test for 1
    def convert_string_to_vec_chars_tester(self, string):
        converted_string = self.decrypter.convert_string_to_vec_chars(string)
        print()
        print("===========================================================================")
        print("================ TEST FOR convert_string_to_vec_chars =====================")
        print('Input: %s\n. Output: %s', string, converted_string)
        print("===========================================================================")
        print()

    #test for 2
    def find_distribution_n_grams_tester(self):
        
        print()
        print("===========================================================================")
        print("================ TEST FOR find_distribution_n_grams =====================")
        for n_gram in range(3):
            dist = self.decrypter.find_distribution_n_grams(plain_text1, n_gram)
            print(f'plaintext1 n_gram={n_gram} distribution')
            for key, val in dist.items():
                print(f'n_gram: {key}, frequency: {val}')
        print("===========================================================================")
        print()

    #test for 3
    def get_terms_ordered_by_dec_freq_tester(self):
        print()
        print("===========================================================================")
        print("================ TEST FOR get_terms_ordered_by_dec_freq =====================")

        dist = defaultdict(lambda : 0)
        for char in alphabet:
            freq = random.randint(0,50)
            dist[char] = freq
            print(f'char: {char}, freq: {freq}')

        n_gram_list = self.decrypter.get_terms_ordered_by_dec_freq(dist)
        print("n_gram_list", n_gram_list)

        print("===========================================================================")
        print()

    #test for 4
    def get_grouped_n_grams_ordered_by_dec_freq_tester(self):

        print()
        print("===========================================================================")
        print("================ TEST FOR get_grouped_n_grams_ordered_by_dec_freq =====================")
        dist = defaultdict(lambda : 0)
        n_gram = 2
        print('n_gram is', n_gram)
        for i in range(len(alphabet) - n_gram + 1 ):
            chars = alphabet[i : i+n_gram ]
            freq = random.randint(0,50)
            dist[chars] = freq
            print(f'chars: {chars}, freq: {freq}')
        
        grouped_n_gram_list = self.decrypter.get_grouped_n_grams_ordered_by_dec_freq(dist)
        print("grouped_n_gram_list", grouped_n_gram_list)
        print("===========================================================================")
        print()

    #test for 5
    def get_n_gram_converter_tester(self):
        print()
        print("===========================================================================")
        print("================ TEST FOR get_n_gram_converter =====================")
        ordered_n_gram_cipher = ["abc", "geq", "adf", "qer", "fqe"]
        ordered_n_gram_plain = ["tre", "fbq", "fqe", "eqw"]
        for i in range(3):

            # cipher list has 1 more term for test 1
            if i == 1: #equal size for test 2
                ordered_n_gram_plain.append("utw")
            elif i == 2:# plain list has 1 more term for test 3
                ordered_n_gram_plain.append("xyz")

            print(f"====TEST {i+1}===")
            print("ordered_n_gram_cipher", ordered_n_gram_cipher)
            print("ordered_n_gram_plain", ordered_n_gram_plain)
            n_gram_converter = self.decrypter.get_n_gram_converter(ordered_n_gram_cipher, ordered_n_gram_plain)
            print('n_gram_converter is' )
            for n_gram_cipher, n_gram_plain in n_gram_converter.items():
                print(f'n_gram_cipher: {n_gram_cipher}, n_gram_plain: {n_gram_plain}')

        print("===========================================================================")
        print()

    #test for 6
    def map_two_distributions_tester(self):

        print()
        print("===========================================================================")
        print("================ TEST FOR map_two_distributions =====================")

        ordered_n_gram_cipher = ["abc", "geq", "adf", "qer", "fqe"]
        ordered_n_gram_plain = ["tre", "fbq", "fqe", "eqw", "xyz"]

        n_gram_converter = defaultdict(str, zip(ordered_n_gram_cipher,ordered_n_gram_plain))
        decrypted_ciphertext = list("abcadfgeqqerfqegeqabcadfabcqeradfgeqabcabcgeqabc")
        print("decrypted_ciphertext before", decrypted_ciphertext)
        start = 0
        t = 5
        n_gram = 3

        self.decrypter.map_two_distributions(n_gram_converter, decrypted_ciphertext, start, t, n_gram)
        print("decrypted_ciphertext after", decrypted_ciphertext)

        print("===========================================================================")
        print()

    #test for 7
    def concate_2_defaultdict_tester(self):

        print()
        print("===========================================================================")
        print("================ TEST FOR concate_2_defaultdict =====================")

        ordered_n_gram_cipher = ["abc", "geq"]
        ordered_n_gram_plain = ["tre", "fbq"]
        org_dict = defaultdict(str, zip(ordered_n_gram_cipher,ordered_n_gram_plain))

        ordered_n_gram_cipher = ["adf", "qer", "fqe"]
        ordered_n_gram_plain = ["fqe", "eqw", "xyz"]
        add_dict = defaultdict(str, zip(ordered_n_gram_cipher,ordered_n_gram_plain))
        print("========= BEFORE =============")
        print('org_dict')
        for key, val in org_dict.items():
            print(f'{key}: {val}')
        print('add_dict')
        for key, val in add_dict.items():
            print(f'{key}: {val}')
        self.decrypter.concate_2_defaultdict(org_dict, add_dict)
        print("========= AFTER =============")
        print('org_dict')
        for key, val in org_dict.items():
            print(f'{key}: {val}')
        print("===========================================================================")
        print()

    #test for 8
    def convert_list_chars_to_string_tester(self):
        print()
        print("===========================================================================")
        print("================ TEST FOR convert_list_chars_to_string =====================")

        lst = ['a', 'b', 'c', 'd', 'e', 'f']
        string = self.decrypter.convert_list_chars_to_string(lst)
        print(f'lst is: {lst}')
        print(f'string is: {string}')
        print("===========================================================================")
        print()


    #test for 9
    def change_char_at_tester(self):

        print()
        print("===========================================================================")
        print("================ TEST FOR change_char_at =====================")
        string = "abcdef"
        index = 2
        char = 'Z'
        print(f"string before: {string}")
        string = self.decrypter.change_char_at(string, index, char)
        print(f"string after: {string}")
        print("===========================================================================")
        print()


    #test for 10
    #TO BE FINISHED
    def try_1_edit_distance_away_groups_tester(self):
        print()
        print("===========================================================================")
        print("================ TEST FOR try_1_edit_distance_away_groups =====================")
        shared_n_gram_group = None
        grouped_n_gram_freq_cipher = None
        grouped_n_gram_freq_plain = None
        n_gram_converter = None
        self.decrypter.try_1_edit_distance_away_groups(shared_n_gram_group, grouped_n_gram_freq_cipher, grouped_n_gram_freq_plain, n_gram_converter)
        print("===========================================================================")
        print()

    #test for 11
    #TO BE FINISHED
    def try_decode_2_gram_tester(self):
        print()
        print("===========================================================================")
        print("================ TEST FOR try_decode_2_gram =====================")

        shared_n_gram_group = None
        grouped_n_gram_freq_cipher = None
        grouped_2_gram_freq_plain = None
        n_gram_converter = None

        self.decrypter.try_decode_2_gram(shared_n_gram_group, grouped_n_gram_freq_cipher, grouped_2_gram_freq_plain, n_gram_converter)
        print("===========================================================================")
        print()


    #test for 12
    #TO BE FINISHED
    def try_decode_1_gram_tester(self):
        print()
        print("===========================================================================")
        print("================ TEST FOR try_decode_1_gram =====================")

        shared_n_gram_group = None
        grouped_n_gram_freq_cipher = None
        ordered_1_gram_plain = None
        n_gram_converter = None

        self.decrypter.try_decode_1_gram(shared_n_gram_group, grouped_n_gram_freq_cipher, ordered_1_gram_plain, n_gram_converter)
        print("===========================================================================")
        print()

    def print_dict(self, the_dict):
        for key, val in the_dict.items():
            print(f'({key}, {val})')
    #test for 13
    def get_grouped_n_gram_converter_tester(self):
        print()
        print("===========================================================================")
        print("================ TEST FOR get_grouped_n_gram_converter =====================")

        t = 5
        ciphertext = self.cipher_generator.generate_cipher(plain_text1, t)
        print('ciphertext for plaintext1')
        print(ciphertext)
        n_gram = 3
        grouped_n_gram_freq_cipher_dist = self.decrypter.find_distribution_n_grams(ciphertext, n_gram)
        grouped_n_gram_freq_cipher = self.decrypter.get_grouped_n_grams_ordered_by_dec_freq(grouped_n_gram_freq_cipher_dist)
        print('grouped_n_gram_freq_cipher')
        self.print_dict(grouped_n_gram_freq_cipher)
        grouped_n_gram_freq_plain_dist = self.decrypter.find_distribution_n_grams(plain_text1, n_gram)
        grouped_n_gram_freq_plain = self.decrypter.get_grouped_n_grams_ordered_by_dec_freq(grouped_n_gram_freq_plain_dist)
        print('grouped_n_gram_freq_plain')
        self.print_dict(grouped_n_gram_freq_cipher)
        grouped_2_gram_freq_plain_dist = self.decrypter.find_distribution_n_grams(plain_text1, 2)
        grouped_2_gram_freq_plain = self.decrypter.get_grouped_n_grams_ordered_by_dec_freq(grouped_2_gram_freq_plain_dist)
        print('grouped_2_gram_freq_plain')
        self.print_dict(grouped_2_gram_freq_plain)
        one_gram_dist = self.decrypter.find_distribution_n_grams(plain_text1, 1)
        print('one_gram_dist')
        self.print_dict(one_gram_dist)
        ordered_1_gram_plain = self.decrypter.get_terms_ordered_by_dec_freq(one_gram_dist)
        print('ordered_1_gram_plain')
        print(ordered_1_gram_plain)
        
        self.decrypter.get_grouped_n_gram_converter(grouped_n_gram_freq_cipher, grouped_n_gram_freq_plain, grouped_2_gram_freq_plain, ordered_1_gram_plain)
        print("===========================================================================")
        print()


    #test for 14
    def decrypt_key_tester(self):
        print()
        print("===========================================================================")
        print("================ TEST FOR decrypt_key =====================")

        t = 5
        ciphertext = self.cipher_generator.generate_cipher(plain_text1, t)
        n_gram = 3

        decrypted_texts = self.decrypter.decrypt_key(t, ciphertext, n_gram)
        for i in range(len(decrypted_texts)):
            decrypted_text = decrypted_texts[i]
            print(f'Decryption for plaintext {i}, edit distance: {self.decrypter.calc_edit_distance(decrypted_text, plain_text1)}')
            print(decrypted_text)
        print("===========================================================================")
        print()

    #test for 15
    def calc_edit_distance_tester(self):
        print()
        print("===========================================================================")
        print("================ TEST FOR calc_edit_distance =====================")

        for decrypted_ciphertext,plaintext in zip(["abcdef", "abcd", "abcfef"], ["abcfef", "abcfef", "abc"]): 
            
            distance = self.decrypter.calc_edit_distance(decrypted_ciphertext, plaintext)
            print(f"decrypted_ciphertext: {decrypted_ciphertext}, plaintext: {plaintext}. Edit distance: {distance}")

        print("===========================================================================")
        print()

    #test for 16
    def get_most_similar_plaintext_tester(self):
        print()
        print("===========================================================================")
        print("================ TEST FOR get_most_similar_plaintext =====================")
        decrypted_ciphertexts = ["hqllo wozld abcxyz etd henlo wcrld", "hqllo wozld abcxyz etd henlo wcrld", "hqllo wozld abcxyz etd henlo wcrld", "hqllo wozld abcxyz etd henlo wcrld"]
        plaintexts = [ "hello world abcxyz end hello world", "hafo world mnopze end hello world", "hafo world abcdef end hello world", "hafo world abcxyz end hello world"]
        print('decrypted_ciphertexts')
        for decrypted_ciphertext in decrypted_ciphertexts:
            print(decrypted_ciphertext)
        print('plaintexts')
        for plaintext in plaintexts:
            print(plaintext)
        plaintext = self.decrypter.get_most_similar_plaintext(decrypted_ciphertexts, plaintexts)
        print("=========== CHOSEN PLAINTEXT ==========")
        print(plaintext)
        print("===========================================================================")
        print()

    #test for 17
    def decrypt_type_two_tester(self):

        print()
        print("===========================================================================")
        print("================ TEST FOR decrypt_type_two =====================")
        n_gram = 3
        t = 5
        plaintext_test2 = self.cipher_generator.generate_test2(50)
        ciphertext = self.cipher_generator.generate_cipher(plaintext_test2, t)
        print(f'plaintext: {plaintext_test2}')
        print(f'ciphertext: {ciphertext}')
        decrypted_ciphertext = self.decrypter.decrypt_type_two(t, ciphertext, n_gram)
        distance = self.decrypter.calc_edit_distance(decrypted_ciphertext, plaintext_test2)
        print(f"decrypted_ciphertext: {decrypted_ciphertext}, plaintext: {plaintext_test2}. Edit distance: {distance}")
        print("===========================================================================")
        print()


    #test for 18
    def get_most_likely_word_tester(self):
        print()
        print("===========================================================================")
        print("================ TEST FOR get_most_similar_plaintext =====================")

        decrypted_text = "azeswmeness"
        start_index = 0
        chose_word = self.decrypter.get_most_likely_word(decrypted_text, start_index)
        print(f"decrypted_text: {decrypted_text}, start_index: {start_index}, chose_word: {chose_word}")
        print("===========================================================================")
        print()

    #test for 19
    def correct_type_two_decrytion_tester(self):

        print()
        print("===========================================================================")
        print("================ TEST FOR correct_type_two_decrytion =====================")
        decrypted_text = "azeswmeness atzentiunal"
        corrected_decryption = self.decrypter.correct_type_two_decrytion(decrypted_text)
        print(f"decrypted_text: {decrypted_text}, corrected_decryption: {corrected_decryption}")

        print("===========================================================================")
        print()

if __name__ == "__main__":
    tester = Dectypter_Tester()
    tester.run_tests()
