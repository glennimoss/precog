create table bar
  ( id number check (id > 1337)
  , whee date default SYSDATE + 3
  , data varchar2(32) not null
  , CONSTRAINT bar_pk PRIMARY KEY (id, whee)
);

create type test_type as object (num number(6), other2 varchar2(100));
/
