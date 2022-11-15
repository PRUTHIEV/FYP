import random
from collections import Counter
from math import log

N = 100
bin_len = 9
chunk_size_chr = 3
primes = []
ent_threshold_chr = 0.95
min_pool_size = 10
chunk_size_key = 9
ent_threshold_key = 0.95
crx_pt = 5

def _xor(A, B):
	"""
	A and B are chars
	and this function performs
	logical XOR on chars.
	'0' ^ '1'
	"""
	return '0' if A == B else '1'


def get_bin(N):
	"""
	generate binary form of N
	upto bit_len places
	"""
	return _get_bin(N, bin_len)

def _get_bin(N, R):
	"""
	generate binary form of N
	upto R places
	"""
	if type(N) == str:
		N = ord(N[0])
	return format(N, 'b').zfill(R)

def _rand_bw(N, M):
	"""
	returns random integer between N, M
	"""
	return int(N + random.random()*(M-N+1))

def _rand(N):
	"""
	returns random integer between 0, N
	"""
	return int(random.random()*N)

def sieve(n):
	"""
	initializes the primes upto n
	"""
	prime = [True for i in range(n+1)]
	p = 2
	while (p*p <= n):
		if (prime[p] == True):
			for i in range(p*2, n+1, p):
				prime[i] = False
		p += 1
	prime[0] = False
	prime[1] = False
	for p in range(n+1):
		if prime[p]:
			primes.append(p)


def _generate_pool():
	"""
	generates an initial pool
	of bit_len bits children
	"""
	rnd_chars = [get_bin(_rand(26)) for _ in range(16)]
	rnd_primes = []
	for _ in range(16):
		rnd_primes.append(get_bin(primes[_rand(len(primes))]))
	rnd_crx_pt = [_rand_bw(1,8) for _ in range(16)]
	crx_pool = []
	for parent1, parent2, crx_pt in zip(rnd_chars, rnd_primes, rnd_crx_pt):
		child1 = parent1[:crx_pt] + parent2[crx_pt:]
		child2 = parent2[:crx_pt] + parent1[crx_pt:]
		crx_pool.extend([child1, child2])
	for idx in range(len(crx_pool)):
		crx_pool_el = list(crx_pool[idx])
		crx_pool_el[0], crx_pool_el[8] = crx_pool_el[8], crx_pool_el[0]
		# crx_pool_el[0] = '1' if crx_pool_el[0] == '0' else '0'
		# crx_pool_el[8] = '1' if crx_pool_el[8] == '0' else '0'
		crx_pool[idx] = ''.join(crx_pool_el)
	# print(rnd_chars)
	# print(rnd_primes)
	# print(rnd_crx_pt)
	# print(crx_pool)
	# ss_entr_chr(crx_pool[0])
	# ss_pool(crx_pool)
	return crx_pool

def ss_entr_chr(chromosome):
	"""
	computes symbolized shannon entropy
	for a chromosome.
	"""
	def chunks(input, chunk_size_chr):
		return [input[i:i+chunk_size_chr] for i in range(0, len(input), chunk_size_chr)]

	chunks_split = chunks(chromosome, chunk_size_chr)
	chunks_ctr = Counter(chunks_split)
	N = len(chunks_split)
	H = -1/log(N)
	et = 0
	for el in chunks_ctr:
		_, val = el, chunks_ctr[el]
		p = val/N
		et += p*log(p)
	H *= et
	# print(chunks_split)
	# print(H)
	return H


def ss_pool(pool):
	"""
	computes symbolized shannon entropy
	for the entire pool
	"""
	ent_pool = []
	for chromosome in pool:
		ent_pool.append(ss_entr_chr(chromosome))
	# print(ent_pool)
	return ent_pool

def filter_pool(pool):
	"""
	filters pool by selecting chromosomes
	above the entropy value of ent_threshold_chr
	"""
	fltr_pool = []
	for chromosome in pool:
		if ss_entr_chr(chromosome) > ent_threshold_chr:
			fltr_pool.append(chromosome)
	if len(fltr_pool) < min_pool_size:
		return None
	return fltr_pool


def ss_ent_key(key):
	"""
	computes symbolized shannon entropy
	for a key.
	"""
	def chunks(input, chunk_size_key):
		return [input[i:i+chunk_size_key] for i in range(0, len(input), chunk_size_key)]

	chunks_split = chunks(key, chunk_size_key)
	chunks_ctr = Counter(chunks_split)
	N = len(chunks_split)
	H = -1/log(N)
	et = 0
	for el in chunks_ctr:
		_, val = el, chunks_ctr[el]
		p = val/N
		et += p*log(p)
	H *= et
	# print(chunks_split)
	# print(H)
	return H


