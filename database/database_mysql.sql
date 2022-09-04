# create a database for storing data for S&P 500

# create a table for exchange
# where to trade it
# we need to use backticks 
# or the auto_increment will not work normally...
CREATE TABLE `exchange`(
`id` int NOT NULL AUTO_INCREMENT,
`abbrev` varchar(32) NOT NULL,
`name` varchar(255) NOT NULL,
`city` varchar(255) NULL,
`country` varchar(255) NULL,
`currency` varchar(64) NULL,
`timezone_offset` time NULL,
`created_date` datetime NOT NULL,
`last_updated_date` datetime NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

# create a table for data vendors
# we need support email to contact with them if we have problems
# where its data comes from
CREATE TABLE `data_vendor`(
`id` int NOT NULL AUTO_INCREMENT,
`name` varchar(64) NOT NULL,
`website_url` varchar(255) NULL,
`support_email` varchar(255) NULL,
`created_date` datetime NOT NULL,
`last_updated_date` datetime NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

# create a table for our assets' symbols
# what it is
CREATE TABLE `symbol`(
`id` int NOT NULL AUTO_INCREMENT,
`exchange_id` int NULL,
`ticker` varchar(32) NOT NULL,
`instrument` varchar(32) NOT NULL,
`name` varchar(255) NOT NULL,
`sector` varchar(255) NULL,
`currency` varchar(32) NULL,
`created_date` datetime NOT NULL,
`last_updated_date` datetime NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

# create a table for price
# its price history

# decimal [(p [,s])]:
# p: total number of digits
# s: number of digits after decimal points

# bigint: 8 bytes

# we define other two keys for easier query
CREATE TABLE `daily_price`(
`id` int NOT NULL AUTO_INCREMENT,
`data_vendor_id` int NOT NULL,
`symbol_id` int NOT NULL,
`price_date` datetime NOT NULL,
`created_date` datetime NOT NULL,
`last_updated_date` datetime NOT NULL,
`open_price` decimal(19,4) NULL,
`high_price` decimal(19,4) NULL,
`low_price` decimal(19,4) NULL,
`close_price` decimal(19,4) NULL,
`adj_close_price` decimal(19,4) NULL,
`volume` bigint NULL,
PRIMARY KEY (`id`),
KEY `index_data_vendor_id` (`data_vendor_id`),
KEY `index_symbol_id` (`symbol_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

