create table comments
(
    id         int auto_increment primary key,
    movie_name char(20),
    shorts     varchar(400),
    stars      int,
    votes      int,
    sentiments decimal(8, 6),
    comment_time date
)