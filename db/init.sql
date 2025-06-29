-- db/init/init.sql

CREATE TABLE IF NOT EXISTS stats (
  id SERIAL PRIMARY KEY,
  label TEXT NOT NULL,
  value NUMERIC NOT NULL,
  recorded_at TIMESTAMPTZ DEFAULT now()
);

INSERT INTO stats (label, value) VALUES
  ('page_views', 123),
  ('sign_ups', 45),
  ('active_users', 67);
