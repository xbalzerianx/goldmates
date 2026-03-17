const APP_ID = Deno.env.get('BASE44_APP_ID') || '69b7cae883aa8d618e49d211';
const SVC_TOKEN = Deno.env.get('BASE44_SERVICE_TOKEN') || '';
const BASE_URL = `https://base44.app/api/apps/${APP_ID}/entities`;

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-App-Id',
};

function apiHeaders() {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${SVC_TOKEN}`,
    'X-App-Id': APP_ID,
  };
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: CORS, status: 204 });
  }

  try {
    const url = new URL(req.url);
    const entity = url.searchParams.get('entity');
    const id = url.searchParams.get('id');

    if (!entity) {
      return Response.json({ error: 'entity param required' }, { status: 400, headers: CORS });
    }

    let apiUrl = `${BASE_URL}/${entity}`;
    if (id) apiUrl += `/${id}`;
    if (req.method === 'GET') apiUrl += (id ? '' : '?limit=500');

    let bodyText: string | undefined;
    if (req.method === 'POST' || req.method === 'PUT') {
      bodyText = await req.text();
    }

    const upstream = await fetch(apiUrl, {
      method: req.method,
      headers: apiHeaders(),
      body: bodyText,
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
