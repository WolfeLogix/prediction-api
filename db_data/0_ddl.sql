CREATE TABLE  (
    id SERIAL PRIMARY KEY,
    time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    symobl VARCHAR NOT NULL,
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

-- Each ticker will use 
--      open, 
--      prev_open, 
--      prev_close, 
--      prev_high, 
--      prev_low, 
--      prev_volume
-- due to the fact that these are the known values at market open. 