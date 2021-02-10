
import gzip
import csv
from datetime import datetime
import psycopg2
k4=dict()

connection_string = "host='localhost' dbname='imdb_data' user='game_user' password='game_password'"

conn = psycopg2.connect(connection_string)

cursor = conn.cursor()

#replace empty values(//N) with None
def fill_nulls(row):
	while row.count('\\N')!=0:
		row.insert(row.index('\\N'),None)
		row.remove('\\N')
	return row

#load Person, Roles, KnownFor tables
def load_Person_Roles():

	person_query = "INSERT INTO Person (id,name,birthYear,deathYear) VALUES (%(id)s,%(name)s, %(birth)s,%(death)s) ON CONFLICT DO NOTHING"
	roles_query="INSERT INTO Roles(person_id, role1,role2,role3) VALUES (%(id)s, %(r1)s,%(r2)s,%(r3)s)"
	id_query="SELECT id from Person where name=%(name)s and (birthYear IS NULL or birthYear=%(birth)s)"
	known4_query="INSERT INTO KnownFor(person_id, title1,title2,title3,title4) VALUES (%(id)s, %(t1)s,%(t2)s,%(t3)s,%(t4)s)"
	title_query="SELECT * FROM Title Where id=%(tid)s"
	principals_query='SELECT * FROM principals WHERE person_id=%(id)s'
	i=0;
	with gzip.open('datasets/name.basics.tsv.gz', 'rt') as f:
		reader= csv.reader(f,delimiter='\t')
		first = next(reader)
		for row in reader:
			i+=1
			#fill empty values with None
			row=fill_nulls(row)
			#if person died before they were born, skip
			if row[2]!=None and row[3]!=None and row[3]<row[2]:
				print(row)
				continue
			#if no known 4, skip
			if row[5]==None:
				continue

			#get list of known4
			known4=row[5].split(",")
			
			# fill with None until there are 4 values
			while len(known4)<4:
				known4.append(None)
			while known4.count('\\N')!=0:
				known4.insert(known4.index('\\N'),None)
				known4.remove('\\N')
			j=0
			#check that all 4 titles in each person's known4 exist in titles table
			while j<4 and known4[j]!=None:
				cursor.execute(title_query,dict(tid=known4[j]))
				res=cursor.fetchall()
				if len(res)==0:
					known4[j]=None
				j+=1
			cursor.execute(principals_query,dict(id=row[0]))
			res=cursor.fetchall()
			if known4.count(None)==4 and len(res)==0:
				continue
			cursor.execute(person_query, dict(id=row[0],name=row[1], birth=row[2],death=row[3]))
			conn.commit()
            
			cursor.execute(known4_query, dict(id=row[0], t1=known4[0],t2=known4[1],t3=known4[2],t4=known4[3]))
			conn.commit()
			
			

			#get list of roles
			roles=row[4].split(",")
			while len(roles)!=3:
				roles.append(None)
			cursor.execute(roles_query, dict(id=row[0], r1=roles[0],r2=roles[1],r3=roles[2]))
			conn.commit()

			
			if i%10000==0:
				print(i, "{:.2f}%".format(i/ 10194348*100))
			


#fills titles, movies,tvseries tables
def load_title():
	title_query="INSERT INTO Title(id,PrimaryTitle,origTitle,type,genres,runtime,year) VALUES (%(id)s,%(ptitle)s,%(otitle)s,%(type)s,%(genres)s,%(runtime)s,%(year)s)"
	movie_query="INSERT INTO Movie(title_id,year) VALUES (%(titleid)s,%(year)s)"
	tvseries_query="INSERT INTO TVSeries(title_id, startYear,endYear) VALUES (%(titleid)s,%(start)s,%(endy)s)"
	with gzip.open('datasets/title.basics.tsv.gz','rt') as f:
		reader= csv.reader(f,delimiter='\t')
		first = next(reader)
		i=1
		for row in reader:
			row=fill_nulls(row)
			type_=row[1].lower()
            #if adult
			if row[4]=='1' or (type_!="movie" and type_!="tvminiseries" and  type_!="tvmovie" and  type_!="tvseries" and  type_!="tvspecial"):
				continue
			# for the few titles where the Primary and Original titles were not split at '\t'
			# manually split them
			if len(row)!=9:
				print(row)
				row.insert(3,row[2][row[2].index('\t')+1:])
				row[2]=row[2][0:row[2].index('\t')]
				print(row)
				
				
			cursor.execute(title_query,dict(id=row[0],ptitle=row[2],otitle=row[3],type=row[1],genres=row[8],runtime=row[7],year=row[5]))
			conn.commit()
			#if title is a movie add to movie table
			if row[1].lower()=="movie"or row[1].lower()=="tvmovie":
				cursor.execute(movie_query, dict(titleid=row[0],year=row[5]))
				conn.commit()
			#if title is a tvseries add to tvseries table
			elif row[1].lower()=='tvseries'or row[1].lower()=='tvminiseries':
				cursor.execute(tvseries_query, dict(titleid=row[0],start=row[5],endy=row[6]))
				conn.commit()

			if i%1000==0: 
				print(i, "{:.2f}%".format(i/6939000*100))
			i+=1

