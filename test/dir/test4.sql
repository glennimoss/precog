create TABLE here_today
  ( gone_tomorrow VARCHAR2(10) CONSTRAINT here_today_pk PRIMARY KEY
  , date_entered DATE DEFAULT SYSDATE
);

INSERT INTO here_today (gone_tomorrow) VALUES ('alpha');
INSERT INTO here_today (gone_tomorrow, date_entered)
  VALUES ('beta', '1970-01-01');
INSERT INTO here_today (gone_tomorrow) VALUES ('delta');

create index five_a_idx on five_a (n);
-- poo poo 4

@ test5.sql
@ test6.sql
