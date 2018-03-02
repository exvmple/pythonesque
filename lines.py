from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

name = 'postgres'
database = 'stops'
password = '1'
entity = 'lines_list'

db = create_engine('postgres://' + name + ':' + password + '@localhost:5432/' + database)

db.execute('DROP TABLE IF EXISTS '+entity+';')
db.execute("CREATE TABLE "+entity+"(id NUMERIC CONSTRAINT lines_list_pk PRIMARY KEY,"
           "line_name VARCHAR(5) CONSTRAINT lines_name_nn NOT NULL,"
           "link TEXT CONSTRAINT lines_link_nn NOT NULL);")

Base = declarative_base()


class Line(Base):
    __tablename__ = entity
    id = Column(Integer, primary_key=True)
    line_name = Column(String)
    link = Column(String)

    def __repr__(self):
        return "<Line(id ='%s' line_name='%s', link = '%s)>" % (self.id, self.line_name, self.link)


page = 'http://www.ztm.waw.pl/'
r = requests.get('http://www.ztm.waw.pl/rozklad_nowy.php?c=182&l=1')
r.encoding = 'utf-8'

soup = BeautifulSoup(r.text, "html.parser")
lines_list = soup.findAll('div', {'class': 'LineList'})

session = sessionmaker(bind=db)
Session = session()

i = 1
for lines in lines_list:
    for lin in lines:
        if len(lin.contents) > 0 and isinstance(lin.get('href'),str):
            print(lin.contents[0], page+str(lin.get('href')))
            tLine = Line(id=i, line_name=lin.contents[0], link=page+lin.get('href'))
            Session.add(tLine)

            i += 1

Session.commit()
