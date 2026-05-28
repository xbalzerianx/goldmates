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
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, X-Admin-Pin",
    "Vary": "Origin",
  };

  if (req.method === "OPTIONS") {
    return new Response(null, { status: 200, headers: corsHeaders });
  }

  // Verify admin PIN
  const pin = req.headers.get("X-Admin-Pin") || "";
  const ADMIN_PINS = ["070726", "111111", "cairspa_admin", "admin"];
  
  const url = new URL(req.url);
  const entity = url.searchParams.get("entity");
  const recordId = url.searchParams.get("id");
  const limitParam = url.searchParams.get("limit") || "200";
  const sortParam = url.searchParams.get("sort") || "-created_date";

  // Simple PIN check (user/password from admin login)
  const authHeader = req.headers.get("Authorization") || "";
  // Allow if it's a valid local token format (starts with local_) - we trust the frontend check
  // OR if it's a recognized admin pin
  const isAuthorized = authHeader.startsWith("Bearer local_") || 
                       authHeader.startsWith("Bearer cairspa_") ||
                       ADMIN_PINS.includes(pin);

  if (!isAuthorized && !authHeader.startsWith("Bearer local_")) {
    return Response.json({ error: "Unauthorized" }, { status: 401, headers: corsHeaders });
  }

  try {
    const base44 = createClientFromRequest(req);
    const entities: Record<string, any> = {
      Appointment: base44.asServiceRole.entities.Appointment,
      LeadForm: base44.asServiceRole.entities.LeadForm,
      BlogPost: base44.asServiceRole.entities.BlogPost,
    };

    if (!entity || !entities[entity]) {
      return Response.json({ error: "Unknown entity: " + entity }, { status: 400, headers: corsHeaders });
    }

    const entityApi = entities[entity];

    if (req.method === "GET") {
      const data = await entityApi.list({ limit: parseInt(limitParam), sort: sortParam });
      return Response.json(Array.isArray(data) ? data : (data?.data || []), { headers: corsHeaders });
    }

    if (req.method === "POST") {
      const body = await req.json();
      const record = await entityApi.create(body);
      return Response.json(record, { headers: corsHeaders });
    }

    if (req.method === "PUT" && recordId) {
      const body = await req.json();
      const record = await entityApi.update(recordId, body);
      return Response.json(record, { headers: corsHeaders });
    }

    if (req.method === "DELETE" && recordId) {
      await entityApi.delete(recordId);
      return Response.json({ ok: true }, { headers: corsHeaders });
    }

    return Response.json({ error: "Invalid request" }, { status: 400, headers: corsHeaders });
  } catch (err: any) {
    console.error("Admin proxy error:", err);
    return Response.json({ error: err.message }, { status: 500, headers: corsHeaders });
  }
});
