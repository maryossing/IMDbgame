import psycopg2
import psycopg2.extras
connection_string = "host='localhost' dbname='imdb_data' user='game_user' password='game_password'"
conn = psycopg2.connect(connection_string, cursor_factory=psycopg2.extras.DictCursor)
cursor = conn.cursor()

def get_person_info(name):
	name_query="SELECT name,id,role1,role2,role3 FROM Person,Roles WHERE name LIKE %(inputname)s AND person_id=id  ORDER BY credits desc LIMIT 3"
	with conn.cursor() as cursor:
		cursor.execute(name_query,dict(inputname=name))
		res=cursor.fetchall()


		return res
def get_person_info_ilike(name):
	name_query="SELECT name,id,role1,role2,role3 FROM Person,Roles WHERE name ILIKE %(inputname)s AND person_id=id  ORDER BY credits desc LIMIT 3"
	with conn.cursor() as cursor:
		cursor.execute(name_query,dict(inputname=name))
		res=cursor.fetchall()
		priority=[]
		for name in res:

			priority.append((name.count(None),name))
		priority.sort()
		ret=[p[1] for p in priority]
		return ret
def get_name(ID):
	name_query="SELECT name FROM Person WHERE id=%(ID)s"
	with conn.cursor() as cursor:
		cursor.execute(name_query,dict(ID=ID))
		return cursor.fetchall()[0][0]
def get_k4(ID):
	titles_query='SELECT * FROM knownfor_Titles WHERE id=%(ID)s'
	with conn.cursor() as cursor:
		cursor.execute(titles_query,dict(ID=ID))
		return cursor.fetchall()
def get_title_id(title,year,genres):
	title_id_query ="SELECT id FROM Title where primaryTitle=%(title)s AND year=%(year)s AND genres=%(genres)s "
	with conn.cursor() as cursor:
		cursor.execute(title_id_query,dict(title=title, year=year,genres=genres))
		return cursor.fetchall()[0][0]

def get_director(ID):
	director_query="SELECT name FROM Person, Principals WHERE id=person_id and title_id= %(ID)s and category='director' "
	actor_director_query="SELECT name FROM Person, Principals WHERE id=person_id and title_id= %(ID)s and ordering=1 "
	with conn.cursor() as cursor:
		cursor.execute(director_query,dict(ID=ID))
		res=cursor.fetchall()
		if len(res)==0:
			cursor.execute(actor_director_query,dict(ID=ID))
			res=cursor.fetchall()
		return res[0][0];

def get_writer(ID):
	writer_query="SELECT name FROM Person, Principals WHERE id=person_id and title_id= %(ID)s and category='writer' "
	with conn.cursor() as cursor:
		cursor.execute(writer_query,dict(ID=ID))
		res=cursor.fetchall()[0][0]

		return res;

def get_highest_rated_movie(ID):
	movie_query="SELECT primaryTitle,year,avgrating from Person,Title,Principals,rating where person.id=%(ID)s AND person_id=person.id AND principals.title_id=Title.id and rating.title_id=Title.id AND type='movie' AND numvotes>5000 ORDER BY avgrating desc,primaryTitle LIMIT 1"
	with conn.cursor() as cursor:
		cursor.execute(movie_query,dict(ID=ID))
		res=cursor.fetchall()[0]

		return res;

def get_movie_together(ID1,ID2):
	movie_query="SELECT primaryTitle,year FROM Title,(SELECT title_id FROM Principals, Title WHERE title_id=id AND person_id=%(ID1)s and type ILIKE '%%movie') AS person1movies,(SELECT title_id FROM Principals, Title WHERE title_id=id AND person_id=%(ID2)s and type ILIKE '%%movie')as person2movies where id=person1movies.title_id and person1movies.title_id=person2movies.title_id "
	with conn.cursor() as cursor:
		cursor.execute(movie_query,dict(ID1=ID1,ID2=ID2))
		res=cursor.fetchall()

		return res;

def get_actor_top250(ID):
	movie_query="SELECT primaryTitle,year FROM top_250_movies,principals where principals.title_id=top_250_movies.title_id and person_id=%(ID)s"
	with conn.cursor() as cursor:
		cursor.execute(movie_query,dict(ID=ID))
		res=cursor.fetchall()
		return res;
