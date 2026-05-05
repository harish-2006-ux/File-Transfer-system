"""
VaultX Database Module
Handles all database operations with Supabase
"""

from .supabase_client import (
    init_supabase,
    get_supabase,
    test_connection
)

__all__ = [
    'init_supabase',
    'get_supabase',
    'test_connection'
]
