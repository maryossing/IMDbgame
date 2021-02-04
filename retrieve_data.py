import gzip
import wget
from os import mkdir
from shutil import rmtree

with open('code/datasets.txt') as datasets_file:
	urls = datasets_file.readlines()

	
	rmtree('code/datasets', ignore_errors=True)
	mkdir('code/datasets')

	for u in urls:
		print(u)
		f = wget.download(u.rstrip(), 'code/datasets/')
		print(f)


