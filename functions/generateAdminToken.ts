// Simple function to return a test response - we'll use a different approach
export default async function handler(req: Request): Promise<Response> {
  return new Response(JSON.stringify({ status: "ok", message: "token generation via SDK not supported directly" }), {
    headers: { "Content-Type": "application/json" }
  });
}
