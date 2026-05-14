#!/usr/bin/env bash
# Replace Unicode curly quotes with ASCII in staged JS/JSX/PY/MD files.
# Idempotent — safe to run repeatedly.
set -euo pipefail

files=$(git diff --cached --name-only --diff-filter=ACM \
  | grep -E '\.(js|jsx|ts|tsx|py|md)$' || true)

[ -z "$files" ] && exit 0

for f in $files; do
  [ -f "$f" ] || continue
  node -e "
    const fs=require('fs');
    const p='$f';
    let c=fs.readFileSync(p,'utf8');
    const orig=c;
    c=c.replace(/“/g,'\"').replace(/”/g,'\"')
       .replace(/‘/g,\"'\").replace(/’/g,\"'\")
       .replace(/–/g,'-').replace(/—/g,'--')
       .replace(/…/g,'...');
    if(c!==orig){ fs.writeFileSync(p,c); console.log('sanitised: '+p); }
  "
  git add "$f"
done
