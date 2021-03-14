import sys
import encryption_test
import decryptor
import time

gen = encryption_test.Cipher_Generator()

def find_ngram_indices(ngram, seq):
    l = len(seq)
    n = len(ngram)
    indices = []
    for i in range(0,l-n+1):
        if seq[i:i+n] == ngram: indices.append(i)
    return indices

def test(insert_random, random_sched):
    p,c,key = gen.generate_test1_cipher(insert_random=insert_random, random_sched=random_sched)
    guess = decryptor.guess_plaintext(c)
    if guess != p:
        print ((p,c,guess))
    return True if guess == p else False

def run_tests(runs, insert_random, random_sched, description):
    count = 0
    start = time.time()
    for i in range(runs):
        result = test(insert_random, random_sched)
        if result: count += 1
        else:
            break

    end = time.time()
    print(f'{description}: {count}/{runs}')
    print(f'Completed in {end-start} seconds')

def experiment(runs):
    run_tests(runs, False, False, 'Test 1, no random characters')
    run_tests(runs, True, False, 'Test 1, cyclical key with random characters')
    run_tests(runs, False, True, 'Test 1, no random characters, random scheduler')
    run_tests(runs, True, True, 'Test 1, random characters with random scheduler')

if __name__ == '__main__':
    experiment(int(sys.argv[1]))

