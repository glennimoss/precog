@ gim.sql

CREATE TABLE tab1
  ( a NUMBER
  , b NUMBER
  , c NUMBER
  , d NUMBER
  , e NUMBER
  , f NUMBER
  , CONSTRAINT tab1_uk1 UNIQUE (a, b)
  , CONSTRAINT tab1_uk3 UNIQUE (a, b, c)
  , CONSTRAINT tab1_uk4 UNIQUE (a, b, c, d)
  , CONSTRAINT tab1_uk2 UNIQUE (a, b, c, d, e)
  );

INSERT INTO tab1 (a, b, c, d, e, f)
VALUES (1, 2, 3, 4, 5, 6);
INSERT INTO tab1 (a, b, c)
VALUES (2, 3, 4);
INSERT INTO tab1 (a)
VALUES (1);

CREATE TABLE tab2
  ( a NUMBER DEFAULT 10
  , b NUMBER
  , c NUMBER DEFAULT 20
  , d NUMBER
  , e NUMBER
  , f NUMBER
  , CONSTRAINT tab2_pk PRIMARY KEY (a, b, c)
  , CONSTRAINT tab2_uk UNIQUE (a, b)
  );

INSERT INTO tab2 (b)
VALUES (1);
INSERT INTO tab2 (a, b)
VALUES (1, 2);

CREATE TABLE tab3
  ( a NUMBER DEFAULT 10
  , b NUMBER DEFAULT 20
  , c NUMBER DEFAULT 30
  , d NUMBER DEFAULT 40
  , e NUMBER DEFAULT 50
  , f NUMBER
  , CONSTRAINT tab3_pk PRIMARY KEY (a, b, c, d, e)
  --, CONSTRAINT tab3_pk PRIMARY KEY (a, b, c, d)
  );

INSERT INTO tab3 (c)
VALUES (1);
