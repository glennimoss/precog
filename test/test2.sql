create table bar
  ( id number CONSTRAINT bar_id_chk check (id > 1337)
  , whee date default SYSDATE + 3
  , data varchar2(32) not null
  , obj test_type
  , CONSTRAINT bar_pk PRIMARY KEY (id, whee)
);

 @ dir/test4.sql
-- @dir/test5.sql
-- @dir/test6a.sql

-- @ ignore FARGFUG

create type test_type as object (num number(7), other2 varchar2(100));
/

create type test_garbage as object (num number(7), other2 varchar2(100));
/

create type test_table_type as table of test_type NOT Null;
/

create type test_varray as varray(13 ) of varchar2(123)
/
