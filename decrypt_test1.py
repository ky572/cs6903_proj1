from decrypt_2 import *
# from encryption_test import Cipher_Generator 
import random
from collections import defaultdict
import time


class Decrypt_test1(Decrypter_2):

    def __init__(self):
        super().__init__()
            # print(f'({letter}:{i})', end=" ")
        # print()

    def get_key(self, num_random, ciphertext, plaintext):
        key_lsts = []
        L = len(plaintext)
        L_cipher = len(ciphertext)
        for i in range(num_random+1):
            key_lst = []
            for index in range(L):
                idx = (index+i) % L_cipher

                key_distance =  self.letter_to_index[ ciphertext[idx] ]  - self.letter_to_index[ plaintext[index] ] 
                if key_distance < 0:
                    key_distance += len(alphabet)
                key_distance %= len(alphabet)
                key_lst.append( key_distance )
            key_lsts.append(key_lst)
        return key_lsts

    #O(L*num_random*t)
    def get_possible_keys(self, num_random, ciphertext, plaintext):
        key_lsts = self.get_key(num_random, ciphertext, plaintext)
        # print(key_lsts)
        possible_keys = []
        

        for t in range(1, 25):
            dist = defaultdict(lambda: 0)
            max_freq = 0
            best_key = None
            for key_lst in key_lsts:
                for i in range(0, len(key_lst), t):
                    key = tuple(key_lst[i: i+t])
                    dist[key] += 1
                    if best_key == None or max_freq < dist[key]:
                        best_key = key
                        max_freq = dist[key]

            #limit to 50 possible keys per shift
            # count = 0
            for key, val in dist.items():
                if val == max_freq:
                    possible_keys.append(key)
                    # count += 1
                if len(possible_keys) == t * 50:
                    break
                # if count == 50:
                #     break

        return possible_keys, key_lsts

    #O(L*num_random)
    def find_key_positions(self, key, ciphertext, key_lsts):
        t = len(key)
        key_as_lst = list(key)
        positions = []
        for key_lst in key_lsts:
            for i in range(0, len(key_lst), t):
                if i + t > len(key_lst):
                    continue
                if key_lst[i: i+t] == key_as_lst:
                    positions.append(i)
        return positions

    
    #O(L * t)
    def decrypt_key_at_known_positions(self, positions, ciphertext, key):
        t = len(key)
        for pos in positions:
            ciphertext[ pos: pos+t ] = self.decode(ciphertext, key, pos)
    

    #O(L*t)
    def decode_perturbed_positions(self, ciphertext, plaintext, decrypted_positions, key, max_ran_chars):
        decrypted = []
        i = 0
        j = 0
        t = len(key)
        num_random_chars = 0
        while i < len(ciphertext):
            if j < len(decrypted_positions) and i == decrypted_positions[j]:
                decrypted.extend(ciphertext[i: i+t])
                i += t
                j += 1
            else:
                end = decrypted_positions[j] if j < len(decrypted_positions) else len(ciphertext)
                min_distance = float('inf')
                decrypted_text = None
                pos_in_plaintext = len(decrypted)
                for k in range(i, end):
                    if k + t >= len(ciphertext):
                        break
                    decoded = self.decode(ciphertext, key, k)
                    distance = self.calc_edit_distance(decoded, plaintext[pos_in_plaintext: pos_in_plaintext + t])
                    if  distance < min_distance:
                        min_distance = distance
                        decrypted_text = decoded
                remain_ran_chars = max_ran_chars - num_random_chars
                if min_distance < remain_ran_chars:
                    decrypted.append(decrypted_text)
                    num_random_chars += end - i - t
                else:
                    num_random_chars += end - i
                
                i = end
                
        return decrypted

    #ciphertext as list
    #O(L*num_random* possible_key + L * t * possible_key)
    
    # possible_key = O(t *50)
    def brute_force_decrypt(self, ciphertext, plaintext):
        best_decryption = None
        best_edit_distance = float('inf')
        max_ran_chars = len(ciphertext) - len(plaintext)
        start = time.time()
        #O(L*num_random*t)
        possible_keys, key_lsts = self.get_possible_keys(max_ran_chars, ciphertext, plaintext)
        end = time.time()

        # print()
        # print("======================================")
        # # print(f'possible_keys {possible_keys}')
        # print(f'real key in possible_keys: {tuple(self.cipher_generator.key) in possible_keys}.')
        # print(f'Number of possible keys: {len(possible_keys)}')
        # print("======================================")
        # print()
        # print(f'real key in possible_keys: {tuple(self.cipher_generator.key) in possible_keys}.')
        # print(f'{len(possible_keys)} possible_keys, takes {end-start} seconds')

        total = 0
        total_time = 0
        position_len = 0
        for possible_key in possible_keys:
            start = time.time()
            ciphertext_copy = ciphertext.copy()
            #O(L*num_random)
            positions = self.find_key_positions(possible_key, ciphertext_copy, key_lsts)
            position_len += len(positions)
            #O(L * t)
            self.decrypt_key_at_known_positions( positions, ciphertext_copy, possible_key)
            #O(L*t)
            self.decode_perturbed_positions( ciphertext_copy, plaintext, positions, possible_key, max_ran_chars )
            distance = self.calc_edit_distance(ciphertext_copy, plaintext)

            if distance < best_edit_distance:
                best_decryption = ciphertext_copy
                best_edit_distance = distance
            end = time.time()
            total_time += end-start
            total += 1
        # print(f'Each key takes {total_time/total} to decrypt')
        # print(f'average position len: {position_len/total}')
        return best_edit_distance, "".join(best_decryption)

    def decrypt(self, ciphertext):
        
        best_edit_distance = float('inf')
        answer = None
        total_time = 0
        total = 0
        best_decryption = None
        for i in range(len(self.plaintexts)):
            plaintext = self.plaintexts[i]
            start = time.time()
            ciphertext_lst = list(ciphertext)
            distance, decrypted = self.brute_force_decrypt(ciphertext_lst, plaintext)
            if distance < best_edit_distance:
                answer = plaintext
                best_decryption = decrypted
                best_edit_distance = distance
            end = time.time()
            total_time += end - start
            total += 1
            # print()
            # print("======================================")
            # print(f'plaintext {i+1}, error: {distance}')
           
            # print("======================================")
            # print()
        # print(f'best_decryption: {best_decryption}')
        # print(f'Each plaintext decryption takes about {total_time/total} seconds')
        # print()
        return answer, best_edit_distance


    def run_test(self):
        correct = 0
        total = 50
        tot_error = 0
        start = time.time()
        for i in range(total):
            # print()
            # print("======================================")
            t = random.randint(1,24)
            pindex = random.randint(0, 4)
            plaintext = self.plaintexts[ pindex ]
            ciphertext = self.cipher_generator.generate_cipher(plaintext, t)
            # print(f'key: {self.cipher_generator.key}')
            # print(f'plaintext {pindex+1}: {plaintext}')
            # print(f'ciphertext : {ciphertext}')
            # print()
            decrypted, error = self.decrypt(ciphertext)
            # print(f'decrypted: {decrypted}')
            tot_error += error
            if decrypted == plaintext:
                correct += 1
            # print("======================================")
            # print()
        end = time.time()
        print(f'Test 1 with no random characters. Correct: {correct}. Total: {total}. Accuracy: {correct/total}')
        print(f'Average error: {tot_error/ total}')
        print(f'Average time: {(end-start)/total}')

        correct = 0
        total = 50
        tot_error = 0
        start = time.time()
        for i in range(total):
            # print()
            # print("======================================")
            t = random.randint(1,24)
            num_random = random.randint(1, 50)
            plaintext = random.choice(self.plaintexts)
            ciphertext = self.cipher_generator.generate_cipher(plaintext, t, True, num_random)
            
            # print(f'plaintext {pindex+1}: {plaintext}')
            # print(f'decrypted: {decrypted}')
            # print(f'key: {self.cipher_generator.key}')
            # print(f'Number of random characters: {num_random} ')
            # print()
            decrypted, error = self.decrypt(ciphertext)
            tot_error += error
            # print(f'decrypted: {decrypted}')
            if decrypted == plaintext:
                correct += 1
            # print("======================================")
            # print()
        end = time.time()
        print(f'Test 1 with some random characters. Correct: {correct}. Total: {total}. Accuracy: {correct/total}')
        print(f'Average error: {tot_error/ total}')
        print(f'Average time: {(end-start)/total}')

if __name__ == "__main__":
    decryptor = Decrypt_test1()
    decryptor.run_test()


    

        