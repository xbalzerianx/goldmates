-- ============================================================
-- GOLDMATES ENTERPRISES — Full Supabase Schema
-- Run this entire script in: Supabase Dashboard > SQL Editor
-- ============================================================

-- ─────────────────────────────────────────
-- 1. PRODUCTS
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS gm_products (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id      TEXT,
  product_name    TEXT NOT NULL,
  category        TEXT,
  brand           TEXT,
  unit            TEXT DEFAULT 'pcs',
  unit_price      NUMERIC(12,2) DEFAULT 0,
  markup_price    NUMERIC(12,2) DEFAULT 0,
  stock_qty       INTEGER DEFAULT 0,
  min_stock       INTEGER DEFAULT 5,
  tire_size       TEXT,
  notes           TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE gm_products ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all for anon" ON gm_products FOR ALL TO anon USING (true) WITH CHECK (true);

-- ─────────────────────────────────────────
-- 2. SALES
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS gm_sales (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sale_id         TEXT,
  product_id      TEXT,
  product_name    TEXT,
  category        TEXT,
  qty_sold        INTEGER DEFAULT 1,
  unit_price      NUMERIC(12,2) DEFAULT 0,
  sale_total      NUMERIC(12,2) DEFAULT 0,
  sale_date       DATE DEFAULT CURRENT_DATE,
  recorded_by     TEXT,
  notes           TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE gm_sales ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all for anon" ON gm_sales FOR ALL TO anon USING (true) WITH CHECK (true);

-- ─────────────────────────────────────────
-- 3. EXPENSES
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS gm_expenses (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  description     TEXT NOT NULL,
  category        TEXT,
  amount          NUMERIC(12,2) DEFAULT 0,
  expense_date    DATE DEFAULT CURRENT_DATE,
  recorded_by     TEXT,
  user_role       TEXT,
  notes           TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE gm_expenses ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all for anon" ON gm_expenses FOR ALL TO anon USING (true) WITH CHECK (true);

-- ─────────────────────────────────────────
-- 4. CATEGORIES
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS gm_categories (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name            TEXT NOT NULL UNIQUE,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE gm_categories ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all for anon" ON gm_categories FOR ALL TO anon USING (true) WITH CHECK (true);

-- Default categories (customize as needed)
INSERT INTO gm_categories (name) VALUES
  ('Tires'),
  ('Engine Oil'),
  ('Brake Pads'),
  ('Brake Oil'),
  ('Filters'),
  ('Batteries'),
  ('Wipers'),
  ('Accessories'),
  ('Labor'),
  ('Other')
ON CONFLICT (name) DO NOTHING;

-- ─────────────────────────────────────────
-- 5. SETTINGS (PINs & Config)
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS gm_settings (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key             TEXT NOT NULL UNIQUE,
  value           TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE gm_settings ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all for anon" ON gm_settings FOR ALL TO anon USING (true) WITH CHECK (true);

-- Default PINs — CHANGE THESE AFTER SETUP
INSERT INTO gm_settings (key, value) VALUES
  ('admin_pin', '070726'),
  ('asst_pin',  '111111')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;

-- ─────────────────────────────────────────
-- 6. WORK ORDERS
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS gm_work_orders (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  wo_number       TEXT,
  client_name     TEXT,
  client_phone    TEXT,
  vehicle_make    TEXT,
  vehicle_model   TEXT,
  vehicle_year    TEXT,
  plate_number    TEXT,
  mileage         TEXT,
  charges         JSONB DEFAULT '[]',
  labor_total     NUMERIC(12,2) DEFAULT 0,
  parts_total     NUMERIC(12,2) DEFAULT 0,
  grand_total     NUMERIC(12,2) DEFAULT 0,
  mechanic_name   TEXT,
  mechanic_id     TEXT,
  commission_rate NUMERIC(5,2) DEFAULT 0,
  commission_amt  NUMERIC(12,2) DEFAULT 0,
  status          TEXT DEFAULT 'open',
  notes           TEXT,
  recorded_by     TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE gm_work_orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all for anon" ON gm_work_orders FOR ALL TO anon USING (true) WITH CHECK (true);

-- ─────────────────────────────────────────
-- 7. WORK ORDER TEMPLATES
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS gm_wo_templates (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name            TEXT NOT NULL,
  description     TEXT,
  charges         JSONB DEFAULT '[]',
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE gm_wo_templates ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all for anon" ON gm_wo_templates FOR ALL TO anon USING (true) WITH CHECK (true);

-- ─────────────────────────────────────────
-- 8. EMPLOYEES
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS gm_employees (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name            TEXT NOT NULL,
  phone           TEXT,
  role            TEXT DEFAULT 'Mechanic',
  commission_rate NUMERIC(5,2) DEFAULT 0,
  photo_url       TEXT,
  is_active       BOOLEAN DEFAULT TRUE,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE gm_employees ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all for anon" ON gm_employees FOR ALL TO anon USING (true) WITH CHECK (true);

-- ─────────────────────────────────────────
-- 9. ACTIVITY LOG
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS gm_activity (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  action_type     TEXT,
  product_name    TEXT,
  detail          TEXT,
  performed_by    TEXT,
  user_role       TEXT,
  timestamp_ph    TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE gm_activity ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all for anon" ON gm_activity FOR ALL TO anon USING (true) WITH CHECK (true);

-- ─────────────────────────────────────────
-- 10. AUTO-UPDATE TIMESTAMPS (triggers)
-- ─────────────────────────────────────────
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_products_updated
  BEFORE UPDATE ON gm_products
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_work_orders_updated
  BEFORE UPDATE ON gm_work_orders
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_employees_updated
  BEFORE UPDATE ON gm_employees
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_settings_updated
  BEFORE UPDATE ON gm_settings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ─────────────────────────────────────────
-- DONE ✅
-- Next steps for the client:
--   1. Note your Supabase Project URL and anon key
--   2. In index.html, replace:
--        YOUR_SUPABASE_PROJECT_ID  →  your project ref (e.g. abcxyz123)
--        YOUR_SUPABASE_ANON_KEY   →  your anon public key
--   3. Connect the Goldmates GitHub repo to Vercel and deploy
--   4. Change default PINs in gm_settings table after first login
-- ─────────────────────────────────────────
