-- migrate:up
create table if not exists citation
(
    citing_id      varchar not null,
    cited_id       varchar not null,
    is_influential boolean,
    constraint citation_pk
        primary key (citing_id, cited_id)
);

create index if not exists cited_index
    on citation (cited_id);

create index if not exists citing_index
    on citation (citing_id);

create unique index if not exists pk_index
    on citation (citing_id, cited_id);
-- migrate:down
drop table citation
