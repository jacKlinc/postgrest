# 📊 Public API Dashboard with PostgREST

This is a simple public API built with [PostgREST](https://postgrest.org/) that serves time-series data like analytics, counters, or sensor readings directly from a PostgreSQL database.

The goal is to show how you can turn your PostgreSQL tables and views into a read-only, RESTful API with zero backend code.

---

## 🚀 Features

- 📡 Expose real-time or historical public metrics (e.g. app stats, IoT sensors, or scraped data)
- 🔍 Filter data by time, label, or value using REST query parameters
- 📄 Fully documented API using PostgREST's auto-discovery
- 🔐 Read-only — no write operations allowed
- 🔁 Easily integrate into frontends or dashboards (supports CORS)

---

## 🧱 Database Schema

```sql
CREATE TABLE stats (
  id SERIAL PRIMARY KEY,
  label TEXT NOT NULL,
  value NUMERIC NOT NULL,
  recorded_at TIMESTAMPTZ DEFAULT now()
);
