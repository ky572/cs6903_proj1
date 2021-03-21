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

def test(insert_random, random_sched, t2):
    p,c,key = gen.generate_cipher(insert_random=insert_random, random_sched=random_sched, t2=t2)
    guess = decryptor.guess_test2_plaintext(c) if t2 else decryptor.guess_test1_plaintext(c)
    if guess != p:
        print ((p,c,guess,key))
    return True if guess == p else False

def run_tests(runs, insert_random, random_sched, t2, description):
    count = 0
    start = time.time()
    for i in range(runs):
        result = test(insert_random, random_sched, t2)
        if result: count += 1
#        else:
#            break

    end = time.time()
    print(f'{description}: {count}/{runs}')
    print(f'Completed in {end-start} seconds')

def experiment_test1(runs):
    run_tests(runs, False, False, False, 'Test 1, no random characters')
    run_tests(runs, True, False, False, 'Test 1, cyclical key with random characters')
    run_tests(runs, False, True, False, 'Test 1, no random characters, random scheduler')
    run_tests(runs, True, True, False, 'Test 1, random characters with random scheduler')

def experiment_test2(runs):
    run_tests(runs, False, False, True, 'Test 2, no random characters, cyclical key')

def experiment_test2_fallthrough(runs):
    count = 0
    for i in range(runs):
        p,c,key = gen.generate_cipher(insert_random=True, random_sched=True, t2=True)
        guess = decryptor.guess_test1_plaintext(c)
        if guess is not None:
            count += 1
    print(f'Made a guess on {count}/{runs}')

if __name__ == '__main__':
    experiment_test1(int(sys.argv[1]))
    experiment_test2(int(sys.argv[2]))

