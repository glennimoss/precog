create table bar
  ( id number
  , whee date default SYSDATE + 3
  , data varchar2(32)
);

create type test_type as object (num number(6), other2 varchar2(100));
/
