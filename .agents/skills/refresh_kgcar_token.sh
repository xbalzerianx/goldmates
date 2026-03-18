#!/bin/bash
# Refreshes the KGcar app token in GitHub with the permanent BASE44_SERVICE_TOKEN
# Handles both `const TOK` (old) and `let TOK` (new) patterns

source /app/.agents/.env

# Get current file + SHA from GitHub
RESPONSE=$(curl -s "https://api.github.com/repos/xbalzerianx/KGcar-Database/contents/index.html" \
  -H "Authorization: token $GITHUB_TOKEN")

SHA=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['sha'])")
CONTENT=$(echo "$RESPONSE" | python3 -c "
import sys,json,base64
d=json.load(sys.stdin)
print(base64.b64decode(d['content'].replace('\n','')).decode('utf-8'))
")

# Replace token - supports both const TOK and let TOK patterns
NEW_CONTENT=$(echo "$CONTENT" | python3 -c "
import sys, re, os
content = sys.stdin.read()
token = os.environ['BASE44_SERVICE_TOKEN']
# Try let TOK first (new format), then fall back to const TOK (old format)
new = re.sub(r\"let TOK = '[^']*'\", f\"let TOK = '{token}'\", content)
if new == content:
    new = re.sub(r\"const TOK = '[^']*'\", f\"const TOK = '{token}'\", content)
print(new)
")

# Test the token first
TEST=$(curl -s "https://base44.app/api/apps/69b7cae883aa8d618e49d211/entities/KGProduct?limit=1" \
  -H "Authorization: Bearer $BASE44_SERVICE_TOKEN" \
  -H "X-App-Id: 69b7cae883aa8d618e49d211")

if echo "$TEST" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if isinstance(d,list) else 1)" 2>/dev/null; then
  # Token works - push update
  CONTENT_B64=$(echo "$NEW_CONTENT" | base64 -w 0)
  RESULT=$(curl -s -X PUT "https://api.github.com/repos/xbalzerianx/KGcar-Database/contents/index.html" \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"message\":\"Auto: refresh service token\",\"content\":\"$CONTENT_B64\",\"sha\":\"$SHA\"}")
  
  echo "$RESULT" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print('✅ Token refreshed OK' if 'commit' in d else '❌ Push failed: '+str(d)[:200])
"
else
  echo "❌ Token test failed - skipping push"
fi