#load Episode table
# def load_Episode():
# 	episode_query="INSERT INTO Episode(series_id,eptitle_id,season,episodeNum) VALUES (%(sid)s,%(tid)s,%(season)s,%(episodeNum)s)"
# 	show_query="SELECT title_id FROM TVSeries Where title_id=%(sid)s"
# 	title_query="SELECT * FROM Title Where id=%(sid)s"
# 	with gzip.open('datasets/title.episode.tsv.gz', 'rt') as f:
# 		reader= csv.reader(f,delimiter='\t')
# 		first = next(reader)
# 		i=1
# 		for row in reader:
# 			row=fill_nulls(row)
# 			
# 			cursor.execute(show_query,dict(sid=row[1]))
# 			res=cursor.fetchall()
# 			#if parent title(tv show) is not in title table, print and continue
# 			if len(res)==0:
# 				print(row)
# 				cursor.execute(title_query,dict(sid=row[0]))
# 				res=cursor.fetchall()
# 				print(res)
# 				cursor.execute(title_query,dict(sid=row[1]))
# 				res=cursor.fetchall()
# 				print(res)
# 				continue


# 			cursor.execute(episode_query, dict(sid=row[1],tid=row[0],season=row[2],episodeNum=row[3]))
# 			conn.commit()

#  			if i%1000==0:
#  				print(i, "{:.2f}%".format(i/4959000*100)) 
#  			i+=1

#load Rating table
def load_Rating():
	rating_query="INSERT INTO Rating(title_id,avgRating,numVotes) VALUES (%(tid)s,%(avgRating)s,%(numVotes)s)"
	title_query="SELECT id FROM Title Where id=%(tid)s"
    
	with gzip.open('datasets/title.ratings.tsv.gz', 'rt') as f:
		reader= csv.reader(f,delimiter='\t')
		first = next(reader)
		i=1
		for row in reader:
			i+=1
			row=fill_nulls(row)
			cursor.execute(title_query,dict(tid=row[0]))
			res=cursor.fetchall()
			if len(res)==0:
				continue
			
				
			cursor.execute(rating_query, dict(tid=row[0],avgRating=row[1],numVotes=row[2]))
			conn.commit()
			if i%1000==0:
				print(i, "{:.2f}%".format(i/1050000*100))
			

def load_principals():
	principals_query="INSERT INTO Principals(title_id,ordering,person_id,category, job,charName) VALUES (%(tid)s,%(ordering)s,%(pid)s,%(cat)s,%(job)s,%(charName)s)"
	title_query="SELECT id FROM Title Where id=%(tid)s"
	person_query="SELECT id FROM Person Where id=%(pid)s"

	with gzip.open('datasets/title.principals.tsv.gz', 'rt') as f:
		reader= csv.reader(f,delimiter='\t')
		first = next(reader)
		i=0
		for row in reader:
			i+=1
		

			row=fill_nulls(row)
			cursor.execute(title_query,dict(tid=row[0]))
			res=cursor.fetchall()
			if len(res)==0:
				continue
			
			cursor.execute(person_query,dict(pid=row[2]))

			res=cursor.fetchall()
			if len(res)==0:

				continue
			if row[4]!=None:
				row[4]=row[4][:min(255,len(row[4]))]
				
			cursor.execute(principals_query, dict(tid=row[0],ordering=row[1],pid=row[2],cat=row[3],job=row[4],charName=row[5]))
			conn.commit()
			if i%10000==0:
				print(i, "{:.2f}%".format(i/39720000*100))




def main():
	print("Creating Schema")
	cursor.execute(open("schema.sql", "r").read())
	conn.commit()


	print("Loading Title,Movie,TV table")
	load_title()
	print("Loading Person, Roles, and KnownFor tables") 
	load_Person_Roles()
	print("Person and Roles tables loaded")
	


	# print("Loading Episodes")
	# load_Episode()
	print("Loading Ratings")
	load_Rating()
	print("Loading Principals")
	load_principals()
	cursor.execute(open("view.sql", "r").read())
	conn.commit()

	
if __name__ == '__main__':
	main();