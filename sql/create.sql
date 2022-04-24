create database stock;
use stock;
create table stock_info(
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    stock_code varchar(5) NOT NULL,
    stock_name varchar(20) NOT NULL,
    industry_type int NOT NULL,
    create_time datetime NOT NULL
)

create table stock_revenue(
    id bigint NOT NULL PRIMARY KEY AUTO_INCREMENT,
    stock_id int NOT NULL,
    `year` smallint NOT NULL,
    `month` smallint NOT NULL,
    revenue int NOT NULL
)