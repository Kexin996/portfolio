# create a table for exchange
CREATE TABLE exchange (
id int NOT NULL AUTO_INCREMENT,
abbrev varchar(32) NOT NULL,
name varchar(255) NOT NULL,
city varchar(255) NULL,
country varchar(255) NULL,
currency varchar(64) NULL,
timezone_offset time NULL,
created_date datetime NOT NULL,
last_updated_date datetime NOT NULL,
PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

# create a table for data vendors
# we need support email to contact with them if we have problems
CREATE TABLE data_vendor(
id int NOT NULL AUTO_INCREMENT,
name varchar(64) NOT NULL,
website_url varchar(255) NULL,
support_email varchar(255) NULL,
created_date datetime NOT NULL,
last_updated_date datetime NOT NULL,
PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE symbol(
id int NOT NULL AUTO_INCREMENT,
exchange_id int NULL,
ticker varchar(32) NOT NULL,
instrument varchar(32) NOT NULL,
name varchar(255) NOT NULL,
sector varchar(255) NULL,
currency varchar(32) NULL,
created_date datetime NOT NULL,
last_updated_date datetime NOT NULL,
PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;