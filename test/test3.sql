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
  , o VARCHAR2(10)
  , p NUMBER
  , q VARCHAR2(10)
  );

INSERT INTO static_with_dynamic (n, o) VALUES (1, 'cat');
INSERT INTO static_with_dynamic (n, o, p, q) VALUES (2, 'doggy', 9, 'dog');
INSERT INTO static_with_dynamic (n, o, q) VALUES (3, 'mouseling', 'mouse');
INSERT INTO static_with_dynamic (n, o, p) VALUES (4, 'emu', 123);
INSERT INTO static_with_dynamic (n, o, p) VALUES (7, 'george', 23);
