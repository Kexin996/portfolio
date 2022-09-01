# create an amazon sql table
CREATE TABLE test.AMZN
(
	dt timestamp without time zone NOT NULL,
	high numeric NOT NULL,
	low numeric NOT NULL,
	open numeric NOT NULL,
	close numeric NOT NULL,
	volume numeric NOT NULL,
	adj close numeric NOT NULL,
	PRIMARY KEY (dt) # primary key: uniquely identify each row in a table
);
