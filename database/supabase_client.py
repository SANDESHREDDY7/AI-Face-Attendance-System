import os
from config import SUPABASE_URL, SUPABASE_KEY
from database.local_client import LocalSupabaseClient

supabase = None

if os.getenv("USE_LOCAL_DB", "").lower() in ("true", "1") or not SUPABASE_URL or not SUPABASE_KEY:
    print("ℹ️ Using local SQLite database (database/local_attendance.db)")
    supabase = LocalSupabaseClient()
else:
    try:
        from supabase import create_client
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        client.table("students").select("id").limit(1).execute()
        supabase = client
        print("✅ Connected to Supabase successfully!")
    except Exception as e:
        print(f"⚠️ Supabase unreachable ({e}). Falling back to local SQLite database (database/local_attendance.db).")
        supabase = LocalSupabaseClient()
