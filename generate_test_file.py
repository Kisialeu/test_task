import random
import string 


def rand_str(size=6, chars=string.ascii_lowercase + string.ascii_lowercase ):
	c = 0
	a = []
	while c < 10:
		a.append(''.join(random.choice(chars) for _ in range(size)))
		c += 1
		if c//5 == 0:
			a.append(random.randint(1,999))
	
	return str(a)


c =0
with open(r'softeq_test.test', 'a') as log_file:
	while c < 20:
		log_file.write(rand_str() + rand_str() +'\n')
		c +=1
