from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

name = 'postgres'
database = 'stops'
password = '1'

db = create_engine('postgres://' + name + ':' + password + '@localhost:5432/' + database)

db.execute('DROP TABLE IF EXISTS stops_list;')
db.execute("CREATE TABLE stops_list(id NUMERIC CONSTRAINT stops_list_pk PRIMARY KEY,"
           "name VARCHAR(50) CONSTRAINT list_name_nn NOT NULL,"
           "stop_id NUMERIC CONSTRAINT list_stop_gz CHECK (stop_id > 0),"
           "city VARCHAR(30) CONSTRAINT list_city_nn NOT NULL,"
           "link TEXT CONSTRAINT list_link_nn NOT NULL);")

Base = declarative_base()


class Stop(Base):
    __tablename__ = 'stops_list'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    stop_id = Column(Integer)
    city = Column(String)
    link = Column(String)

    def __repr__(self):
        return "<Stop(id ='%s' name='%s', stop_id='%s', city='%s', link = '%s)>" % (self.id, self.name, self.stop_id, self.city, self.link)


page = 'http://www.ztm.waw.pl/'
r = requests.get('http://www.ztm.waw.pl/rozklad_nowy.php?c=183&l=1')
r.encoding = 'utf-8'

soup = BeautifulSoup(r.text, "html.parser")
stops_list = soup.findAll('div', {'class': 'PrzystanekList'})

session = sessionmaker(bind=db)
Session = session()

i = 1
for stops in stops_list:
    for stop in stops:
        for sto in stop:
            if len(sto) > 1:
                print(i, sto.contents[0], sto.get('href')[-4:],
                      sto.find('em').contents[0][1:-1], sto.get('href'))
                tStop = Stop(id=i, name=sto.contents[0], stop_id=sto.get('href')[-4:],
                             city=sto.find('em').contents[0][1:-1], link=page+sto.get('href'))
                Session.add(tStop)

                i += 1

Session.commit()