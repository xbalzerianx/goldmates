-- Run this in Supabase SQL Editor to create the kg_employees table

CREATE TABLE IF NOT EXISTS kg_employees (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  name text NOT NULL,
  phone text,
  role text,
  commission_rate numeric DEFAULT 0,
  status text DEFAULT 'active',
  photo_url text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE kg_employees ENABLE ROW LEVEL SECURITY;

-- Allow all operations (same pattern as other KG tables)
CREATE POLICY IF NOT EXISTS "allow_all_kg_employees" ON kg_employees
  FOR ALL USING (true) WITH CHECK (true);
