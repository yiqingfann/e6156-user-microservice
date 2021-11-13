create schema e6156;

create table e6156.address
(
	addr_id int auto_increment
		primary key,
	street_line_1 varchar(255) null,
	street_line_2 varchar(255) null,
	city varchar(255) null,
	state varchar(255) null,
	zip_code int null
);

create table e6156.user
(
	user_id int auto_increment
		primary key,
	first_name varchar(255) null,
	last_name varchar(255) null,
	email varchar(255) null,
	addr_id int null,
	constraint user_email_uindex
		unique (email),
	constraint user_address_addr_id_fk
		foreign key (addr_id) references e6156.address (addr_id)
);



