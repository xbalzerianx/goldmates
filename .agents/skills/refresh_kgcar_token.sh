#!/bin/bash
# Refresh the Base44 service token in the KGcar GitHub repo HTML
# This keeps the deployed app working since tokens expire hourly

set -e
source /app/.agents/.env

REPO="xbalzerianx/KGcar-Database"
FILE="index.html"
NEW_TOKEN="$BASE44_SERVICE_TOKEN"

if [ -z "$NEW_TOKEN" ]; then
    echo "ERROR: BASE44_SERVICE_TOKEN is empty"
    exit 1
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo "ERROR: GITHUB_TOKEN is empty"
    exit 1
fi

echo "Fetching current file from GitHub..."
FILE_DATA=$(curl -s "https://api.github.com/repos/$REPO/contents/$FILE" \
    -H "Authorization: token $GITHUB_TOKEN")

SHA=$(echo "$FILE_DATA" | python3 -c "import sys,json; print(json.load(sys.stdin)['sha'])")
CONTENT_B64=$(echo "$FILE_DATA" | python3 -c "import sys,json; print(json.load(sys.stdin)['content'])")

echo "Decoding content..."
CONTENT=$(echo "$CONTENT_B64" | python3 -c "
import sys, base64
data = sys.stdin.read().replace('\n','')
print(base64.b64decode(data).decode('utf-8'))
")

# Find the old token and replace it
OLD_TOKEN=$(echo "$CONTENT" | python3 -c "
import sys, re
content = sys.stdin.read()
match = re.search(r\"const TOK = '([^']+)'\", content)
if match:
    print(match.group(1))
else:
    print('')
")

if [ -z "$OLD_TOKEN" ]; then
    echo "ERROR: Could not find old token in HTML"
    exit 1
fi

if [ "$OLD_TOKEN" = "$NEW_TOKEN" ]; then
    echo "Token is already up to date, no update needed"
    exit 0
fi

echo "Replacing old token..."
NEW_CONTENT=$(echo "$CONTENT" | python3 -c "
import sys
content = sys.stdin.read()
import os
old = '''$OLD_TOKEN'''
new = os.environ['BASE44_SERVICE_TOKEN']
content = content.replace(old, new)
print(content, end='')
")

# Encode new content
NEW_CONTENT_B64=$(echo "$NEW_CONTENT" | python3 -c "
import sys, base64
content = sys.stdin.read()
print(base64.b64encode(content.encode('utf-8')).decode('utf-8'))
")

echo "Pushing update to GitHub..."
RESULT=$(curl -s -X PUT "https://api.github.com/repos/$REPO/contents/$FILE" \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"Auto-refresh auth token\", \"content\": \"$NEW_CONTENT_B64\", \"sha\": \"$SHA\"}")

COMMIT=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('commit',{}).get('sha','ERROR: '+str(d)[:100]))")
echo "Done! Commit: $COMMIT"