def form_key(pool):
	"""
	merges the individual chromosome
	to form a key
	"""
	return ''.join(pool)


def create_key():
	sieve(N)
	ent_val = 0
	while ent_val < ent_threshold_key:
		pool = _generate_pool()
		pool = filter_pool(pool)
		if pool == None:
			continue
		key = form_key(pool)
		ent_val = ss_ent_key(key)
	# print("Key: {}".format(key))
	# print("Entropy Value: {}".format(ent_val))
	return key, cvt_key(key)


def cvt_key(key):
	"""
	converts binary key into
	letters
	"""
	def chunks(input, chunk_size_key):
		return [input[i:i+chunk_size_key] for i in range(0, len(input), chunk_size_key)]
	key_chunks = chunks(key, chunk_size_key)
	# for el in list(key_chunks):
	# 	print(chr(int(el, 2)))
	return ''.join([chr(int(el, 2)) for el in key_chunks])



def diffuse_pt(plain_text):
	"""
	diffuses plain text using
	genetic operators such as crossover
	and mutation
	"""
	bin_pts = [get_bin(ch) for ch in list(plain_text)]
	crx_children = []
	for idx in range(len(bin_pts)):
		fp = idx % len(bin_pts)
		sp = (idx + 1) % len(bin_pts)
		p1, p2 = bin_pts[fp], bin_pts[sp]
		c1, c2 = p1[:crx_pt] + p2[crx_pt:], p2[:crx_pt] + p1[crx_pt:]
		crx_children.extend([c1, c2])
	# print(bin_pts)
	# print(crx_children)
	for idx in range(len(crx_children)):
		crx_el = list(crx_children[idx])
		crx_el[0], crx_el[8] = crx_el[8], crx_el[0]
		crx_children[idx] = ''.join(crx_el)

	# print(bin_pts)
	# print(crx_children)
	return ''.join(crx_children)


def remove_diffusion(diffused_text):
	"""
	removes diffusion while
	decrypting the text
	"""
	def chunks(input, chunk_size_key):
		return [input[i:i+chunk_size_key] for i in range(0, len(input), chunk_size_key)]
	dif_tx_chunks = chunks(diffused_text, chunk_size_key)
	rm_mut_els = []
	for idx in range(len(dif_tx_chunks)):
		dif_el = list(dif_tx_chunks[idx])
		dif_el[0], dif_el[8] = dif_el[8], dif_el[0]
		rm_mut_els.append(''.join(dif_el))
	orig_data = []
	for idx in range(0, len(rm_mut_els), 2):
		el1, el2 = rm_mut_els[idx], rm_mut_els[idx+1]
		parent = el1[:crx_pt] + el2[crx_pt:]
		orig_data.append(parent)
		# print("{} + {} = {}".format(el1, el2, parent))
	# print(rm_mut_els)
	# print(orig_data)
	return orig_data


def encrypt(plain_text, key):
	"""
	encrypts plain text using
	the key provided
	"""
	key_list = list(key)
	pt_list = list(diffuse_pt(plain_text))
	mod = len(key_list)
	idx = 0
	enc_data = []
	for el in pt_list:
		enc_data.append(_xor(el, key_list[idx%mod]))
		idx += 1
	enc_data = ''.join(enc_data)
	return enc_data, cvt_key(enc_data)

def decrypt(encrypted_text, key):
	"""
	decrypts encrypted text
	using the key provided
	"""
	key_list = list(key)
	ect_list = list(encrypted_text)
	mod = len(key_list)
	idx = 0
	dec_data = []
	for el in ect_list:
		dec_data.append(_xor(el, key_list[idx%mod]))
		idx += 1
	dec_data = ''.join(remove_diffusion(''.join(dec_data)))
	return dec_data, cvt_key(dec_data)

def run_test(inp=None):
	key, fmt_key = create_key()
	plain_text = "This project is made by Gaurav, Prashant and Manish Devgan." if inp == None else inp
	enc_bin, enc_text = encrypt(plain_text, key)
	dec_bin, dec_text = decrypt(enc_bin, key)
	print("Plain Text     : {}".format(plain_text))
	print("Key            : {}".format(fmt_key))
	print("Encrypted Text : {}".format(enc_text))
	print("Decrpyted Text : {}".format(dec_text))
	if plain_text == dec_text:
		print("Report         : Passed!")
	else:
		print("Report         : Failed!")
	assert plain_text == dec_text


if __name__ == '__main__':
	inp = str(input("Default Plain Text: 'This project is made by Gaurav, Prashant and Manish Devgan.'\nEnter plain text or press enter to use default: "))
	if inp == "":
		run_test()
	else:
		run_test(inp)