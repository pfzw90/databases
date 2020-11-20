from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

albums = [['Sleepless', 1999], ['Oxygen', 2000], ['Frozen', 2001], ['Monody', 2002], ['The Business', 2003],
          ['God Is A Dancer', 2009], ['Nothing Really Matters', 1978], ['5 Seconds Before Sunrise', 2018]]
tracks = [['Love Goes On And On', 1984, 2.22, 1], ['Mercy Mirror', 1983, 3.21, 2], ['Oblivion', 1982, 4.09, 3],
          ['Primo Victoria', 1991, 2.16, 4], ['Commotion', 1985, 3.33, 5], ['Take You Down', 1989, 3.34, 6],
          ['Read My Mind', 1988, 3.35, 7], ['My Enemy', 1988, 3.36, 8], ['Around My Heart', 1989, 2.01, 7],
          ['Return to the Sauce', 1990, 2.02, 6], ['The Calling', 1991, 5.08, 1], ['The Journey', 1992, 5.15, 5],
          ['Eternal', 1993, 1.44, 3], ['Pulsar', 1998, 5.56, 1], ['The Vulture', 2005, 3.42, 7],
          ['Fire', 2010, 1.43, 6]]
performers = ['Nirvana', 'Aerosmith', 'Little Big', 'Jack Wood', 'Motorama',
              'Elton John', 'Madonna', 'Noize MC']
genres = ['Pop', 'Rock', 'Country', 'Disco', 'Opera']
collections = [['Collection_1', 1999], ['Collection_2', 2000], ['Collection_3', 2001], ['Collection_4', 2002],
               ['Collection_5', 2019], ['Collection_6', 2009], ['Collection_7', 2020], ['Collection_8', 2018]]
performers_genres = [[1, 2], [1, 3], [2, 4], [3, 1], [4, 5], [5, 1], [5, 3], [6, 2], [7, 2], [8, 4], [8, 5]]
performers_albums = [[1, 2], [1, 2], [2, 4], [3, 3], [4, 5], [5, 1], [5, 7], [6, 8], [7, 2], [8, 7], [8, 8]]
collections_tracks = [[1, 2], [1, 8], [2, 4], [3, 1], [4, 5], [5, 1], [5, 3], [6, 2], [7, 2], [8, 4], [8, 5]]

db_options = 'postgresql://postgres:admin@localhost:5432/musical_site'
db = create_engine(db_options)
base = declarative_base()


class Album(base):
    __tablename__ = 'Album'

    id = Column(INTEGER, primary_key=True)
    year = Column(NUMERIC(4, 0), nullable=False)
    name = Column(VARCHAR(100), nullable=False)


class Genre(base):
    __tablename__ = 'Genre'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(35), nullable=False)


class Track(base):
    __tablename__ = 'Track'

    id = Column(INTEGER, primary_key=True)
    year = Column(NUMERIC(4, 0), nullable=False)
    name = Column(VARCHAR(100), nullable=False)
    duration = Column(NUMERIC(3, 2), nullable=False)
    album_id = Column(INTEGER, nullable=False)


class Performer(base):
    __tablename__ = 'Performer'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(100), nullable=False, unique=True)


class PerformerGenre(base):
    __tablename__ = 'Performer_Genre'

    id = Column(INTEGER, primary_key=True)
    performer_id = Column(INTEGER, nullable=False)
    genre_id = Column(INTEGER, nullable=False)


class PerformerAlbum(base):
    __tablename__ = 'Performer_Album'

    id = Column(INTEGER, primary_key=True)
    performer_id = Column(INTEGER, nullable=False)
    album_id = Column(INTEGER, nullable=False)


class Collection(base):
    __tablename__ = 'Collection'

    id = Column(INTEGER, primary_key=True)
    year = Column(NUMERIC(4, 0), nullable=False)
    name = Column(VARCHAR(100), nullable=False)


class CollectionTrack(base):
    __tablename__ = 'Collection_Track'

    id = Column(INTEGER, primary_key=True)
    collection_id = Column(INTEGER, nullable=False)
    track_id = Column(INTEGER, nullable=False)


Session = sessionmaker(db)
session = Session()
base.metadata.create_all(db)

for a in albums:
    album = Album(name=a[0], year=a[1])
    session.add(album)

for p in performers:
    performer = Performer(name=p)
    session.add(performer)

for g in genres:
    genre = Genre(name=g)
    session.add(genre)

for c in collections:
    collection = Collection(name=c[0], year=c[1])
    session.add(collection)

for t in tracks:
    track = Track(name=t[0], year=t[1], duration=t[2], album_id=t[3])
    session.add(track)

for pg in performers_genres:
    perf_genre = PerformerGenre(performer_id=pg[0], genre_id=pg[1])
    session.add(perf_genre)

for pa in performers_albums:
    perf_album = PerformerAlbum(performer_id=pa[0], album_id=pa[1])
    session.add(perf_album)

for ct in collections_tracks:
    collection_track = CollectionTrack(collection_id=ct[0], track_id=ct[1])
    session.add(collection_track)

session.commit()

print('Название и год выхода альбомов, вышедших в 2018 году:')
for p in session.execute(select([Album.name, Album.year]).where(Album.year == '2018')):
    print(f'{p[0]}, {p[1]}')

print('Название и продолжительность самого длительного трека:')
res = session.execute(select([Track.name, Track.duration]).order_by(-Track.duration)).fetchone()
print(f'{res[0]}, {str(res[1])}')

print('Название треков, продолжительность которых не менее 3,5 минуты:')
for p in session.execute(select([Track.name]).where(Track.duration >= 3.30).order_by(Track.name)):
    print(p[0])

print('Названия сборников, вышедших в период с 2018 по 2020 год включительно:')
for p in session.execute(select([Collection.name]). \
                                 where(and_(Collection.year >= 2018, Collection.year <= 2020)). \
                                 order_by(Collection.year)):
    print(p[0])

print('Исполнители, чье имя состоит из 1 слова:')
for p in session.execute(select([Performer.name]).where((func.length(Performer.name) -
                                                         func.length(func.replace(Performer.name, ' ', '')) + 1) == 1)):
    print(p[0])


print('Название треков, которые содержат слово "мой"/"my":')
for p in session.execute(select([Track.name]).where(func.lower(Track.name).ilike('%my%'))):
    print(p[0])

session.close()
