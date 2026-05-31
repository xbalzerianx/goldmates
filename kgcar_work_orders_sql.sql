-- ============================================================
-- KG CAR DATABASE — Work Orders SQL
-- Run this in your Supabase SQL Editor
-- ============================================================

-- 1. WORK ORDERS table
CREATE TABLE kg_work_orders (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  wo_number text NOT NULL,
  status text DEFAULT 'open' CHECK (status IN ('open','inprogress','completed','cancelled')),
  work_date date,
  work_time time,
  customer_name text NOT NULL,
  customer_phone text,
  plate_number text,
  vehicle text,
  mechanic text,
  notes text,
  services_json text DEFAULT '[]',
  parts_json text DEFAULT '[]',
  labor_total numeric DEFAULT 0,
  parts_total numeric DEFAULT 0,
  subtotal numeric DEFAULT 0,
  vat_amount numeric DEFAULT 0,
  grand_total numeric DEFAULT 0,
  recorded_by text,
  created_date timestamptz DEFAULT now(),
  updated_date timestamptz DEFAULT now()
);

-- Enable RLS and allow all access (same pattern as other KG tables)
ALTER TABLE kg_work_orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON kg_work_orders FOR ALL USING (true) WITH CHECK (true);

-- Auto-update updated_date on edit
CREATE OR REPLACE FUNCTION update_updated_date()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_date = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER kg_work_orders_updated
  BEFORE UPDATE ON kg_work_orders
  FOR EACH ROW EXECUTE FUNCTION update_updated_date();


-- 2. WO TEMPLATES table
CREATE TABLE kg_wo_templates (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  name text NOT NULL,
  description text,
  services_json text DEFAULT '[]',
  parts_json text DEFAULT '[]',
  created_date timestamptz DEFAULT now(),
  updated_date timestamptz DEFAULT now()
);

ALTER TABLE kg_wo_templates ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON kg_wo_templates FOR ALL USING (true) WITH CHECK (true);

CREATE TRIGGER kg_wo_templates_updated
  BEFORE UPDATE ON kg_wo_templates
  FOR EACH ROW EXECUTE FUNCTION update_updated_date();


-- ============================================================
-- OPTIONAL: Insert sample templates to get you started
-- ============================================================
INSERT INTO kg_wo_templates (name, description, services_json, parts_json) VALUES
(
  'Change Oil Package',
  'Standard oil change with filter replacement',
  '[{"name":"Labor - Change Oil","price":250},{"name":"Labor - Oil Filter Replacement","price":100}]',
  '[]'
),
(
  'PMS Package (Preventive Maintenance)',
  'Complete preventive maintenance service',
  '[{"name":"Labor - Change Oil","price":250},{"name":"Labor - Air Filter Check","price":100},{"name":"Labor - Brake Inspection","price":150},{"name":"Labor - Tire Rotation","price":200}]',
  '[]'
),
(
  'Brake Job',
  'Brake pad replacement and inspection',
  '[{"name":"Labor - Brake Pad Replacement","price":350},{"name":"Labor - Brake System Inspection","price":150}]',
  '[]'
),
(
  'Change Filter',
  'Air and fuel filter replacement',
  '[{"name":"Labor - Air Filter Replacement","price":150},{"name":"Labor - Fuel Filter Replacement","price":200}]',
  '[]'
);

-- ============================================================
-- Done! After running this:
-- 1. Hard refresh the KG Car Database site
-- 2. Click "Work Orders" in the sidebar
-- 3. Click "WO Templates" to see the pre-loaded templates
-- ============================================================
