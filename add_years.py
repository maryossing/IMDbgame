
import gzip
import csv
from datetime import datetime
import psycopg2


connection_string = "host='localhost' dbname='imdb_data' user='game_user' password='game_password'"

conn = psycopg2.connect(connection_string)

cursor = conn.cursor()

#add year for each title
def add_title_years():
	title_query="UPDATE TITLE SET year = %(yr)s where id=%(tid)s"
	with gzip.open('datasets/title.basics.tsv.gz','rt') as f:
		reader= csv.reader(f,delimiter='\t')
		first = next(reader)
		i=1
		for row in reader:
			if row[4]=='1' or row[4]==1:
				i+=1
				continue
			while row.count('\\N')!=0:
				row.insert(row.index('\\N'),None)
				row.remove('\\N')
			if len(row)!=9:
				print(row)
				row.insert(3,row[2][row[2].index('\t')+1:])
				row[2]=row[2][0:row[2].index('\t')]
				print(row)
				
				
			cursor.execute(title_query,dict(yr=row[5],tid=row[0]))
			conn.commit()
			

			if i%1000==0: 
				print(i, "{:.2f}%".format(i/6939000*100))
			i+=1


if __name__ == '__main__':
	add_title_years()