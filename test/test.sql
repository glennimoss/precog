create synonym myfoo for foo;

-- TODO: parse types so we can build hidden columns on object properties
--create index baz_idx on baz ( obj.num );

create index foo_idx on foo ( foo_id );

create table foo
  ( foo_id number
  , text vArChaR2(156) CONSTRAINT foo_pk PRIMARY KEY
  , bar_id number CONSTRAINT foo_uk_bar_id UNIQUE
  , bar_whee date
  , moredata CLOB default sysdate
  --, moredata as (18 + foo_id)
  --, id_len AS (length(to_char(foo_id)))
  , id_len number
  , id_len2 AS (length(to_char(foo_id)) - 2)
  , CONSTRAINT foo_sum CHECK (foo_id + id_len > to_number(bar_id))
  , CONSTRAINT foo_fk_bar FOREIGN KEY (bar_id, bar_whee)
    references bar (id, whee)
  , obj test_type
);

@ test2.sql

@@ test3.sql

create type gt_string is table of varchar2(100);
/

CREATE OR REPLACE PACKAGE pack AS
  /**
   * $Id: something$ --@volatile
   */
  PROCEDURE bar (
    p_param22 NUMBER
  , o_return OUT VARCHAR2
  );

  TYPE tt_foo IS TABLE OF VARCHAR2(100);
  FUNCTION foo (p_foo tt_foo) RETURN gt_string;

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

  FUNCTION foo (p_foo tt_foo) RETURN gt_string AS
    l_foo gt_string := gt_string();
  BEGIN
    l_foo.extend(p_foo.count);
    for i in 1..p_foo.count loop
      l_foo(i) := 'from foo: ' || p_foo(i);
    end loop;
    --FOR l_foo in 1..p_foo.count LOOP
      --PIPE ROW ('l_foo is ' || p_foo(l_foo));
    --END LOOP;
    return l_foo;
  END foo;
END pack;
/

create sequence the_seq increment by 9;

--create table coolbeans
  --( n number
  --, m varchar2(10)
  --, CONSTRAINT coolbeans_pk PRIMARY KEY (n, m)
--);

--@ignore awesomesauce
--@ignore awesomesauce_fk

--@ignore schema kount1_pentaho
--@ignore pfiles

--create table awesomesauce
  --( n number
  --, m varchar2(10)
  --, j clob
  --, constraint awesomesauce_pk primary key (n, m)
  --, CONSTRAINT awesomesauce_fk FOREIGN KEY (n, m) REFERENCES coolbeans (n, m)
--);

create synonym bogus_syn for nonexistent_schema.totally_bogus;

