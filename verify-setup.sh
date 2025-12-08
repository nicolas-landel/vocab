#!/bin/bash

echo "🔍 Verifying Vocab App Setup..."
echo ""

# Check folders
echo "📁 Checking folder structure..."
[ -d "backend" ] && echo "✅ backend/" || echo "❌ backend/ missing"
[ -d "frontend" ] && echo "✅ frontend/" || echo "❌ frontend/ missing"
[ -f "docker-compose.yml" ] && echo "✅ docker-compose.yml" || echo "❌ docker-compose.yml missing"
echo ""

# Check backend files
echo "🐍 Checking backend files..."
[ -f "backend/main.py" ] && echo "✅ backend/main.py" || echo "❌ backend/main.py missing"
[ -f "backend/requirements.txt" ] && echo "✅ backend/requirements.txt" || echo "❌ backend/requirements.txt missing"
[ -f "backend/Dockerfile" ] && echo "✅ backend/Dockerfile" || echo "❌ backend/Dockerfile missing"
[ -d "backend/app" ] && echo "✅ backend/app/" || echo "❌ backend/app/ missing"
echo ""

# Check frontend files
echo "🎨 Checking frontend files..."
[ -f "frontend/package.json" ] && echo "✅ frontend/package.json" || echo "❌ frontend/package.json missing"
[ -f "frontend/vite.config.js" ] && echo "✅ frontend/vite.config.js" || echo "❌ frontend/vite.config.js missing"
[ -f "frontend/index.html" ] && echo "✅ frontend/index.html" || echo "❌ frontend/index.html missing"
[ -d "frontend/src" ] && echo "✅ frontend/src/" || echo "❌ frontend/src/ missing"
echo ""

# Check for Firebase remnants
echo "🔥 Checking for Firebase remnants..."
[ ! -f "firebase.json" ] && echo "✅ No firebase.json" || echo "⚠️  firebase.json still exists"
[ ! -f ".firebaserc" ] && echo "✅ No .firebaserc" || echo "⚠️  .firebaserc still exists"
[ ! -d "functions" ] && echo "✅ No functions/" || echo "⚠️  functions/ still exists"
[ ! -f "frontend/src/firebase.js" ] && echo "✅ No frontend/src/firebase.js" || echo "⚠️  frontend/src/firebase.js still exists"
echo ""

# Check environment files
echo "🔐 Checking environment setup..."
[ -f ".env.example" ] && echo "✅ .env.example" || echo "⚠️  .env.example missing"
[ -f "frontend/.env" ] && echo "✅ frontend/.env exists" || echo "⚠️  frontend/.env missing (copy from .env.example)"

# Check frontend .env content
if [ -f "frontend/.env" ]; then
  if grep -q "VITE_API_URL" "frontend/.env"; then
    echo "✅ frontend/.env has VITE_API_URL"
  else
    echo "⚠️  frontend/.env missing VITE_API_URL"
  fi
  if grep -q "FIREBASE" "frontend/.env"; then
    echo "⚠️  frontend/.env still has Firebase config"
  else
    echo "✅ frontend/.env cleaned of Firebase"
  fi
fi
echo ""

echo "✨ Verification complete!"
echo ""
echo "To start the app, run: docker-compose up"
