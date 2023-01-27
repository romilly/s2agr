create table schema_migrations
(
    version varchar(255) not null
        primary key
);

alter table schema_migrations
    owner to romilly;

INSERT INTO public.schema_migrations (version) VALUES ('20230126104607');
