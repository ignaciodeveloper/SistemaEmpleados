create database if no exists sistema;
use sistema;
drop table if exists empleados;

create table empleados (
    id int not null auto_increment,
    nombre varchar (255),
    correo varchar (255),
    foto varchar(5000), 
    primary key (id)
);