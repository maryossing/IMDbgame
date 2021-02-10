# IMDbgame
Python application that uses PostGres SQL to download IMDb data, create SQL database,
and search the database to perform different fuctions such as:
    IMDb game: ask user for a name of an actor/writer/director, 
                use database to find what four movies IMDb lists as an actor/writer/director's most known films,  
                ask user to guess the titles of those films, providing hints as needed
    Films in common: ask the user for 2 names and list the movies/TV shows that the two people have in common
    Highest rated film: ask the user for a name and print the film IMDb lists as their highest rated
    Top 250: ask the user for a name and print out the titles of the films (if any) that the person appeared in that IMDb lists as being in the Top 250 films of all time

To get started with the project, users will need to run retrieve_data.py and load_data.py to create and populate the database, then run application.py to use the app
    
