create table if not exists Album(
	Id serial primary key,
	Year numeric(4,0) not null,
	Name varchar(100) not null
);

create table if not exists Track(
	Id serial primary key,
	Year numeric(4,0) not null,
	Name varchar(100) not null,
	AlbumId integer references Album(Id)
);

create table if not exists Genre(
	Id serial primary key,
	Name varchar(35) not null
);

create table if not exists Performer(
	Id serial primary key,
	Name varchar(35) not null unique,
	GenreId integer references Genre(Id) not null
);

create table if not exists Performer_Genre(
	Id serial primary key,
	PerformerId integer references Performer(Id) not null,
	GenreId integer references Genre(Id) not null
);

create table if not exists Performer_Album(
	Id serial primary key,
	PerformerId integer references Performer(Id) not null,
	AlbumId integer references Album(Id) not null
);

create table if not exists Collection(
	Id serial primary key,
	Name varchar(100) not null,
	Year numeric(4,0) not null
);

create table if not exists Collection_Tracks(
	Id serial primary key,
	CollectionId integer references Collection(Id) not null,
	TrackId integer references Track(Id) not null
);

