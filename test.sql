create index baz_idx on baz ( obj.num );

create unique index foo_idx on foo ( foo_id );

create table foo
  ( foo_id number
  , text vArChaR2(156)
  , bar_id varchar2(256)
  , moredata CLOB
);

create table bar
  ( id number
  , whee date default SYSDATE + 3
  , data varchar2(32)
);

create type test_type as object (num number(6), other2 varchar2(100));
/

create table baz
  ( fizz varchar2(4000)
  , a number(7)
  , b number(7,9)
  , c number(*,13)
  , e number
  , obj test_type
);

insert into baz (fizz, a, e) values ('foo', 9, 100);
insert into baz (fizz, a, e) values ('foo1', 9, 101);
insert into baz (fizz, a, e) values ('foo1', 9, 102);

CREATE OR REPLACE PACKAGE pack AS
  PROCEDURE bar (
    p_param22 NUMBER
  , o_return OUT VARCHAR2
  );

  FUNCTION foo RETURN number;
END pack;
/

CREATE OR REPLACE PACKAGE BODY pack AS
  PROCEDURE bar (
    p_param22 NUMBER
  , o_return OUT VARCHAR2
  ) IS
  BEGIN
    dbms_output.put_line(p_param22);
    o_return := 'awesome sauce';
  END bar;

  FUNCTION foo RETURN number AS
    l_latest NUMBER;
  BEGIN
    SELECT max(foo_id)
    INTO l_latest
    FROM foo;

    RETURN l_latest;
  END foo;
END pack;
/

create sequence the_seq increment by 2;
