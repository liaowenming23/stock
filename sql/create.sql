create database stock;
use stock;
create table stock_info(
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    stock_code varchar(8) NOT NULL,
    stock_name varchar(20) NOT NULL,
    industry_type int NOT NULL,
    create_time datetime NOT NULL
)

create table stock_revenue(
    id bigint NOT NULL PRIMARY KEY AUTO_INCREMENT,
    stock_id int NOT NULL,
    `year` smallint NOT NULL,
    `month` smallint NOT NULL,
    revenue_by_million int NOT NULL
)

create table stock_industry (
  id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `name` int NOT NULL
)