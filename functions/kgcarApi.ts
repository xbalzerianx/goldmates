// KGcar API - Permanent PIN-authenticated proxy
// No expiring tokens - uses internal service auth

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-Pin, X-Session',
};

const VALID_ENTITIES = ['KGProduct', 'KGSale', 'KGExpense'];

const PINS: Record<string, string> = {
  '070726': 'admin',
  '5678': 'assistant',
};

const APP_ID = Deno.env.get('BASE44_APP_ID') || '69b7cae883aa8d618e49d211';
const BASE_URL = `https://base44.app/api/apps/${APP_ID}/entities`;

function getServiceHeaders() {
  const svcToken = Deno.env.get('BASE44_SERVICE_TOKEN') || '';
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${svcToken}`,
    'X-App-Id': APP_ID,
  };
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: CORS, status: 204 });
  }

  try {
    const url = new URL(req.url);
    const path = url.pathname; // e.g. /functions/kgcarApi or just /
    
    // Parse body once
    let body: any = {};
    if (req.method === 'POST' || req.method === 'PUT') {
      const text = await req.text();
      try { body = JSON.parse(text); } catch { body = {}; }
    }

    // PIN auth from header or body
    const pin = req.headers.get('X-Pin') || body._pin || url.searchParams.get('pin') || '';
    const role = PINS[pin];
    if (!role) {
      return Response.json({ error: 'Unauthorized - invalid PIN' }, { status: 401, headers: CORS });
    }

    // Entity and ID from query params
    const entity = url.searchParams.get('entity') || body._entity;
    const id = url.searchParams.get('id') || body._id;

    if (!entity || !VALID_ENTITIES.includes(entity)) {
      return Response.json({ error: 'Invalid entity' }, { status: 400, headers: CORS });
    }

    // Build upstream URL
    let apiUrl = `${BASE_URL}/${entity}`;
    if (id) apiUrl += `/${id}`;
    if (req.method === 'GET') apiUrl += `?limit=500`;

    // Remove internal params from body
    const { _pin, _entity, _id, ...cleanBody } = body;

    const upstream = await fetch(apiUrl, {
      method: req.method,
      headers: getServiceHeaders(),
      body: (req.method === 'POST' || req.method === 'PUT') ? JSON.stringify(cleanBody) : undefined,
    });

    const text = await upstream.text();
    return new Response(text, {
      status: upstream.status,
      headers: { ...CORS, 'Content-Type': 'application/json' },
    });

  } catch (e: any) {
    return Response.json({ error: e.message }, { status: 500, headers: CORS });
  }
});
