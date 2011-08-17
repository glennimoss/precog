create index bar_idx on bar ( id);

create table foo
  ( id number
  , text vArChaR2(156)
  , bar_id varchar2(256)
  , moredata CLOB
);

create table bar
  ( id number
  , whee date default SYSDATE + 3
  , data varchar2(32)
);

create type test_type as object (num number, other2 varchar2(100));
/

create table baz
  ( fizz varchar2(4000)
  , a number(7)
  , b number(7,9)
  , c number(*,13)
  , obj test_type
);

insert into baz (fizz, a) values ('foo', 9);
insert into baz (fizz, a) values ('foo1', 9);
insert into baz (fizz, a) values ('foo1', 9);

CREATE OR REPLACE PACKAGE pack AS
  PROCEDURE bar (
    p_param22 NUMBER
  , o_return OUT VARCHAR2
  );
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
END pack;
/

create sequence the_seq increment by 2;
