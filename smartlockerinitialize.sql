drop table if exists failopen ;
drop table if exists nfcopen;
drop table if exists nfcinfo;
drop table if exists ownerinfo;
create table ownerinfo(
    id integer primary key,
    name text not null ,
    perferWay integer not null ,
    email text
);
create table nfcinfo(
    id integer,
    uid text primary key,
    foreign key (id) references ownerinfo(id)
);
create table nfcopen(
    nfcoid integer primary key autoincrement ,
    uid text,
    opentime datetime DEFAULT (datetime('now', 'localtime')),
    foreign key (uid) references nfcinfo(uid)
);
create table failopen(
    uid text,
    failtime datetime DEFAULT (datetime('now', 'localtime')),
    foid integer primary key autoincrement
);

