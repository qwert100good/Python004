use w3h2;

create table job_info(
    `id` int auto_increment primary key,
    `city` varchar(20),
    `title` varchar(50),
    `company` varchar(50),
    `money` int
)