# pythonesque
Various Python scripts

main.py parses a page with the list of bus stops in Warsaw and records it to a PostgreSQL database.

lines.py parses a page with the list of bus lines in Warsaw and records it to a PostgreSQL database.

both scripts use requests to fetch a page, BeautifulSoup to parse the page, SQLAlchemy to write the data to the database.
