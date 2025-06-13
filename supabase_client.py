from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

if not SUPABASE_URL or not SUPABASE_API_KEY:
    raise ValueError("❌ SUPABASE_URL o SUPABASE_API_KEY no están definidos en el entorno")

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

