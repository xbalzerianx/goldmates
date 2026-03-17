import { createClient } from 'npm:@base44/sdk@0.8.20';

const base44 = createClient({
  appId: Deno.env.get('BASE44_APP_ID') || '69b7cae883aa8d618e49d211',
  token: Deno.env.get('BASE44_SERVICE_TOKEN'),
});

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Content-Type': 'application/json',
};

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response(null, { headers: CORS });

  try {
    const url = new URL(req.url);
    const entity = url.searchParams.get('entity');
    const id = url.searchParams.get('id');
    const body = req.method !== 'GET' ? await req.json().catch(() => ({})) : {};

    if (!entity) return Response.json({ error: 'entity param required' }, { status: 400, headers: CORS });

    const db = base44.asServiceRole.entities[entity];
    if (!db) return Response.json({ error: 'Unknown entity' }, { status: 400, headers: CORS });

    let result;

    if (req.method === 'GET') {
      result = id ? await db.get(id) : await db.list(null, 500);
    } else if (req.method === 'POST') {
      result = await db.create(body);
    } else if (req.method === 'PUT') {
      if (!id) return Response.json({ error: 'id required for update' }, { status: 400, headers: CORS });
      result = await db.update(id, body);
    } else if (req.method === 'DELETE') {
      if (!id) return Response.json({ error: 'id required for delete' }, { status: 400, headers: CORS });
      result = await db.delete(id);
    }

    return Response.json(result, { headers: CORS });
  } catch (e) {
    return Response.json({ error: e.message }, { status: 500, headers: CORS });
  }
});
