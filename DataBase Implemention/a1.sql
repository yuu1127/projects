-- COMP9311 18s2 Assignment 1
-- Schema for the myPhotos.net photo-sharing site
--
-- Written by:
--    Name:  <<Yuta Sato>>
--    Student ID:  <<z5186797>>
--    Date:  ??/09/2018
--
-- Conventions:
-- * all entity table names are plural
-- * most entities have an artifical primary key called "id"
-- * foreign keys are named after either:
--   * the relationship they represent
--   * the table being referenced

-- Domains (you may add more)

create domain URLValue as
	varchar(100) check (value like 'http://%');

create domain EmailValue as
	varchar(100) check (value like '%@%.%');

--create domain PhotoValue as
	--varchar(50) check (value like '%.jpeg'));

create domain GenderValue as
	varchar(6) check (value in ('male','female'));

create domain GroupModeValue as
	varchar(15) check (value in ('private','by-invitation','by-request'));

create domain ContactListTypeValue as
	varchar(10) check (value in ('friends','family'));

create domain SafetyLevelValue as
	varchar(15) check (value in ('safe','moderate','restricted'));

create domain VisibilityValue as
	varchar(20) check (value in ('private','friends','family','friends+family','public'));

create domain RateValue as
	integer check (value <= 5 and value >= 1);

create domain NameValue as varchar(50);

create domain LongNameValue as varchar(100);




-- Tables (you must add more)

create table People (
	id serial,--integer(negative)
	givenName NameValue not null,
	familyname NameValue,
	displayedname LongNameValue not null,
	emailaddress EmailValue not null,
	primary key (id)
	--need function
);

create table Discuusion(
	discussion_id serial,
	title NameValue,
	primary key(discussion_id)
);

create table Photos (
	photo_id serial,
	date_taken date,
	title NameValue not null,
	date_uploaded date default CURRENT_DATE,
	description text,
	technical_details text,
	safety_level SafetyLevelValue,
	visibility VisibilityValue,
	file_size integer ,--KB
	discussion_id integer,
	primary key (photo_id),
	foreign key(discussion_id) references Discuusion(discussion_id)
);


create table Users (
	user_id integer,
	website URLValue,
	date_registered text,
	gender GenderValue,
	birthday date,
	password text not null,
	photo_id integer,
	contact_id integer,
	primary key (user_id),
	foreign key (user_id) references People(id),
	foreign key (photo_id) references Photos(photo_id)
);

alter table Photos
	add column user_id integer not null
	constraint ValidUsers references Users(user_id) DEFERRABLE;

create table Groups (
	group_id serial,
	mode GroupModeValue not null,
	title text,
	user_id integer not null,
	primary key (group_id),
	foreign key (user_id) references Users(user_id)
);

create table Member_Users_Group(
	group_id integer,
	user_id integer,
	primary key(group_id,user_id),
	foreign key (group_id) references Groups(group_id),
	foreign key (user_id) references Users(user_id)
);

create table Contact_lists (
	contact_id serial,
	type ContactListTypeValue,
	title text not null,
	users_id integer not null,
	primary key (contact_id),
	foreign key(users_id) references Users(user_id)
);

--for easy to access groups of people
create table Member_Person_Contact(
	person_id integer,
	contact_list_id integer,
	primary key(person_id,contact_list_id),
	foreign key(person_id) references People(id),
	foreign key(contact_list_id) references Contact_lists(contact_id)
);


create table Rates(
	user_id integer,
	photo_id integer,
	when_rated timestamp,
	rating RateValue,
	primary key(user_id,photo_id),
	foreign key(user_id) references Users(user_id),
	foreign key(photo_id) references Photos(photo_id)
);

create table Tag(
	tag_id serial,
	tag_name NameValue not null,
	tag_freq integer check (tag_freq >= 0),
	primary key(tag_id)
);

create table Photo_has_tag(
	tag_id integer,
	photo_id integer,
	when_tagged timestamp,
	primary key(tag_id,photo_id),
	foreign key(tag_id) references Tag(tag_id),
	foreign key(photo_id) references Photos(photo_id)
);

create table Collection(
	collection_id serial,
	title NameValue not null,
	description text,
	photo_id integer not null,
	primary key(collection_id),
	foreign key(photo_id) references Photos(photo_id)
);

create table Photo_in_collection(
	photo_id integer,
	collection_id integer,
	rank_order integer,
	primary key(photo_id,collection_id),
	foreign key(photo_id) references Photos(photo_id),
	foreign key(collection_id) references Collection(collection_id)
);


create table UserCollection(
	collection_id integer,
	user_id integer,
	primary key (collection_id),
	foreign key (collection_id) references Collection(collection_id),
	foreign key (user_id) references Users(user_id)
);

create table GroupCollection(
	collection_id integer,
	group_id integer,
	primary key (collection_id),
	foreign key(collection_id) references Collection(collection_id),
	foreign key(group_id) references Groups(group_id)

);


create table Group_has_discussion(
	group_id integer,
	discussion_id integer,
	primary key(group_id,discussion_id),
	foreign key(group_id) references Groups(group_id),
	foreign key(discussion_id) references Discuusion(discussion_id)
);

create table Comment(
	comment_id serial,
	reply_id integer,
	content text,
	when_posted timestamp,
	discussion_id integer not null,
	user_id integer not null,
	primary key(comment_id),
	foreign key(reply_id) references Comment(comment_id),
	foreign key(discussion_id) references Discuusion(discussion_id),
	foreign key(user_id) references Users(user_id)

);
