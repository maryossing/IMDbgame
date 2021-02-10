CREATE VIEW k4_title1_view AS 
	SELECT Person.id,name, primaryTitle, type, year, genres,origTitle 
		FROM KnownFor 
		INNER JOIN Title ON KnownFor.title1=title.id 
		INNER JOIN Person ON Person.id = KnownFor.person_id;


CREATE VIEW k4_title2_view AS 
	SELECT Person.id, name, primaryTitle, type, year, genres,origTitle 
		FROM KnownFor 
		INNER JOIN Title ON KnownFor.title2=title.id 
		INNER JOIN Person ON Person.id = KnownFor.person_id;

CREATE VIEW k4_title3_view AS 
	SELECT Person.id,name, primaryTitle, type, year, genres,origTitle 
		FROM KnownFor 
		INNER JOIN Title ON KnownFor.title3=title.id 
		INNER JOIN Person ON Person.id = KnownFor.person_id;

CREATE VIEW k4_title4_view AS 
	SELECT Person.id,name, primaryTitle, type, year, genres,origTitle 
		FROM KnownFor 
		INNER JOIN Title ON KnownFor.title4=title.id 
		INNER JOIN Person ON Person.id = KnownFor.person_id;

CREATE VIEW top_250_movies AS 
	SELECT primaryTitle,title_id, year, avgRating,numVotes
		FROM title
		INNER JOIN  rating on title_id=id
		WHERE numVotes>=90000 and type='movie' order by avgRating desc,numvotes desc limit 250;


