import { createClientFromRequest } from 'npm:@base44/sdk@0.8.25';

const ALLOWED_ORIGINS = [
  "https://cairspa.com",
  "https://www.cairspa.com",
];

Deno.serve(async (req) => {
  const origin = req.headers.get("origin") || "";
  const corsOrigin = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];

  const corsHeaders = {
    "Access-Control-Allow-Origin": corsOrigin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Vary": "Origin",
  };

  if (req.method === "OPTIONS") {
    return new Response(null, { status: 200, headers: corsHeaders });
  }

  if (req.method !== "POST") {
    return Response.json({ error: "Method not allowed" }, { status: 405, headers: corsHeaders });
  }

  try {
    const base44 = createClientFromRequest(req);
    const body = await req.json();
    const { type, ...data } = body;

    if (type === "appointment") {
      const record = await base44.asServiceRole.entities.Appointment.create({
        client_name: data.name || data.client_name || "",
        client_email: data.email || data.client_email || "",
        client_phone: data.phone || data.client_phone || "",
        service: data.service || "Other",
        preferred_date: data.preferred_date || data.date || "",
        preferred_time: data.preferred_time || data.time || "",
        notes: data.notes || data.message || "",
        status: "Pending",
        source: "Website Form",
      });
      return Response.json({ success: true, id: record.id }, { headers: corsHeaders });
    }

    if (type === "lead" || type === "contact") {
      const record = await base44.asServiceRole.entities.LeadForm.create({
        name: data.name || "",
        email: data.email || "",
        phone: data.phone || "",
        service_interest: data.service || data.service_interest || "",
        message: data.message || "",
        form_type: data.form_type || "Hero Callback",
        status: "New",
      });
      return Response.json({ success: true, id: record.id }, { headers: corsHeaders });
    }

    return Response.json({ error: "Unknown form type" }, { status: 400, headers: corsHeaders });
  } catch (err) {
    console.error("Form submission error:", err);
    return Response.json({ error: err.message }, { status: 500, headers: corsHeaders });
  }
});
