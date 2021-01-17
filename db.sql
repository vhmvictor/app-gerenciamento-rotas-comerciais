--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

-- Started on 2021-01-16 23:52:04

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
-- TOC entry 207 (class 1259 OID 16965)
-- Name: cliente; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cliente (
    id integer NOT NULL,
    nome text NOT NULL,
    geolocalizacao double precision[] NOT NULL,
    rota_id integer NOT NULL,
    vendedor_id integer,
    data_criacao timestamp without time zone,
    data_atualizacao timestamp without time zone,
    data_deletacao timestamp without time zone
);


--
-- TOC entry 206 (class 1259 OID 16963)
-- Name: cliente_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cliente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3047 (class 0 OID 0)
-- Dependencies: 206
-- Name: cliente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cliente_id_seq OWNED BY public.cliente.id;


--
-- TOC entry 210 (class 1259 OID 16999)
-- Name: log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.log (
    id integer NOT NULL,
    acao text,
    entidade text,
    usuario_id integer,
    usuario_nome text,
    registro text,
    data_criacao timestamp without time zone
);


--
-- TOC entry 209 (class 1259 OID 16997)
-- Name: log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3048 (class 0 OID 0)
-- Dependencies: 209
-- Name: log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.log_id_seq OWNED BY public.log.id;


--
-- TOC entry 205 (class 1259 OID 16830)
-- Name: rota; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rota (
    id integer NOT NULL,
    bounds double precision[] NOT NULL,
    nome text NOT NULL,
    vendedor_id integer,
    data_criacao timestamp without time zone,
    data_atualizacao timestamp without time zone,
    data_deletacao timestamp without time zone
);


--
-- TOC entry 204 (class 1259 OID 16828)
-- Name: rota_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rota_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3049 (class 0 OID 0)
-- Dependencies: 204
-- Name: rota_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rota_id_seq OWNED BY public.rota.id;


--
-- TOC entry 201 (class 1259 OID 16621)
-- Name: usuario; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuario (
    id integer NOT NULL,
    email text NOT NULL,
    senha text NOT NULL,
    nome text NOT NULL,
    is_adm boolean NOT NULL,
    status integer NOT NULL,
    data_criacao timestamp without time zone,
    data_atualizacao timestamp without time zone
);


--
-- TOC entry 200 (class 1259 OID 16619)
-- Name: usuario_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3050 (class 0 OID 0)
-- Dependencies: 200
-- Name: usuario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.usuario_id_seq OWNED BY public.usuario.id;


--
-- TOC entry 203 (class 1259 OID 16654)
-- Name: vendedor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vendedor (
    id integer NOT NULL,
    nome text NOT NULL,
    email text NOT NULL,
    data_criacao timestamp without time zone,
    data_atualizacao timestamp without time zone,
    data_deletacao timestamp without time zone
);


--
-- TOC entry 208 (class 1259 OID 16989)
-- Name: v_cliente; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_cliente AS
 SELECT cliente.id,
    cliente.nome,
    cliente.geolocalizacao,
    cliente.rota_id,
    rota.nome AS rota_nome,
    cliente.vendedor_id,
    vendedor.nome AS vendedor_nome,
    vendedor.email AS vendedor_email,
    cliente.data_criacao,
    cliente.data_atualizacao,
    cliente.data_deletacao
   FROM ((public.cliente
     JOIN public.rota ON ((cliente.rota_id = rota.id)))
     JOIN public.vendedor ON ((cliente.vendedor_id = vendedor.id)))
  WHERE (cliente.data_deletacao IS NULL)
  ORDER BY cliente.nome;


--
-- TOC entry 202 (class 1259 OID 16652)
-- Name: vendedor_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.vendedor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3051 (class 0 OID 0)
-- Dependencies: 202
-- Name: vendedor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.vendedor_id_seq OWNED BY public.vendedor.id;


--
-- TOC entry 2886 (class 2604 OID 16968)
-- Name: cliente id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cliente ALTER COLUMN id SET DEFAULT nextval('public.cliente_id_seq'::regclass);


