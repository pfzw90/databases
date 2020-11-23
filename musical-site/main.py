from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

albums = [['Sleepless', 1999], ['Oxygen', 2019], ['Frozen', 2001], ['Monody', 2011], ['The Business', 2020],
          ['God Is A Dancer', 2009], ['Nothing Really Matters', 1978], ['5 Seconds Before Sunrise', 2018]]
tracks = [['Love Goes On And On', 1984, 2.22, 1], ['Mercy Mirror', 1983, 3.21, 2], ['Oblivion', 1982, 4.09, 3],
          ['Primo Victoria', 1991, 2.16, 4], ['Commotion', 1985, 3.33, 5], ['Take You Down', 1989, 3.34, 6],
          ['Read My Mind', 1988, 3.35, 7], ['My Enemy', 1988, 3.36, 8], ['Around My Heart', 1989, 2.01, 2],
          ['Return to the Sauce', 1990, 2.02, 5], ['The Calling', 1991, 5.08, 1], ['The Journey', 1992, 5.15, 5],
          ['Eternal', 1993, 1.44, 3], ['Pulsar', 1998, 5.56, 5], ['The Vulture', 2005, 3.42, 7],
          ['Fire', 2010, 1.43, 6]]
performers = ['Nirvana', 'Aerosmith', 'Little Big', 'Jack Wood', 'Motorama',
              'Elton John', 'Madonna', 'Noize MC']
genres = ['Pop', 'Rock', 'Country', 'Disco', 'Opera']
collections = [['Collection_1', 1999], ['Collection_2', 2000], ['Collection_3', 2001], ['Collection_4', 2002],
               ['Collection_5', 2019], ['Collection_6', 2009], ['Collection_7', 2020], ['Collection_8', 2018]]
performers_genres = [[1, 2], [1, 3], [2, 4], [3, 1], [4, 5], [5, 1], [5, 3], [6, 2], [7, 2], [8, 4], [8, 5]]
performers_albums = [[1, 2], [1, 2], [2, 4], [3, 3], [4, 5], [5, 1], [5, 7], [6, 8], [7, 2], [8, 7], [8, 8], [8, 6],
                     [3, 6]]
collections_tracks = [[1, 2], [1, 8], [2, 4], [3, 1], [4, 5], [5, 1], [5, 3], [6, 2], [7, 2], [8, 4], [8, 5]]

db_options = 'postgresql://postgres:admin@localhost:5432/musical_site'
db = create_engine(db_options)
base = declarative_base()


def print_result(re):
    for r in re:
        for r1 in r:
            print(r1, end=' ')
        print('')
    print('')

class Album(base):
    __tablename__ = 'album'

    album_id = Column(INTEGER, primary_key=True)
    year = Column(NUMERIC(4, 0), nullable=False)
    name = Column(VARCHAR(100), nullable=False)


class Genre(base):
    __tablename__ = 'genre'

    genre_id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(35), nullable=False)


class Track(base):
    __tablename__ = 'track'

    track_id = Column(INTEGER, primary_key=True)
    year = Column(NUMERIC(4, 0), nullable=False)
    name = Column(VARCHAR(100), nullable=False)
    duration = Column(NUMERIC(3, 2), nullable=False)
    album_id = Column(INTEGER, ForeignKey('album.album_id'), nullable=False)


class Performer(base):
    __tablename__ = 'performer'

    performer_id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(100), nullable=False, unique=True)


class PerformerGenre(base):
    __tablename__ = 'performer_genre'

    performergenre_id = Column(INTEGER, primary_key=True)
    performer_id = Column(INTEGER, ForeignKey('performer.performer_id'), nullable=False)
    genre_id = Column(INTEGER, ForeignKey('genre.genre_id'), nullable=False)


class PerformerAlbum(base):
    __tablename__ = 'performer_album'

    performeralbum_id = Column(INTEGER, primary_key=True)
    performer_id = Column(INTEGER, ForeignKey('performer.performer_id'), nullable=False)
    album_id = Column(INTEGER, ForeignKey('album.album_id'), nullable=False)


class Collection(base):
    __tablename__ = 'collection'

    collection_id = Column(INTEGER, primary_key=True)
    year = Column(NUMERIC(4, 0), nullable=False)
    name = Column(VARCHAR(100), nullable=False)


