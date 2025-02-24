-- Latest Datapoint Table --
CREATE TABLE if NOT EXISTS public.ts_kv_latest (
    device_id VARCHAR NOT NULL,
    device_name VARCHAR NOT NULL,   
    device_group VARCHAR,
    key VARCHAR NOT NULL,
    ts BIGINT NOT NULL,
    bool_v BOOLEAN,
    str_v VARCHAR(10000000),
    long_v BIGINT,
    dbl_v DOUBLE PRECISION,
    json_v JSON,
    PRIMARY KEY (device_id, key)
);

ALTER TABLE public.ts_kv_latest OWNER TO enohub;

-- Historical Datapoint Table --
CREATE TABLE IF NOT EXISTS public.ts_kv (
    device_id VARCHAR NOT NULL,
    device_name VARCHAR NOT NULL,   
    device_group VARCHAR,
    key VARCHAR NOT NULL,
    ts bigint NOT NULL,
    bool_v boolean,
    str_v varchar(10000000),
    long_v bigint,
    dbl_v double precision,
    json_v json,
    PRIMARY KEY (device_id, key, ts)
);

ALTER TABLE public.ts_kv OWNER TO enohub;

-- 2. Create index on timestamp for more efficient queries
CREATE INDEX IF NOT EXISTS ts_kv_ts_idx ON public.ts_kv (ts DESC);

-- 3. Convert to TimescaleDB hypertable
SELECT create_hypertable (
        'public.ts_kv', 'ts', chunk_time_interval => 86400000, -- 1 day in milliseconds
        if_not_exists => TRUE
    );