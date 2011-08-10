create index foo_idx on foo ( id );

create table foo
  ( id number
  , text vArChaR2(256)
  , moredata CLOB
);

create table bar
  ( bar_id number
  , when date default SYSDATE + 3
  , data varchar2(32)
);

create table baz
  ( fizz varchar2(4000)
  , a number(7)
  , b number(7,9)
  , c number(*,13)
);

insert into baz (fizz, a) values ('foo', 9);
insert into baz (fizz, a) values ('foo1', 9);
insert into baz (fizz, a) values ('foo1', 9);

