-- migrate:up
create table if not exists author
(
    author_id           varchar                 not null
        constraint author_pk
            primary key,
    s2ag_json_text     jsonb                   not null,
    created            timestamp default now() not null,
    updated            timestamp default now() not null,
    author_name        varchar,
    notes              varchar
);

alter table author
    owner to romilly;

create unique index if not exists author_uindex
    on author (author_id);

-- migrate:down
drop table author;
