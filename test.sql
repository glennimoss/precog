--create index foo_idx on foo ( id );

create table foo
  ( id number
  , text vArChaR2(128)
);

create table bar
  ( bar_id number
  , when date default sysdate
  , data varchar2(32)
);

create table baz
  ( fizz varchar2(4000)
  , a number(7)
  , b number(7,9)
  , c number(*,13)
);
