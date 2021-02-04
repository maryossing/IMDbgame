from database import *
import time

'''
Removes starting articles ('the', 'a','an') 
 from correct title if given title does not have them

 ie remove_articles("the godfather","godfather") returns 'godfather'
	remove_articles("the godfather","the godfather") returns 'the godfather'
@params: correct full correct title of a film
		 given input title to be compared to correct
@requires correct, given all lowercase
@returns correct without starting article 
'''
def remove_articles(correct,given):
	if correct.startswith('the ') and not given.startswith('the '):
		correct=correct[4:]
	if correct.startswith('an ') and not given.startswith('an '):
		correct=correct[3:]	
	if correct.startswith('a ') and not given.startswith('a '):
		correct=correct[2:]
	return correct

'''
Counts letter differences word by word between correct and given
returns list of number of differences by word

ie count_differences("one two three", "one too 3")-> [0,1,5]


@params:  correct full correct title of a film
		 given input title to be compared to correct
@requires: correct, given all lowercase
@returns: a list of numbers of letter differences
		 between each word in correct and given


'''


def count_differences(correct,given):
	
	#create list of lengths of each word in correct title
	correct_words=[len(word) for word in correct.split(' ')]
	
	#create list of number of words in correct
	#to keep track of number of letter differences in each word
	word_diffs=[0]*len(correct_words)
	cword=0 #number of word in correct
	gword=0	#number of word in given
	gl=0 #index of letter in given


	# go through the 2 titles letter by letter
	# and count the letter differences in each word of the correct title
	for cl in range(len(correct)):

		#if at new word
		if correct[cl]==' ':
			#move to next word in the given title
			if gword<len(given.split(' '))-1 and gword==cword:
				for i in range(gl,len(given)):
					if given[i]==' ':
						gl=i+1
						break
			cword+=1
			if gword<len(given.split(' ')):
				gword+=1
			continue
		#if given is shorter than correct, 
		# fill the entries in word_diffs for the remaining words with the lengths of the remaining letters
		if gl>=len(given):
			#count remaining letters in current word
			for i in  range(cl,len(correct)):
				if correct[i]==' ':
					break
				if correct[i].isalnum():
					word_diffs[cword]+=1

			cword+=1
			#add lengths of all words left in correct
			for i in range(cword,len(correct_words)):
				word_diffs[i]+=correct_words[i]
			break

		#if there is a letter or number difference between the correct title and the given one
		if correct[cl]!=given[gl] and correct[cl].isalnum():
			word_diffs[cword]+=1
		elif correct[cl]!=given[gl] and not correct[cl].isalnum():
			continue


		#move to next letter in given if not at a space
		if given[gl]!=' ':
			gl+=1

	if gl!=len(given):
		#count remaining letters in given word
		for i in  range(gl,len(given)):
			if given[i]!=' ':
			
				word_diffs[cword]+=1
		
	return word_diffs
def longWords(correct):
	lens_and_words=[(len(correct.split(' ')[i]),i) for i in range(len(correct.split(' '))) if len(correct.split(' ')[i])>3]
	lens_and_words.sort(reverse=True)
	words=[tup[1] for tup in lens_and_words]
	return words
def close_enough(correct, given): 

	correct=remove_articles(correct,given)
	if correct==given:
		return True
	if len(given)>len(correct)+2:
		return False
	
	wordcount=correct.count(' ')+1
	word_diffs=count_differences(correct,given)
	long_words=longWords(correct)
	print(word_diffs)
	#if less than 4 total letter differences
	if sum(word_diffs)<4:
		return True
	#if there are more correct words than incorrect letters
	if word_diffs.count(0)>sum(word_diffs):
   		return True
	#if there are more than 2 long words and the 2 longest are mostly correct
	if len(long_words)>2 and word_diffs[long_words[0]]+word_diffs[long_words[1]]<3:
		return True
	return False


def check_guess(title, remaining_titles):
	if title in remaining_titles:
		print_box(["{} ({}) is Correct!".format(remaining_titles[title][2],remaining_titles[title][0])],'-')
		remaining_titles.pop(title)
		return True
	for correct_title in remaining_titles:
		
		if close_enough(correct_title,title):
			print_box(["{} ({}) is Correct!".format(remaining_titles[correct_title][2],remaining_titles[correct_title][0])],'-')
			remaining_titles.pop(correct_title)
			return True
			
	print_box([title+' is Incorrect'],'x')
	return False


def print_box(lines,char):
	max_len=len(lines[0])+8
	print((char*max_len)+'\n'+'|'+((max_len-2)*' ')+'|')
	print('|'+'   '+lines[0]+'   '+'|')
	for i in range(1,len(lines)):
		print('|'+"	",lines[i],((max_len-11-len(lines[i]))*' ')+'|')
	print('|'+((max_len-2)*' ')+'|'+'\n'+(char*max_len))
	print()
def get_hint(remaining_titles,letter_count):
	
	lines=["What type of hint would you like?",'genres','directors','letters']
	print_box(lines,'?')
	hint=input("Choice? => ").strip().lower()
	lines=[]
	if hint=='genres':
		lines=[remaining_titles[title][1] for title in remaining_titles ]
		lines.insert(0,"The genres of the remaining titles are:")
		print_box(lines,'*')
	
	elif hint=='directors':
		ids=[get_title_id(remaining_titles[title][2],remaining_titles[title][0],remaining_titles[title][1]) for title in remaining_titles ]
		lines=[get_director(ID) for ID in ids]
		
		lines.insert(0,"The directors of the remaining titles are:")
		print_box(lines,"*")
	elif hint=='letters':
		lines=[]
		lines=[remaining_titles[title][2][0:letter_count] for title in remaining_titles]
		lines.insert(0,"The first letters of the remaining titles are:")
		print_box(lines,"*")
		letter_count+=1
	else:
		print("\nInvalid Choice. Try Again\n")
		letter_count=get_hint(remaining_titles,letter_count)
	return letter_count
