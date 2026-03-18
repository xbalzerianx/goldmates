// KGcar API - PIN-authenticated proxy using SDK auto-refresh
import { createClient } from 'npm:@base44/sdk@0.8.20';

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-Pin, X-Session',
};

const VALID_ENTITIES = ['KGProduct', 'KGSale', 'KGExpense', 'KGActivity'];

const PINS: Record<string, string> = {
  '070726': 'admin',
  '5678': 'assistant',
};

const APP_ID = Deno.env.get('BASE44_APP_ID') || '69b7cae883aa8d618e49d211';
const SERVER_URL = Deno.env.get('BASE44_SERVER_URL') || 'https://base44.app';
const SERVICE_TOKEN = Deno.env.get('BASE44_SERVICE_TOKEN') || '';

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: CORS, status: 204 });
  }

  try {
    const url = new URL(req.url);

    // Parse body once
    let body: any = {};
    if (req.method === 'POST' || req.method === 'PUT') {
      const text = await req.text();
      try { body = JSON.parse(text); } catch { body = {}; }
    }

    // PIN auth from header or body or query param
    const pin = req.headers.get('X-Pin') || body._pin || url.searchParams.get('pin') || '';
    const role = PINS[pin];
    if (!role) {
      return Response.json({ error: 'Unauthorized - invalid PIN' }, { status: 401, headers: CORS });
    }

    // Entity and ID
    const entity = url.searchParams.get('entity') || body._entity;
    const id = url.searchParams.get('id') || body._id;
    const limit = parseInt(url.searchParams.get('limit') || '500');

    if (!entity || !VALID_ENTITIES.includes(entity)) {
      return Response.json({ error: `Invalid entity. Allowed: ${VALID_ENTITIES.join(', ')}` }, { status: 400, headers: CORS });
    }

    // Create SDK client with service role (auto-refreshes token)
    const base44 = createClient({
      appId: APP_ID,
      token: SERVICE_TOKEN,
      serverUrl: SERVER_URL,
    });

    const entityClient = base44.asServiceRole.entities[entity];

    // Remove internal params from body
    const { _pin, _entity, _id, ...cleanBody } = body;

    let result: any;

    if (req.method === 'GET') {
      if (id) {
        result = await entityClient.get(id);
      } else {
        result = await entityClient.list({ limit });
      }
    } else if (req.method === 'POST') {
      result = await entityClient.create(cleanBody);
    } else if (req.method === 'PUT') {
      if (!id) return Response.json({ error: 'ID required for PUT' }, { status: 400, headers: CORS });
      result = await entityClient.update(id, cleanBody);
    } else if (req.method === 'DELETE') {
      const delId = id || url.searchParams.get('id');
      if (!delId) return Response.json({ error: 'ID required for DELETE' }, { status: 400, headers: CORS });
      result = await entityClient.delete(delId);
    }

    return Response.json(result, { headers: CORS });

  } catch (e: any) {
    return Response.json({ error: e.message, detail: e.stack }, { status: 500, headers: CORS });
  }
});
