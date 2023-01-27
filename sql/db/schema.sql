SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: citation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.citation (
    citing_id character varying NOT NULL,
    cited_id character varying NOT NULL,
    is_influential boolean
);


--
-- Name: paper; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.paper (
    paper_id character varying NOT NULL,
    s2ag_json_text jsonb NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    updated timestamp without time zone DEFAULT now() NOT NULL,
    title character varying,
    pub_year integer,
    key_paper boolean DEFAULT false,
    pdf_url character varying,
    can_get_pdf boolean,
    local_pdf_location character varying,
    notes character varying
);


--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying(255) NOT NULL
);


--
-- Name: citation citation_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citation
    ADD CONSTRAINT citation_pk PRIMARY KEY (citing_id, cited_id);


--
-- Name: paper paper_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paper
    ADD CONSTRAINT paper_pk PRIMARY KEY (paper_id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: cited_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cited_index ON public.citation USING btree (cited_id);


--
-- Name: citing_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX citing_index ON public.citation USING btree (citing_id);


--
-- Name: paper_key_paper_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX paper_key_paper_index ON public.paper USING btree (key_paper);


--
-- Name: paper_paper_uindex; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX paper_paper_uindex ON public.paper USING btree (paper_id);


--
-- Name: pk_index; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX pk_index ON public.citation USING btree (citing_id, cited_id);


--
-- PostgreSQL database dump complete
--


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('20230126104607'),
    ('20230127121805'),
    ('20230127171102'),
    ('20230127172342');