def game(name,ID):
	# l=['First','Second','Third','Fourth','Fifth', 'Sixth', 'Seventh']
	titles=get_k4(ID)
	
	remaining_titles=dict()
	numTV=0
	animation=0
	for title in titles:
		#[year, genres, Primarytitle]
		remaining_titles[title[2].lower()]=[title[4],title[5],title[2]]
		# print(title[3])
		if title[3].count('tv')>0:
			numTV+=1
		if title[5].count('Animation'):
			animation+=1
	print(80*'-' +'\n')
	if len(titles)>1:
		print_box(["Can You Guess the {} Titles that IMDb Claims {} is Most Known For?".format(len(titles),name)],'?')
	else:
		print_box(["Can You Guess the {} Title that IMDb Claims {} is Most Known For?".format(len(titles),name)],'?')
	if animation>0:
		print('\n    {} Titles are Animation\n'.format(animation))
	if numTV>0:
		print('\n    {} Titles are TV Shows\n'.format(numTV))
	print("After 2 wrong guesses, the remaining Titles's years will be revealed\n")
	print("Let's Begin!")
	correct_count=0
	wrong_count=0
	letter_count=1
	while len(remaining_titles)>0:
		#print years after 2 wrong guesses
		if wrong_count>=2:
			lines=[str(remaining_titles[title][0]) for title in remaining_titles ]
			lines.insert(0,"The years of the remaining titles are:")
			print_box(lines,'.')


		print('{} Remaining Titles'.format(len(remaining_titles)))
		guess = input("Guess => ").strip().lower()

		#print hint
		if guess == 'hint':
			
			letter_count =get_hint(remaining_titles,letter_count)
			

		elif guess=='give up':
			print('\nA remaining title is: ')
			for title in remaining_titles:
				print('   '+remaining_titles[title][2], '('+str(remaining_titles[title][0])+')')
				remaining_titles.pop(title)
				break
			print()
			wrong_count+=1


		#if guess is correct
		elif check_guess(guess,remaining_titles):

			correct_count+=1
		else:
			wrong_count+=1

	time.sleep(1)
	print("{}'s Known 4 are:".format(name))
	for title in titles:
		print("\t{} ({})".format(title[2],title[4]))

	print()
	print_box(["Your Score: {} Correct Guesses and {} Wrong Guesses".format(correct_count,wrong_count)],'+')
	if wrong_count==0 and correct_count==len(titles):
		print("A Perfect Score!!")

def input_name():
	name=input(" => ")
	name=name.strip().lower().title()
	print('\nSearching...\n')
	if name.split(' ')[1].startswith('Mac') 

	elif name.split(' ')[1].startswith('Mc'):
		name= name.index(' ')
		results=get_person_info_ilike(name)
	else:
		results=get_person_info(name)
	
	

	if len(results)>1:
		print("Multiple Names Matched Your Input:")
		for i in range(min(3,len(results))):

			print('\t'+str(i+1)+'. '+ results[i][0]+' ('+results[i][2],end='')
			j=3
			while j< len(results[i]) and results[i][j]!=None:
				print(', '+results[i][j],end='')
				j+=1
			print(')')
		valid=False
		while not valid:
			choice =input("Which person did you mean? (Type q to try a different input) => ").strip()
			if choice.lower()=='q':
				print("\nChoose a Name",end='')
				return input_name()
				valid=True
			elif choice.isdigit() and int(choice)<4 and int(choice)>0:
				return results[int(choice)-1][0],results[int(choice)-1][1]
			else:
				print("Invalid Choice. Try Again")
	elif len(results)==0:
		print('No Names Matched Your Input. Try Again')
		print("\tChoose a Name",end='')
		return input_name()
	else:
		return results[0][0],results[0][1]
def best_movie(name,ID):
	movie=get_highest_rated_movie(ID)
	lines=["{}'s highest rated movie is:".format(name),movie]
	print_box(lines, "0")
def movie_together(ID1,ID2):
	movies=get_movie_together(ID1,ID2)
	name1=get_name(ID1)
	name2=get_name(ID2)

	if len(movies)==0:
		print("{} and {} don't star in any movies together".format(name1,name2))
		return

	print("{} and {} both star in ".format(name1,name2),end="")
	for movie in movies:
		print("{} ".format(movie[0]))
	print()
def driver():
	

	print("What do you want to do?")
	print("\t1. Play Game")
	print("\t2. Find Movies with Actors in Common")
	print("\t3. Find an Actor's Highest Rated Movie")
	print("\t4. Find Out How Many of the Top 250 Movies an Actor Starred in\n")

	choice=input("Choice => ").strip()
	if not choice.isdigit() or int(choice)<1 or int(choice)>4:
		print("Invalid Choice. Try Again")
		driver()
		return
	choice=int(choice)
	if choice==1:
		print_box(["Welcome to the IMDb Game!"],"%")
		print("\n   To begin choose a name",end='')
		name,ID=input_name()
		game(name,ID)
	elif choice==2:
		print("\n   First Actor",end='')
		name,ID=input_name()
		print("\n   Second Actor",end='')
		name2,ID2=input_name()
		movie_together(ID,ID2)
	elif choice==3:
		print("\n   To begin choose a name",end='')
		name,ID=input_name()
		best_movie(name,ID)
	else:
		print("\n   To begin choose a name",end='')
		name,ID=input_name()
		get_actor_top250(ID)
if __name__ == '__main__':
	print_box(["Welcome to Mary's IMDb thing!"],"%")
	driver()

	
	
	
