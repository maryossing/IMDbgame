DROP SCHEMA IF EXISTS game CASCADE;
CREATE SCHEMA game;

DROP TRIGGER delcreditsupdt ON Principals;
DROP TRIGGER addcreditsupdt ON Principals;
DROP FUNCTION delcreditsupdt_fnct;
DROP FUNCTION addcreditsupdt_fnct;
DROP TABLE IF EXISTS Person CASCADE;
DROP TABLE IF EXISTS Roles CASCADE;

DROP TABLE IF EXISTS KnownFor CASCADE;
DROP TABLE IF EXISTS Title CASCADE;
DROP TABLE IF EXISTS Movie CASCADE;
DROP TABLE IF EXISTS TVSeries CASCADE;
-- DROP TABLE IF EXISTS Episode CASCADE;

DROP TABLE IF EXISTS Rating CASCADE;
DROP TABLE IF EXISTS Principals;

CREATE TABLE Title(
	id VARCHAR(15) PRIMARY KEY,
	primaryTitle VARCHAR(1023),
	origTitle VARCHAR(1023),
	type VARCHAR(255),
	genres VARCHAR(255),
	runtime INT,
	year INT
);



CREATE TABLE Person(
	id VARCHAR(10) PRIMARY KEY,
	name VARCHAR(255),
	birthYear INT,
	deathYear INT,
	credits INT,
	CONSTRAINT chk_years CHECK (birthYear <= deathYear AND birthYear>0)
);
CREATE TABLE Principals(
    title_id VARCHAR(15) REFERENCES Title(id),
    ordering INT,
    person_id VARCHAR(10) REFERENCES Person(id),
    category VARCHAR(127),
    job VARCHAR(255),
    charName VARCHAR(1023),
    PRIMARY KEY(title_id, ordering)

);


CREATE TABLE Roles(
	person_id VARCHAR(10) REFERENCES Person(id),
	role1 VARCHAR(255),
	role2 VARCHAR(255),
	role3 VARCHAR(255),
	PRIMARY KEY(person_id)
);

CREATE TABLE KnownFor(
	person_id VARCHAR(10) REFERENCES Person(id),
	title1 VARCHAR(15) REFERENCES Title(id),
	title2 VARCHAR(15) REFERENCES Title(id),
	title3 VARCHAR(15) REFERENCES Title(id),
	title4 VARCHAR(15) REFERENCES Title(id),
	PRIMARY KEY(person_id)
);

CREATE TABLE Movie(
	title_id VARCHAR(10) REFERENCES Title(id),
	year INT,
	PRIMARY KEY(title_id),
	CONSTRAINT chk_year check (year>1800)
);
CREATE TABLE TVSeries(
	title_id VARCHAR(15) REFERENCES Title(id),
	startYear INT,
	endYear INT,
	seasons INT,

	PRIMARY KEY(title_id),
	CONSTRAINT chk_year check (startYear<=endYear AND startYear>1800)
);

-- CREATE TABLE Episode(
-- 	series_id VARCHAR(10) REFERENCES TVSeries(title_id),
-- 	eptitle_id VARCHAR(15) REFERENCES Title(id),
-- 	season INT,
-- 	episodeNum INT,
-- 	PRIMARY KEY (eptitle_id,series_id)
-- );

CREATE TABLE Rating(
	title_id VARCHAR(15) REFERENCES Title(id),
	avgRating DECIMAL(4,2),
	numVotes INT,
	PRIMARY KEY (title_id)
);


CREATE OR REPLACE FUNCTION addcreditsupdt_fnct()
	RETURNS TRIGGER as
$$
BEGIN
	UPDATE Person SET credits=credits+1 where NEW.person_id=person.id;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER addcreditsupdt
AFTER INSERT
ON Principals
FOR EACH ROW
EXECUTE PROCEDURE addcreditsupdt_fnct();


CREATE OR REPLACE FUNCTION delcreditsupdt_fnct()
	RETURNS TRIGGER as
$$
BEGIN
	UPDATE Person SET credits=credits-1 where OLD.person_id=person.id;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delcreditsupdt
AFTER DELETE
ON Principals
FOR EACH ROW
EXECUTE PROCEDURE delcreditsupdt_fnct();
