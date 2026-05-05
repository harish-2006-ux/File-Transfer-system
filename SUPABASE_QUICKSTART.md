# Supabase Quick Start - 5 Minutes

Fast track guide to get VaultX running with Supabase.

---

## ⚡ Quick Setup (5 Steps)

### 1️⃣ Create Supabase Project (2 min)

1. Go to https://supabase.com → Sign up
2. Click "New Project"
3. Name: `vaultx`, Choose region, Generate password
4. Wait for project to initialize

### 2️⃣ Get Your Keys (30 sec)

Dashboard → Settings → API

Copy these 3 values:
- **Project URL**: `https://xxxxx.supabase.co`
- **Anon Key**: `eyJhbGci...`
- **Service Role Key**: `eyJhbGci...` (keep secret!)

### 3️⃣ Update .env (30 sec)

```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
DATABASE_TYPE=supabase
```

### 4️⃣ Setup Database (1 min)

```bash
# Install dependencies
pip install -r requirements.txt

# Generate schema
python supabase_setup.py
```

Then:
1. Open Supabase Dashboard → SQL Editor
2. Copy contents of `supabase_schema.sql`
3. Paste and click "Run"

### 5️⃣ Test & Run (1 min)

```bash
# Test connection
python db_supabase.py

# Should see: ✅ Connection successful!

# Run app
python app.py
```

---

## ✅ Verification

Visit http://127.0.0.1:8000

1. Create account
2. Login with OTP
3. Upload file
4. Check Supabase Dashboard → Table Editor → `users`

You should see your user! 🎉

---

## 🔄 Switch Back to SQLite

In `.env`:
```bash
DATABASE_TYPE=sqlite
```

Restart app. Done!

---

## 📚 Need More Details?

See `SUPABASE_SETUP_GUIDE.md` for:
- Detailed explanations
- Troubleshooting
- Migration guides
- Production deployment
- Advanced features

---

## 🆘 Common Issues

**"Connection failed"**
- Check SUPABASE_URL and SUPABASE_SERVICE_KEY in .env
- Wait 2-3 min after project creation

**"Table does not exist"**
- Run SQL schema in Supabase Dashboard
- Check Table Editor to verify tables

**"Import error: supabase"**
```bash
pip install supabase==2.3.4
```

---

## 🎯 What You Get

✅ Cloud PostgreSQL database  
✅ Scalable file storage  
✅ Real-time capabilities  
✅ Auto backups (Pro plan)  
✅ Global CDN  
✅ Free tier: 500MB DB + 1GB storage  

---

**That's it! You're now running VaultX with Supabase! 🚀**
