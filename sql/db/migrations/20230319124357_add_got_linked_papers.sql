-- migrate:up
alter table paper
    add if not exists got_linked_papers boolean default false not null;

-- migrate:down

alter table paper
    drop column got_linked_papers;