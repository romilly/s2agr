-- migrate:up
alter table wrote
    drop constraint wrote_author_author_id_fk;

-- migrate:down
alter table wrote
    add constraint wrote_author_author_id_fk
        foreign key (author_id) references author;

