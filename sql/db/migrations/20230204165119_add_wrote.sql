-- migrate:up
create table if not exists wrote
(
    author_id varchar not null
        constraint wrote_author_author_id_fk
            references author,
    paper_id  varchar not null
        constraint wrote_paper_paper_id_fk
            references paper,
    constraint wrote_pk
        primary key (author_id, paper_id)
);

create index if not exists wrote_paper_id_index
    on wrote (paper_id);

create index if not exists wrote_author_id_index
    on wrote (author_id);

create unique index if not exists wrote_uindex
    on wrote (author_id, paper_id);


-- migrate:down
drop table wrote;
