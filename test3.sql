create table baz
  ( fizz varchar2(4000)
  , a number(7)
  , b number(7,9)
  , c number(*,13)
  , d number
  , e number
  , f varchar2(3)
  , g date
  , obj test_type
);

create unique index baz_fnidx on baz ( round(a + b + c + d));
create unique index baz_fnidx2 on baz ( round(a + b + c));

create index foo_virtidx on foo (id_len);

insert into baz (fizz, a, e) values ('foo0', 9, '100.00');
insert into baz (fizz, a, e) values ('foo0', 9, '100.00');
insert into baz (fizz, a, e) values ('foo0', 9, '100.00');
insert into baz (fizz, a, e) values ('foo0', 9, '100.00');
insert into baz (fizz, a, f, e) values ('foo1', 9, 'bar', 101.00);
insert into baz (fizz, a, e, g)
  values ('foo2', 9, 102.010, ' 2010-01-01    19:12:13.0');

--@ option partial_data
CREATE TABLE static_with_dynamic
  ( n NUMBER CONSTRAINT static_with_dynamic_pk PRIMARY KEY
  );

INSERT INTO static_with_dynamic (n) VALUES (1);
INSERT INTO static_with_dynamic (n) VALUES (2);
INSERT INTO static_with_dynamic (n) VALUES (3);
INSERT INTO static_with_dynamic (n) VALUES (4);
