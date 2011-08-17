create unique index foo_idx on foo F ( "F".id );

create table foo
  ( id number
  , text vArChaR2(256)
  , moredata CLOB
);

create table bar
  ( bar_id number
  , whee date default SYSDATE + 3
  , data varchar2(32)
);

create table baz
  ( fizz varchar2(4000)
  , a number(7)
  , b number(7,9)
  , c number(*,13)
);

insert into baz (fizz, a) values ('foo', 9);
insert in!to baz (fizz, a) values ('foo1', 9);
insert into baz (fizz, a) values ('foo1', 9);

CREATE OR REPLACE PACKAGE pack AS
  PROCEDURE bar (
    p_param NUMBER
  , o_return OUT VARCHAR2
  );
END pack;
/

create;
CREATE OR REPLACE PACKAGE BODY pack AS
  PROCEDURE bar (
    p_param NUMBER
    o_return OUT VARCHAR2
  ) IS
  BEGIN
    dbms_output.put_line(p_param);
    o_return := 'awesome sauce';
  END bar;
END pack;
/
