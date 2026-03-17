const APP_ID = Deno.env.get('BASE44_APP_ID') || '69b7cae883aa8d618e49d211';
const SVC_TOKEN = Deno.env.get('BASE44_SERVICE_TOKEN') || '';
const BASE_URL = `https://base44.app/api/apps/${APP_ID}/entities`;

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-App-Id',
  'Content-Type': 'application/json',
};

function hdrs() {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${SVC_TOKEN}`,
    'X-App-Id': APP_ID,
  };
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response(null, { headers: CORS, status: 204 });

  try {
    const url = new URL(req.url);
    // Path: /functions/kgcarApi/{entity}/{id?}
    const pathParts = url.pathname.replace('/functions/kgcarApi', '').split('/').filter(Boolean);
    const entity = pathParts[0];
    const id = pathParts[1];

    if (!entity) return Response.json({ error: 'entity required in path' }, { status: 400, headers: CORS });

    let apiUrl = `${BASE_URL}/${entity}`;
    if (id) apiUrl += `/${id}`;
    if (req.method === 'GET') apiUrl += '?limit=500';

    const body = (req.method === 'POST' || req.method === 'PUT')
      ? await req.text()
      : undefined;

    const resp = await fetch(apiUrl, {
      method: req.method,
      headers: hdrs(),
      body,
    });

    const text = await resp.text();
    return new Response(text, {
      status: resp.status,
      headers: { ...CORS, 'Content-Type': 'application/json' },
    });

  } catch (e) {
    return Response.json({ error: e.message }, { status: 500, headers: CORS });
  }
});
