CREATE TABLE stats (
  id SERIAL PRIMARY KEY,
  label TEXT,
  value NUMERIC,
  recorded_at TIMESTAMPTZ DEFAULT now()
);
