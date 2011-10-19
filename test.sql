create synonym myfoo for foo;

create index baz_idx on baz ( obj.num );

create index foo_idx on foo ( foo_id );

create table foo
  ( foo_id number CONSTRAINT foo_pk PRIMARY KEY
  , text vArChaR2(156)
  , bar_id varchar2(256) UNIQUE
  , moredata CLOB
  , id_len AS (length(to_char(foo_id)))
  , CONSTRAINT foo_sum CHECK (foo_id + id_len > to_number(bar_id))
);

@ test2.sql

@@ test3.sql

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
