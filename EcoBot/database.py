# -*- coding: utf-8 -*-
from supabase import create_client, Client
from datetime import datetime

# Credenciales de Supabase
SUPABASE_URL = "https://foipeswlpwklreoylgzt.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZvaXBlc3dscHdrbHJlb3lsZ3p0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMyNDQzODksImV4cCI6MjA3ODgyMDM4OX0.1ouFS8estCqwUz-byWbW6SumsFmb1vTzoJP4Cde-aGM"

# Inicializar cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class DatabaseManager:
    """Gestiona todas las operaciones de base de datos con Supabase"""
    
    @staticmethod
    async def add_or_update_user(discord_id: str, username: str):
        """Añade o actualiza un usuario en la tabla users"""
        try:
            # Verificar si el usuario ya existe
            response = supabase.table("users").select("*").eq("discord_id", discord_id).execute()
            
            if response.data:
                # Actualizar usuario existente
                supabase.table("users").update({
                    "username": username,
                    "first_interaction": datetime.now().isoformat()
                }).eq("discord_id", discord_id).execute()
                print(f"✅ Usuario actualizado: {username} ({discord_id})")
            else:
                # Crear nuevo usuario
                supabase.table("users").insert({
                    "discord_id": discord_id,
                    "username": username,
                    "created_at": datetime.now().isoformat(),
                    "first_interaction": datetime.now().isoformat()
                }).execute()
                print(f"✅ Usuario creado: {username} ({discord_id})")
        except Exception as e:
            print(f"❌ Error al añadir/actualizar usuario: {e}")
    
    @staticmethod
    async def add_or_update_server(server_id: str, server_name: str):
        """Añade o actualiza un servidor en la tabla servers"""
        try:
            # Verificar si el servidor ya existe
            response = supabase.table("servers").select("*").eq("server_id", server_id).execute()
            
            if response.data:
                # Actualizar servidor existente
                supabase.table("servers").update({
                    "server_name": server_name
                }).eq("server_id", server_id).execute()
                print(f"✅ Servidor actualizado: {server_name} ({server_id})")
            else:
                # Crear nuevo servidor
                supabase.table("servers").insert({
                    "server_id": server_id,
                    "server_name": server_name,
                    "first_seen": datetime.now().isoformat()
                }).execute()
                print(f"✅ Servidor creado: {server_name} ({server_id})")
        except Exception as e:
            print(f"❌ Error al añadir/actualizar servidor: {e}")
    
    @staticmethod
    async def add_connection(user_discord_id: str, server_id: str):
        """Añade una conexión entre usuario y servidor"""
        try:
            # Obtener IDs de la base de datos
            user_response = supabase.table("users").select("id").eq("discord_id", user_discord_id).execute()
            server_response = supabase.table("servers").select("id").eq("server_id", server_id).execute()
            
            if user_response.data and server_response.data:
                user_id = user_response.data[0]["id"]
                server_db_id = server_response.data[0]["id"]
                
                # Verificar si la conexión ya existe
                connection_response = supabase.table("connection_servers_users").select("*").eq("user_discord_id", user_discord_id).eq("server_id", server_id).execute()
                
                if not connection_response.data:
                    # Crear nueva conexión
                    supabase.table("connection_servers_users").insert({
                        "user_discord_id": user_discord_id,
                        "server_id": server_id,
                        "joined_at": datetime.now().isoformat()
                    }).execute()
                    print(f"✅ Conexión creada: Usuario {user_discord_id} en servidor {server_id}")
            else:
                print("❌ No se encontraron el usuario o el servidor en la BD")
        except Exception as e:
            print(f"❌ Error al añadir conexión: {e}")
    
    @staticmethod
    async def get_user(discord_id: str):
        """Obtiene la información de un usuario"""
        try:
            response = supabase.table("users").select("*").eq("discord_id", discord_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"❌ Error al obtener usuario: {e}")
            return None
    
    @staticmethod
    async def get_server(server_id: str):
        """Obtiene la información de un servidor"""
        try:
            response = supabase.table("servers").select("*").eq("server_id", server_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"❌ Error al obtener servidor: {e}")
            return None
