# OAuth Setup Guide

## Google OAuth Configuration

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name (e.g., "Vocab App") and click "Create"

### Step 2: Enable Google+ API

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Google+ API" or "People API"
3. Click on it and press "Enable"

### Step 3: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External (for testing) or Internal (for organization)
   - App name: Vocab App
   - User support email: Your email
   - Developer contact information: Your email
   - Add scopes: `email`, `profile`, `openid`
   - Add test users if using External type
4. Create OAuth Client ID:
   - Application type: **Web application**
   - Name: Vocab App Web Client
   - Authorized JavaScript origins:
     - `http://localhost:5173`
     - `http://localhost:8000`
   - Authorized redirect URIs:
     - `http://localhost:8000/api/v1/auth/google/callback`
5. Click "Create"
6. Copy the **Client ID** and **Client Secret**

### Step 4: Update Backend Environment Variables

Edit `/home/nlandel/freelance/vocab/backend/.env`:

```env
GOOGLE_CLIENT_ID=your-actual-client-id-from-google
GOOGLE_CLIENT_SECRET=your-actual-client-secret-from-google
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback
```

### Step 5: Restart Backend

```bash
cd /home/nlandel/freelance/vocab
docker compose restart backend
```

### Step 6: Test the Application

1. Open http://localhost:5173
2. You should be redirected to login page
3. Try both authentication methods:
   - **Email/Password**: Create account via "Create Account" link
   - **Google OAuth**: Click "Continue with Google" button

## OAuth Flow Diagram

```
User → Frontend (Login) → "Continue with Google"
  ↓
Backend (/api/v1/auth/google/login) → Redirect to Google
  ↓
Google Login → User authenticates
  ↓
Google → Callback to Backend (/api/v1/auth/google/callback)
  ↓
Backend → Create/Update User → Generate JWT Token
  ↓
Backend → Redirect to Frontend (/auth/callback?token=JWT)
  ↓
Frontend → Store token → Fetch user → Redirect to home
```

## Troubleshooting

### "redirect_uri_mismatch" error
- Ensure the redirect URI in Google Console exactly matches: `http://localhost:8000/api/v1/auth/google/callback`
- No trailing slash, exact protocol (http vs https), exact port

### "invalid_client" error
- Check that GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET are correctly set in .env
- Restart backend after changing .env: `docker compose restart backend`

### Connection refused
- Check backend is running: `docker compose ps`
- Check backend logs: `docker compose logs backend`
- Verify port 8000 is accessible: `curl http://localhost:8000/docs`

### Token not stored
- Check browser console for errors
- Verify localStorage has 'token' key after login
- Check Network tab for /api/v1/auth/me request

## API Endpoints

### Authentication Endpoints

- `POST /api/v1/auth/register` - Register with email/password
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword123"
  }
  ```

- `POST /api/v1/auth/login` - Login with email/password (OAuth2PasswordRequestForm)
  - Content-Type: `application/x-www-form-urlencoded`
  - Form fields: `username` (email), `password`

- `GET /api/v1/auth/me` - Get current user (requires Bearer token)
  - Header: `Authorization: Bearer <token>`

- `GET /api/v1/auth/google/login` - Initiate Google OAuth flow

- `GET /api/v1/auth/google/callback` - Google OAuth callback (don't call directly)

## Frontend Routes

- `/` - Home (protected)
- `/login` - Login page (guest only)
- `/register` - Register page (guest only)
- `/auth/callback` - OAuth callback handler (public)
- `/session` - Session view (protected)
- `/config` - Configuration (protected)
- `/profile` - User profile (protected)

## Testing Checklist

- [ ] Google OAuth credentials configured
- [ ] Backend restarted with new credentials
- [ ] Can access login page
- [ ] Can register with email/password
- [ ] Can login with email/password
- [ ] Can login with Google OAuth
- [ ] Token persists across page refreshes
- [ ] Protected routes redirect to login when not authenticated
- [ ] Can logout successfully
- [ ] Login/register pages redirect to home when already authenticated
