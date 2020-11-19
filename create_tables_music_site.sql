create table if not exists Genre(
	Id serial primary key,
	Name varchar(35) not null
);

create table if not exists Performer(
	Id serial primary key,
	Name varchar(35) not null unique,
	GenreId integer references Genre(Id) not null
);

create table if not exists Album(
	Id serial primary key,
	Year numeric(4,0) not null,
	Name varchar(100) not null,
	PerformerId integer references Performer(Id) not null
);

create table if not exists Track(
	Id serial primary key,
	Year numeric(4,0) not null,
	Name varchar(100) not null,
	AlbumId integer references Album(Id)
);

