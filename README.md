# IMDbgame

   Python application that uses PostgreSQL to download IMDb data, create SQL database,
and search the database to perform different functions for given user input names

## Description
Python application that uses PostgreSQL to download IMDb data, create SQL database,
and search the database to perform different functions such as:
- IMDb game:
   - ask user for a name of an actor/writer/director
   - use database to find what four movies IMDb lists as an actor/writer/director's most known films
   - ask user to guess the titles of those films, providing hints as needed
 - Films in common: ask the user for two names and list the movies/TV shows that the two people have in common
 - Highest rated film: ask the user for a name and print the film IMDb lists as their highest rated
 - Top 250: ask the user for a name and print out the titles of the films (if any) that the person appeared in that are amoung the top 250 highest rated movies acoording to IMDb users' ratings
## Getting Started
 Python3.7 or later required with `psycopg2`, `wget`, `gzip`, and `csv` packages installed
 PostgreSQL 12.1 required
 To get started with the project, users will need to run, from the terminal (or command prompt) in the `IMDbgame` directory, the command:
  ```
  python3.7 retrieve_data.py
  ```
 which will create a `datasets` folder in the `code` folder and download the data from [IMDb](https://www.imdb.com/interfaces/) into `datasets/code`.
 Then, in PostgreSQL, users should run the commands found in `database-setup.sql` in order to create the database and user.
 Then from the terminal in the `IMDbgame/code` folder users will need to run
 ```
  python3.7 load_data.py
 ```
 which will populate the tables in the IMDbdata SQL database.

## Executing Program
 To get started with the application, users will need to run, from the a terminal (or command prompt) in the `IMDbgame/code` directory, the command:
  ```
  python3.7 application.py
  ```
