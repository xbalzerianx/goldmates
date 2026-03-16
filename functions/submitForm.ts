import { createClient } from "@base44/sdk";

const base44 = createClient({
  appId: process.env.BASE44_APP_ID!,
  token: process.env.BASE44_SERVICE_TOKEN!,
  serverUrl: process.env.BASE44_API_URL!,
});

export default async function handler(req: Request): Promise<Response> {
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "https://www.cairspa.com",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };

  if (req.method === "OPTIONS") {
    return new Response(null, { status: 200, headers });
  }

  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), { status: 405, headers });
  }

  try {
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
      return new Response(JSON.stringify({ success: true, id: record.id }), { status: 200, headers });
    }

    if (type === "lead" || type === "contact") {
      const record = await base44.asServiceRole.entities.LeadForm.create({
        name: data.name || "",
        email: data.email || "",
        phone: data.phone || "",
        service_interest: data.service || data.service_interest || "",
        message: data.message || "",
        form_type: data.form_type || "Contact",
        status: "New",
      });
      return new Response(JSON.stringify({ success: true, id: record.id }), { status: 200, headers });
    }

    return new Response(JSON.stringify({ error: "Unknown form type" }), { status: 400, headers });
  } catch (err: any) {
    console.error("Form submission error:", err);
    return new Response(JSON.stringify({ error: err.message }), { status: 500, headers });
  }
}
