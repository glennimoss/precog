create table baz
  ( fizz varchar2(4000)
  , a number(7)
  , b number(7,9)
  , c number(*,13)
  , d number
  , e number
  , f varchar2(3)
  --, obj test_type
);

create unique index baz_fnidx on baz ( round(a + b + c + d));

create index foo_virtidx on foo (id_len);

insert into baz (fizz, a, e) values ('foo0', 9, 100);
insert into baz (fizz, a, f, e) values ('foo1', 9, 'bar', 101);
insert into baz (fizz, a, e) values ('foo2', 9, 102);
