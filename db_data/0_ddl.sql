CREATE TABLE IF NOT EXISTS raw_daily_price (
    id SERIAL PRIMARY KEY,
    "time" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    symbol VARCHAR NOT NULL,
    "open" DECIMAL NOT NULL,
    "close" DECIMAL NOT NULL,
    high DECIMAL NOT NULL,
    low DECIMAL NOT NULL,
    volume NUMERIC NOT NULL,
    prev_open DECIMAL NOT NULL,
    prev_close DECIMAL NOT NULL,
    prev_high DECIMAL NOT NULL,
    prev_low DECIMAL NOT NULL,
    prev_volume NUMERIC NOT NULL
);

-- SELECT create_hypertable('raw_daily_price', by_range('time'));

-- Each ticker will use 
--      open, 
--      prev_open, 
--      prev_close, 
--      prev_high, 
--      prev_low, 
--      prev_volume
-- due to the fact that these are the known values at market open. 