class CollectionTrack(base):
    __tablename__ = 'collection_track'

    collectiontrack_id = Column(INTEGER, primary_key=True)
    collection_id = Column(INTEGER, ForeignKey('collection.collection_id'), nullable=False)
    track_id = Column(INTEGER, ForeignKey('track.track_id'), nullable=False)


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

session.commit()

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
for p in session.execute(select([Performer.name]). \
                                 where((func.length(Performer.name) -
                                        func.length(func.replace(Performer.name, ' ', '')) + 1) == 1)):
    print(p[0])

print('Название треков, которые содержат слово "мой"/"my":')
for p in session.execute(select([Track.name]).where(func.lower(Track.name).ilike('%my%'))):
    print(p[0])

print('Количество исполнителей в каждом жанре:')
result = session.execute("""
SELECT g.name, COUNT(p.performer_id) count FROM genre g
JOIN performer_genre pg ON g.genre_id = pg.genre_id
JOIN performer p ON pg.performer_id = p.performer_id
GROUP BY  g.name
ORDER BY  count DESC;
""").fetchall()
print_result(result)

print('Количество треков, вошедших в альбомы 2019-2020 годов:')
result = session.execute("""
SELECT COUNT(t.track_id) count FROM album a
JOIN track t ON t.album_id = a.album_id
WHERE a.year >= 2019
AND a.year <= 2020;
""").fetchall()
print_result(result)

print('Средняя продолжительность треков по каждому альбому:')
result = session.execute("""
SELECT a.name, AVG(t.duration) avg FROM album a
JOIN track t ON t.album_id = a.album_id
GROUP by a.name
ORDER BY avg DESC;
""").fetchall()
print_result(result)

print('Все исполнители, которые не выпустили альбомы в 2020 году:')
result = session.execute("""
SELECT p.name FROM performer p
JOIN performer_album pa ON p.performer_id = pa.performer_id
JOIN album a ON pa.album_id = a.album_id
WHERE NOT EXISTS(SELECT * FROM performer WHERE a.year = 2020)
GROUP BY p.name
ORDER BY p.name;
""").fetchall()
print_result(result)

print('Названия сборников, в которых присутствует конкретный исполнитель:')
result = session.execute("""
SELECT c.name FROM collection c
JOIN collection_track ct ON c.collection_id = ct.collection_id
JOIN track t ON ct.track_id = t.track_id
JOIN album a ON t.album_id = a.album_id
JOIN performer_album pa ON a.album_id = pa.album_id
JOIN performer p on p.performer_id = pa.performer_id
WHERE p.name = 'Madonna'
GROUP BY c.name
ORDER BY c.name;
""").fetchall()
print_result(result)

print('Название альбомов, в которых присутствуют исполнители более 1 жанра:')
result = session.execute("""
SELECT a.name FROM album a
JOIN performer_album pa ON a.album_id = pa.album_id
JOIN performer p ON pa.performer_id = p.performer_id
JOIN performer_genre pg ON pg.performer_id = p.performer_id
JOIN genre g ON pg.genre_id = g.genre_id
GROUP BY a.name
HAVING COUNT(g.genre_id) > 1;
""").fetchall()
print_result(result)

print('Наименование треков, которые не входят в сборники:')
result = session.execute("""
SELECT t.name FROM track t
LEFT JOIN collection_track ct ON ct.track_id = t.track_id 
WHERE ct.collection_id IS NULL
GROUP BY t.name
""").fetchall()
print_result(result)

print('Имена исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может '
      'быть несколько):')
result = session.execute("""
SELECT p.name FROM performer p
JOIN performer_album pa ON p.performer_id = pa.performer_id
JOIN album a ON pa.album_id = a.album_id
JOIN track t ON t.album_id = a.album_id
WHERE t.duration = (SELECT MIN(duration) from track)
GROUP BY p.name
ORDER BY p.name
""").fetchall()
print_result(result)

print('Название альбомов, содержащих наименьшее количество треков:')
result = session.execute("""
SELECT a.name from track t 
JOIN album a ON a.album_id = t.album_id
GROUP BY a.name 
HAVING COUNT(t.track_id) = (SELECT MIN(count) FROM 
                                (SELECT album.name, COUNT(track.track_id) count FROM track
                                JOIN album ON album.album_id = track.album_id
                                GROUP BY album.name) as c
                            )
""").fetchall()
print_result(result)

session.close()