--
-- TOC entry 2887 (class 2604 OID 17002)
-- Name: log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.log ALTER COLUMN id SET DEFAULT nextval('public.log_id_seq'::regclass);


--
-- TOC entry 2885 (class 2604 OID 16833)
-- Name: rota id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rota ALTER COLUMN id SET DEFAULT nextval('public.rota_id_seq'::regclass);


--
-- TOC entry 2883 (class 2604 OID 16624)
-- Name: usuario id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);


--
-- TOC entry 2884 (class 2604 OID 16657)
-- Name: vendedor id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vendedor ALTER COLUMN id SET DEFAULT nextval('public.vendedor_id_seq'::regclass);


--
-- TOC entry 3039 (class 0 OID 16965)
-- Dependencies: 207
-- Data for Name: cliente; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.cliente (id, nome, geolocalizacao, rota_id, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (5, 'loja sudoeste 2', '{-49.29016113281249,-16.69531186055323}', 3, 6, '2021-01-14 16:09:07.852941', NULL, NULL);
INSERT INTO public.cliente (id, nome, geolocalizacao, rota_id, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (6, 'loja sudoeste 3', '{-49.30088996887207,-16.69835370186849}', 3, 6, '2021-01-14 16:09:19.361582', NULL, NULL);
INSERT INTO public.cliente (id, nome, geolocalizacao, rota_id, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (7, 'loja sudoeste 4', '{-49.2971134185791,-16.69309210794294}', 3, 6, '2021-01-14 16:09:31.634128', NULL, NULL);
INSERT INTO public.cliente (id, nome, geolocalizacao, rota_id, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (10, 'loja setor bueno 3', '{-49.273080825805664,-16.698435913123625}', 6, 7, '2021-01-14 16:10:53.514878', NULL, '2021-01-14 17:15:59.912147');
INSERT INTO public.cliente (id, nome, geolocalizacao, rota_id, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (4, 'loja sudoeste', '{-49.30088996887207,-16.690296827230053}', 3, 6, '2021-01-14 16:08:54.849973', '2021-01-15 21:02:38.72483', NULL);
INSERT INTO public.cliente (id, nome, geolocalizacao, rota_id, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (1, 'loja vila uniao', '{-49.30440902709961,-16.717343561447013}', 4, 6, '2021-01-14 16:05:09.063223', '2021-01-15 21:07:33.971655', NULL);
INSERT INTO public.cliente (id, nome, geolocalizacao, rota_id, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (2, 'loja vila uniao 2 ', '{-49.313249588012695,-16.7106849946083}', 4, 6, '2021-01-14 16:05:29.964712', '2021-01-15 21:07:33.971655', NULL);
INSERT INTO public.cliente (id, nome, geolocalizacao, rota_id, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (3, 'loja vila uniao 3', '{-49.2996883392334,-16.7113426411802}', 4, 6, '2021-01-14 16:05:42.17385', '2021-01-15 21:07:33.971655', NULL);
INSERT INTO public.cliente (id, nome, geolocalizacao, rota_id, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (8, 'loja setor bueno', '{-49.273338317871094,-16.688570309891823}', 6, 10, '2021-01-14 16:10:31.393169', '2021-01-15 21:17:49.4579', NULL);
INSERT INTO public.cliente (id, nome, geolocalizacao, rota_id, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (9, 'loja setor bueno 2', '{-49.27651405334472,-16.69333874839548}', 6, 10, '2021-01-14 16:10:42.680828', '2021-01-15 21:17:49.4579', NULL);
INSERT INTO public.cliente (id, nome, geolocalizacao, rota_id, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (11, 'loja parque amazonia', '{-49.287071228027344,-16.719809638339907}', 9, 5, '2021-01-14 16:11:50.830476', '2021-01-15 23:33:12.003192', NULL);
INSERT INTO public.cliente (id, nome, geolocalizacao, rota_id, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (12, 'loja parque amazonia 2', '{-49.281578063964844,-16.724412896562786}', 9, 5, '2021-01-14 16:12:01.187001', '2021-01-15 23:33:12.003192', NULL);
INSERT INTO public.cliente (id, nome, geolocalizacao, rota_id, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (13, 'loja parque amazonia 3', '{-49.27076339721679,-16.724906096210493}', 9, 5, '2021-01-14 16:12:11.254486', '2021-01-15 23:33:12.003192', NULL);
INSERT INTO public.cliente (id, nome, geolocalizacao, rota_id, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (14, 'loja parque amazonia 4', '{-49.28363800048828,-16.73156416658138}', 9, 5, '2021-01-14 16:12:23.743644', '2021-01-15 23:33:12.003192', NULL);
INSERT INTO public.cliente (id, nome, geolocalizacao, rota_id, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (15, 'loja teste', '{-49.27445411682129,-16.72918043971581}', 9, 5, '2021-01-16 22:15:21.670308', NULL, NULL);


--
-- TOC entry 3041 (class 0 OID 16999)
-- Dependencies: 210
-- Data for Name: log; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3037 (class 0 OID 16830)
-- Dependencies: 205
-- Data for Name: rota; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.rota (id, bounds, nome, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (9, '{{-49.291534423828125,-16.718987616251404},{-49.29616928100586,-16.723097691265785},{-49.29642677307128,-16.72778306872881},{-49.28664207458496,-16.73361907960675},{-49.27831649780273,-16.736413725761974},{-49.26741600036621,-16.735838360786456},{-49.2641544342041,-16.72959142923318},{-49.26398277282715,-16.721864678061696},{-49.274024963378906,-16.71701474878583},{-49.27908897399902,-16.717507967565055},{-49.291534423828125,-16.718987616251404}}', 'Parque Amazonia', 5, '2021-01-14 02:10:23.788181', '2021-01-15 23:33:12.003192', NULL);
INSERT INTO public.rota (id, bounds, nome, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (10, '{{-49.31196212768555,-16.684377274280234},{-49.30706977844238,-16.68692599316398},{-49.2996883392334,-16.683226228806877},{-49.29685592651367,-16.681088554541905},{-49.30294990539551,-16.67738867722211},{-49.31084632873535,-16.67689535483771},{-49.31196212768555,-16.684377274280234}}', 'teste', NULL, '2021-01-16 22:11:31.888048', NULL, NULL);
INSERT INTO public.rota (id, bounds, nome, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (5, '{{-49.29385185241699,-16.704519447795242},{-49.29247856140136,-16.708712041295648},{-49.29110527038574,-16.71224690151613},{-49.291791915893555,-16.716274918226052},{-49.291019439697266,-16.71791898224031},{-49.28569793701172,-16.717836779376103},{-49.28046226501464,-16.71709695200426},{-49.27617073059082,-16.713644386334302},{-49.27574157714844,-16.709534107654456},{-49.27814483642578,-16.705094907256843},{-49.28071975708008,-16.700573393335922},{-49.28466796875,-16.7013132847586},{-49.28655624389648,-16.703039686929532},{-49.293251037597656,-16.704519447795242},{-49.29385185241699,-16.704519447795242}}', 'Jardim América', NULL, '2021-01-14 01:09:00.407933', '2021-01-14 05:07:32.356933', '2021-01-14 05:07:50.967643');
INSERT INTO public.rota (id, bounds, nome, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (2, '{{-49.27522659301758,-16.708547627599017},{-49.27539825439453,-16.713726591004885},{-49.27642822265625,-16.71504186091754},{-49.27668571472167,-16.716110511045358},{-49.27666425704956,-16.717035299593757},{-49.27396059036255,-16.7167270372424},{-49.271321296691895,-16.717960083659126},{-49.26621437072754,-16.720138446183366},{-49.26389694213867,-16.72087826175867},{-49.26003456115723,-16.717836779376103},{-49.25797462463379,-16.71495965681362},{-49.25797462463379,-16.70994513950608},{-49.26046371459961,-16.70698569041774},{-49.26424026489258,-16.706492444442098},{-49.2711067199707,-16.708444868966694},{-49.27522659301758,-16.708547627599017}}', 'Nova Suíça', NULL, '2021-01-14 00:53:48.798189', '2021-01-14 03:44:20.383371', '2021-01-14 04:03:22.371213');
INSERT INTO public.rota (id, bounds, nome, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (1, '{}', 'Outros', NULL, '2021-01-14 00:49:18.609548', '2021-01-14 04:24:48.651768', NULL);
INSERT INTO public.rota (id, bounds, nome, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (4, '{{-49.31058883666992,-16.704437239159116},{-49.32088851928711,-16.709534107654456},{-49.31985855102539,-16.716603732162383},{-49.314022064208984,-16.72054945519059},{-49.30131912231445,-16.724330696497493},{-49.29342269897461,-16.71939862773847},{-49.292049407958984,-16.71232910678873},{-49.293999999999,-16.705996583591286},{-49.31058883666992,-16.704437239159116}}', 'Vila União', 6, '2021-01-14 01:07:05.476611', '2021-01-15 21:07:33.971655', NULL);
INSERT INTO public.rota (id, bounds, nome, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (6, '{{-49.27496910095215,-16.683390664298805},{-49.27891731262207,-16.686268262511895},{-49.283037185668945,-16.68914581740434},{-49.28492546081543,-16.69087232954314},{-49.28286552429199,-16.694243093997365},{-49.28097724914551,-16.70016234130687},{-49.27968978881836,-16.700984444480216},{-49.27831649780273,-16.70361515085119},{-49.276857376098626,-16.70616361308363},{-49.27599906921387,-16.7078077642116},{-49.27187919616699,-16.708301006788517},{-49.267845153808594,-16.70698569041774},{-49.26363945007324,-16.7056703649839},{-49.26166534423828,-16.70386177771524},{-49.26072120666504,-16.700573393335922},{-49.25926208496093,-16.695887347760515},{-49.25823211669922,-16.6892280326218},{-49.261322021484375,-16.686268262511895},{-49.26647186279297,-16.684212839636928},{-49.27162170410156,-16.68306179317352},{-49.27496910095215,-16.683390664298805}}', 'Setor Bueno', 10, '2021-01-14 01:11:17.637842', '2021-01-15 21:17:49.4579', NULL);
INSERT INTO public.rota (id, bounds, nome, vendedor_id, data_criacao, data_atualizacao, data_deletacao) VALUES (3, '{{-49.307498931884766,-16.68815923203611},{-49.31093215942383,-16.69522964795351},{-49.309558868408196,-16.704108404260715},{-49.29840087890625,-16.704930490444795},{-49.2875862121582,-16.702628640209362},{-49.28277969360351,-16.69539407311755},{-49.29136276245117,-16.685199445375137},{-49.29840087890625,-16.683226228806877},{-49.307498931884766,-16.68815923203611}}', 'Sudoeste', 6, '2021-01-14 01:01:27.935309', '2021-01-14 15:22:27.110471', NULL);


--
-- TOC entry 3033 (class 0 OID 16621)
-- Dependencies: 201
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.usuario (id, email, senha, nome, is_adm, status, data_criacao, data_atualizacao) VALUES (1, 'victor@teste.com', '$2b$12$dDJL6TNSXPSJELPzZTfdw.Oeq33CeZIuCyQMLVJL5bt21f820gAO.', 'Victor Hugo', true, 1, '2021-01-13 18:13:50.002926', NULL);
INSERT INTO public.usuario (id, email, senha, nome, is_adm, status, data_criacao, data_atualizacao) VALUES (2, 'marcus@teste.com', '$2b$12$sut0gSL9D71aXCGCdUv08uf/xRY03JtbxVoy0XNED3mbsvc6ujKIm', 'Marcus Vinicius', false, 1, '2021-01-13 18:22:52.290519', NULL);


--
-- TOC entry 3035 (class 0 OID 16654)
-- Dependencies: 203
-- Data for Name: vendedor; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.vendedor (id, nome, email, data_criacao, data_atualizacao, data_deletacao) VALUES (4, 'Eliane Rosa', 'eliane.rosa@teste.com', '2021-01-13 19:26:16.853411', NULL, '2021-01-13 19:28:12.399688');
INSERT INTO public.vendedor (id, nome, email, data_criacao, data_atualizacao, data_deletacao) VALUES (6, 'Lucas Silva', 'lucas.silva@teste.com', '2021-01-13 19:46:53.162485', NULL, NULL);
INSERT INTO public.vendedor (id, nome, email, data_criacao, data_atualizacao, data_deletacao) VALUES (5, 'Pedro Henrique', 'pedro.henrique@teste.com', '2021-01-13 19:27:38.426103', NULL, NULL);
INSERT INTO public.vendedor (id, nome, email, data_criacao, data_atualizacao, data_deletacao) VALUES (7, 'Yasmin Gonçalves', 'yasmin.gonc@teste.com', '2021-01-14 15:17:42.390957', NULL, NULL);
INSERT INTO public.vendedor (id, nome, email, data_criacao, data_atualizacao, data_deletacao) VALUES (8, 'Lorenzo Leite', 'lorenzo.leite@teste.com', '2021-01-14 15:18:07.497686', NULL, NULL);
INSERT INTO public.vendedor (id, nome, email, data_criacao, data_atualizacao, data_deletacao) VALUES (9, 'Victor Hugo', 'victor.hugo@teste.com', '2021-01-14 16:01:30.160647', NULL, NULL);
INSERT INTO public.vendedor (id, nome, email, data_criacao, data_atualizacao, data_deletacao) VALUES (10, 'Marcus Vinicius', 'marcus.vinicius@teste.com', '2021-01-14 16:01:52.279199', NULL, NULL);
INSERT INTO public.vendedor (id, nome, email, data_criacao, data_atualizacao, data_deletacao) VALUES (11, 'Eliane Rosa', 'eliane.rosa@teste.com', '2021-01-14 16:02:09.227135', NULL, NULL);
INSERT INTO public.vendedor (id, nome, email, data_criacao, data_atualizacao, data_deletacao) VALUES (12, 'José Luíz', 'jose.luis@teste.com', '2021-01-14 16:02:36.005077', NULL, NULL);


--
-- TOC entry 3052 (class 0 OID 0)
-- Dependencies: 206
-- Name: cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cliente_id_seq', 15, true);


--
-- TOC entry 3053 (class 0 OID 0)
-- Dependencies: 209
-- Name: log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.log_id_seq', 1, false);


--
-- TOC entry 3054 (class 0 OID 0)
-- Dependencies: 204
-- Name: rota_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.rota_id_seq', 10, true);


--
-- TOC entry 3055 (class 0 OID 0)
-- Dependencies: 200
-- Name: usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.usuario_id_seq', 2, true);


--
-- TOC entry 3056 (class 0 OID 0)
-- Dependencies: 202
-- Name: vendedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.vendedor_id_seq', 12, true);


--
-- TOC entry 2895 (class 2606 OID 16973)
-- Name: cliente cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (id);


--
-- TOC entry 2897 (class 2606 OID 17007)
-- Name: log log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.log
    ADD CONSTRAINT log_pkey PRIMARY KEY (id);


--
-- TOC entry 2893 (class 2606 OID 16838)
-- Name: rota rota_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rota
    ADD CONSTRAINT rota_pkey PRIMARY KEY (id);


--
-- TOC entry 2889 (class 2606 OID 16629)
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);


--
-- TOC entry 2891 (class 2606 OID 16662)
-- Name: vendedor vendedor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vendedor
    ADD CONSTRAINT vendedor_pkey PRIMARY KEY (id);


--
-- TOC entry 2899 (class 2606 OID 16974)
-- Name: cliente rota_id_fkey ; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT "rota_id_fkey " FOREIGN KEY (rota_id) REFERENCES public.rota(id) NOT VALID;


--
-- TOC entry 2898 (class 2606 OID 16839)
-- Name: rota vendedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rota
    ADD CONSTRAINT vendedor_id_fkey FOREIGN KEY (vendedor_id) REFERENCES public.vendedor(id) DEFERRABLE;


--
-- TOC entry 2900 (class 2606 OID 16979)
-- Name: cliente vendedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT vendedor_id_fkey FOREIGN KEY (vendedor_id) REFERENCES public.vendedor(id) NOT VALID;


-- Completed on 2021-01-16 23:52:04

--
-- PostgreSQL database dump complete
--

