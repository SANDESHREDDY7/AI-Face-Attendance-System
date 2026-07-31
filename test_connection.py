from database.supabase_client import supabase

try:
    response = supabase.table("students").select("*").execute()

    print("✅ Connected to Supabase Successfully!")
    print(response.data)

except Exception as e:
    print("❌ Connection Failed")
    print(e)