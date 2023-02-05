-- migrate:up
create table if not exists paper
(
    paper_id           varchar                 not null
        constraint paper_pk
            primary key,
    s2ag_json_text     jsonb                   not null,
    created            timestamp default now() not null,
    updated            timestamp default now() not null,
    title              varchar,
    pub_year               integer,
    key_paper          boolean   default false,
    pdf_url            varchar,
    can_get_pdf        boolean   default null,
    local_pdf_location varchar,
    notes              varchar
);


create index paper_key_paper_index
    on paper (key_paper);

create unique index paper_paper_uindex
    on paper (paper_id);

-- migrate:down
drop table paper;
