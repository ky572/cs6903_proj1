
from decrypt_2 import *
import time
import random
from collections import defaultdict


class Decrypt_test2(Decrypter_2):
    def __init__(self):
        super().__init__()
        

    def process_plaintext(self, freq, plaintext, ciphertext):
        the_plaintext = " ".join(plaintext)
        # freq = defaultdict(lambda: 0)
        # max_freq = 0
        # for t in range(1,25):
        #     for j in range(0, len(the_plaintext), t):
        #         if j + t >= len(the_plaintext):
        #             break
        #         key = []
                
        #         for i in range(j, j+t):
        #             key_distance =  self.letter_to_index[ ciphertext[i] ]  - self.letter_to_index[ the_plaintext[i] ] 
        #             if key_distance < 0:
        #                 key_distance += len(alphabet)
        #             key_distance %= len(alphabet)
        #             key.append(key_distance)
        #         key = tuple(key)
        #         freq[key] += 1
        #         if max_freq < freq[key]:
        #             max_freq = freq[key]
        key = []
        max_freq = 0
        for t in range(24):
               
            key_distance =  self.letter_to_index[ ciphertext[t] ]  - self.letter_to_index[ the_plaintext[t] ] 
            if key_distance < 0:
                key_distance += len(alphabet)
            key_distance %= len(alphabet)
            key.append(key_distance)
            key_tup = tuple(key)
            freq[tuple(key)] += 1
            max_freq = max(max_freq, freq[key_tup])
            # possible_keys.add(tuple(key))
        return max_freq
        # for key, val in freq.items():
        #     if val == max_freq:
        #         possible_keys.add(key)

    def get_possible_keys(self, ciphertext):
        #try all combinations of first 5 words as plaintext
        possible_keys = set()
        plaintext = [None for i in range(5)]
        text_len = 0
        words.sort(key=lambda word: -len(word))
        freq = defaultdict(lambda: 0)
        max_freq = 0
        for i in range(len(words)):
            plaintext[0] = words[i]
            text_len += len(words[i])
            if text_len >= 24:
                mx_freq = self.process_plaintext(freq, plaintext[:1], ciphertext)
                max_freq = max(mx_freq, max_freq)
                text_len -= len(words[i])
                continue
            text_len -= len(words[i])
            for j in range(len(words)):
                plaintext[1] = words[j]

                text_len += len(words[j])
                if text_len >= 24:
                    mx_freq = self.process_plaintext(freq, plaintext[:2], ciphertext)
                    max_freq = max(mx_freq, max_freq)
                    text_len -= len(words[j])
                    continue
                text_len -= len(words[j])
                for k in range(len(words)):
                    plaintext[2] = words[k]

                    text_len += len(words[k])
                    if text_len >= 24:
                        mx_freq = self.process_plaintext(freq, plaintext[:3], ciphertext)
                        max_freq = max(mx_freq, max_freq)
                        text_len -= len(words[k])
                        continue
                    text_len -= len(words[k])

                    for a in range(len(words)):
                        plaintext[3] = words[a]
                        text_len += len(words[a])

                        if text_len >= 24:
                            mx_freq = self.process_plaintext(freq, plaintext[:4], ciphertext)
                            max_freq = max(mx_freq, max_freq)
                            text_len -= len(words[a])
                            continue
                        
                        text_len -= len(words[a])

                        for b in range(len(words)):
                            plaintext[4] = words[b]
                            
                            mx_freq = self.process_plaintext(freq, plaintext, ciphertext)
                            max_freq = max(mx_freq, max_freq)

        for key, val in freq.items():
            # if val == max_freq:
            possible_keys.add(key)
        # return list(possible_keys)
        return possible_keys

    #O(max_ran_chars * L)
    def get_decryptions_from_key(self, key, ciphertext, max_ran_chars):
        t = len(key)
        ciphertexts = []
        for i in range(max_ran_chars):
            cipher = list(ciphertext)
            for i in range(len(ciphertext)):
                cipher[i] = self.single_decode(ciphertext[i], key[i%t])
            ciphertexts.append(cipher)
        return ciphertexts

    #O(max_ran_chars * max_i (len(word_i)))
    # end - start = O(max_ran_chars)
    def get_closest_word(self, cipher, start, end, word):
        word_len = len(word)
        min_distance = float('inf')
        pos = None
        for i in range(start, end):
            if i + word_len >= len(cipher):
                break
            curr_word = cipher[i: i + word_len]
            distance = self.calc_edit_distance(curr_word, word)
            if distance < min_distance:
                min_distance = distance
                pos = i
        return pos, min_distance

    #O(L * num_random_chars * len(words)* max_i (len(word_i)) ) = 500*50 *40= 1e6
    def decrypt(self, key, decryptions, max_ran_chars):
        t = len(key)
        decrypted = []
        index = 0
        num_ran_chars = 0
        L = len(decryptions[0])
        i = 0
        while i < L:
            remain_ran_chars = max_ran_chars - num_ran_chars
            # if remain_ran_chars >= L - i:
            #     break
            chose_word = None
            min_distance = float('inf')
            pos = None
            

            if remain_ran_chars < 0:
                remain_ran_chars = 0
            #O(num_random_chars * len(words) * max_i (len(word_i)))
            for decryption in decryptions:
                for word in words:
                    curr_pos, curr_dist = self.get_closest_word(decryption, i, i+max_ran_chars, word)
                    if curr_dist < min_distance:
                        min_distance = curr_dist
                        pos = curr_pos
                        chose_word = word
                        
            if pos == None:
                break

            num_ran_chars += pos - i
            decrypted.append(chose_word)
            i = pos + len(chose_word)
        return " ".join(decrypted)

    def mean_edit_distance(self, decryptions, decrypted):
        return sum([self.calc_edit_distance(decrypted, decryption) for decryption in decryptions]) / len(decryptions)
    
    #O(L * num_random_chars * len(words) * max_i (len(word_i)) * possible_keys)
    # possible_keys = t * len(words)^5 * max_i(len(word_i))
    def brute_force_decrypt(self, ciphertext):
        best_decryption = None
        best_edit_distance = float('inf')
        max_ran_chars = 50
        start = time.time()
        #O(len(words)^5 * max_i(len(word_i)) * 6)
        possible_keys = self.get_possible_keys(ciphertext)
        end = time.time()

        print(f'real key in possible_keys: {tuple(self.cipher_generator.key) in possible_keys}.')
        print(f'{len(possible_keys)} possible_keys, takes {end-start} seconds')

        total = 0
        total_time = 0
        position_len = 0
        last_distance = None
        for possible_key in possible_keys:
            
            # count = 0
            # for t in range(24):

            # key = possible_key[:t+1]
            start = time.time()
            #O(max_ran_chars * L)
            decryptions = self.get_decryptions_from_key( possible_key, ciphertext, max_ran_chars)
            #O(L * num_random_chars * len(words)* max_i (len(word_i)) )
            decrypted = self.decrypt(possible_key, decryptions, max_ran_chars)
            distance = self.mean_edit_distance(decryptions, decrypted)

            if distance < best_edit_distance:
                best_decryption = decrypted
                best_edit_distance = distance
            
            
            end = time.time()
            total_time += end-start
            total += 1

            # if distance <= 0.2 * len(ciphertext): #only mild success
            #     break

            # if last_distance and abs(last_distance - distance) <= 0.1 *  len(ciphertext):
            #     count += 1
            # last_distance = distance
            # if count >= 3:
            #     break
        # print(f'Each key takes {total_time/total} to decrypt')
        # print(f'average position len: {position_len/total}')
        return best_edit_distance, "".join(best_decryption)


    def run_test(self):
        correct = 0
        pseudo_correct = 0
        total = 1
        start = time.time()
        for i in range(total):
            print()
            print("======================================")
            t = random.randint(1,24)
            num_words = 50
            plaintext = self.cipher_generator.generate_test2(num_words)
            ciphertext = self.cipher_generator.generate_cipher(plaintext, t)
            # print(f'key: {self.cipher_generator.key}')
            print(f'plaintext, len: {len(plaintext)}: {plaintext}')
            print(f'ciphertext: {ciphertext}')
            # print()
            distance, decrypted = self.brute_force_decrypt(ciphertext)
            print(f'decrypted: {decrypted}')
            print(f'error: {distance}. Percent correct: {( 1.0 - distance / len(plaintext) ) * 100 }')
            
            if decrypted == plaintext:
                correct += 1
            if distance / len(plaintext) <= 0.2:
                pseudo_correct += 1

            print("======================================")
            print()
        end = time.time()
        print(f'Test 2 with no random characters. Correct: {correct}. Total: {total}. Accuracy: {correct/total}')
        print(f'Pseudo Correct: {pseudo_correct}. Total: {total}. Accuracy: {pseudo_correct/total}')
        print(f'Average time: {(end-start)/total}')

        correct = 0
        pseudo_correct = 0
        total = 1
        start = time.time()
        
        
        for i in range(total):
            print()
            print("======================================")
            t = random.randint(1,24)
            num_words = 50
            num_random = random.randint(1, 50)
            plaintext = self.cipher_generator.generate_test2(num_words)
            ciphertext = self.cipher_generator.generate_cipher(plaintext, t, True, num_random)
            # print(f'key: {self.cipher_generator.key}')
            print(f'plaintext, len: {len(plaintext)}: {plaintext}')
            print(f'ciphertext: {ciphertext}')
            # print()
            distance, decrypted = self.brute_force_decrypt(ciphertext)
            print(f'decrypted: {decrypted}')
            print(f'error: {distance}. Percent correct: {( 1.0 - distance / len(plaintext) ) * 100 }')
            
            if decrypted == plaintext:
                correct += 1
            if distance / len(plaintext) <= 0.2:
                pseudo_correct += 1

            print("======================================")
            print()
        end = time.time()
        print(f'Test 2 with some random characters. Correct: {correct}. Total: {total}. Accuracy: {correct/total}')
        print(f'Pseudo Correct: {pseudo_correct}. Total: {total}. Accuracy: {pseudo_correct/total}')
        print(f'Average time: {(end-start)/total}')

if __name__ == "__main__":
    decryptor = Decrypt_test2()
    decryptor.run_test()
    