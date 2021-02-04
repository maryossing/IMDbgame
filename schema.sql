-- DROP SCHEMA IF EXISTS game CASCADE;
-- CREATE SCHEMA game;

DROP TABLE IF EXISTS Person CASCADE;
DROP TABLE IF EXISTS Roles CASCADE;

DROP TABLE IF EXISTS KnownFor CASCADE;
-- DROP TABLE IF EXISTS Title CASCADE;
-- DROP TABLE IF EXISTS Movie CASCADE;
-- DROP TABLE IF EXISTS TVSeries CASCADE;
-- DROP TABLE IF EXISTS Episode CASCADE;
-- DROP TABLE IF EXISTS Rating CASCADE;
-- DROP TABLE IF EXISTS Principals;




-- DROP TABLE IF EXISTS Title CASCADE;

-- CREATE TABLE Principals(
-- 	title_id VARCHAR(15) REFERENCES Smaller_Title(id),
-- 	ordering INT,
-- 	person_id VARCHAR(10) REFERENCES Person(id),
-- 	category VARCHAR(127),
-- 	job VARCHAR(255),
-- 	charName VARCHAR(1023),
-- 	PRIMARY KEY(title_id, ordering)

-- );

CREATE TABLE Person(
	id VARCHAR(10) PRIMARY KEY,
	name VARCHAR(255),
	birthYear INT,
	deathYear INT,
	credits INT,
	CONSTRAINT chk_years CHECK (birthYear <= deathYear AND deathYear<=2020 AND birthYear>0)
);

CREATE TABLE Roles(
	person_id VARCHAR(10) REFERENCES Person(id),
	role1 VARCHAR(255),
	role2 VARCHAR(255),
	role3 VARCHAR(255),
	PRIMARY KEY(person_id)
);

-- CREATE TABLE Title(
-- 	id VARCHAR(15) PRIMARY KEY,
-- 	primaryTitle VARCHAR(1023),
-- 	origTitle VARCHAR(1023),
-- 	type VARCHAR(255),
-- 	isAdult BOOLEAN,
-- 	genres VARCHAR(255),
-- 	runtime INT
-- );
CREATE TABLE KnownFor(
	person_id VARCHAR(10) REFERENCES Person(id),
	title1 VARCHAR(15) REFERENCES smaller_title(id),
	title2 VARCHAR(15) REFERENCES smaller_title(id),
	title3 VARCHAR(15) REFERENCES smaller_title(id),
	title4 VARCHAR(15) REFERENCES smaller_title(id),
	PRIMARY KEY(person_id)
);

-- CREATE TABLE Movie(
-- 	title_id VARCHAR(10) REFERENCES Title(id),
-- 	year INT,
-- 	PRIMARY KEY(title_id),
-- 	CONSTRAINT chk_year check (year>1800)
-- );
-- CREATE TABLE TVSeries(
-- 	title_id VARCHAR(15) REFERENCES Title(id),
-- 	startYear INT,
-- 	endYear INT,
-- 	seasons INT,
	
-- 	PRIMARY KEY(title_id),
-- 	CONSTRAINT chk_year check (startYear<=endYear AND startYear>1800)
-- );

-- CREATE TABLE Episode(
-- 	series_id VARCHAR(10) REFERENCES TVSeries(title_id),
-- 	eptitle_id VARCHAR(15) REFERENCES Title(id),
-- 	season INT,
-- 	episodeNum INT,
-- 	PRIMARY KEY (eptitle_id,series_id)
-- );
-- CREATE TABLE Rating(
-- 	title_id VARCHAR(15) REFERENCES Title(id),
-- 	avgRating DECIMAL(4,2),
-- 	numVotes INT,
-- 	PRIMARY KEY (title_id)
-- );

