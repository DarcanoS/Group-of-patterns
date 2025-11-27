"""
Script to verify which environment file is being used and what values are loaded.
"""

import os
from pathlib import Path

# Get the project root
project_root = Path(__file__).parent

print("=" * 70)
print("VERIFICACIÓN DE ARCHIVOS DE CONFIGURACIÓN")
print("=" * 70)
print()

# Check which .env files exist
env_file = project_root / ".env"
env_example_file = project_root / ".env.example"

print("📁 Archivos de Configuración:")
print(f"   .env existe: {'✓ SÍ' if env_file.exists() else '✗ NO'}")
if env_file.exists():
    print(f"   .env tamaño: {env_file.stat().st_size} bytes")
    print(f"   .env líneas: {len(env_file.read_text().splitlines())}")

print(f"   .env.example existe: {'✓ SÍ' if env_example_file.exists() else '✗ NO'}")
if env_example_file.exists():
    print(f"   .env.example tamaño: {env_example_file.stat().st_size} bytes")
    print(f"   .env.example líneas: {len(env_example_file.read_text().splitlines())}")

print()
print("=" * 70)
print("VALORES CARGADOS EN LA APLICACIÓN")
print("=" * 70)
print()

try:
    from app.core.config import settings

    print("✓ Configuración cargada exitosamente")
    print()
    print("🔧 Configuración Actual:")
    print(f"   DATABASE_URL: {settings.DATABASE_URL[:50]}..." if len(settings.DATABASE_URL) > 50 else f"   DATABASE_URL: {settings.DATABASE_URL}")

    # Extract host and port from DATABASE_URL
    if "@" in settings.DATABASE_URL:
        host_part = settings.DATABASE_URL.split("@")[1].split("/")[0]
        print(f"   → Host: {host_part}")

    print(f"   NOSQL_URI: {settings.NOSQL_URI[:50]}..." if settings.NOSQL_URI and len(settings.NOSQL_URI) > 50 else f"   NOSQL_URI: {settings.NOSQL_URI or 'NO CONFIGURADO'}")

    # Extract host and port from NOSQL_URI
    if settings.NOSQL_URI and "@" in settings.NOSQL_URI:
        host_part = settings.NOSQL_URI.split("@")[1].split("/")[0].split("?")[0]
        print(f"   → Host: {host_part}")

    print(f"   NOSQL_DB_NAME: {settings.NOSQL_DB_NAME}")
    print(f"   PROJECT_NAME: {settings.PROJECT_NAME}")
    print(f"   VERSION: {settings.VERSION}")

    print()
    print("=" * 70)
    print("VERIFICACIÓN ESPECÍFICA")
    print("=" * 70)
    print()

    # Check if using the remote databases
    is_using_remote_postgres = "darcano.duckdns.org" in settings.DATABASE_URL
    is_using_remote_mongo = settings.NOSQL_URI and "darcano.duckdns.org" in settings.NOSQL_URI

    print(f"PostgreSQL remoto (darcano.duckdns.org): {'✓ SÍ' if is_using_remote_postgres else '✗ NO (usando localhost u otro)'}")
    print(f"MongoDB remoto (darcano.duckdns.org): {'✓ SÍ' if is_using_remote_mongo else '✗ NO (usando localhost u otro)'}")

    if is_using_remote_postgres and is_using_remote_mongo:
        print()
        print("✅ CONFIGURACIÓN CORRECTA: Usando las credenciales remotas proporcionadas")
    elif not is_using_remote_postgres or not is_using_remote_mongo:
        print()
        print("⚠️  ADVERTENCIA: No se están usando las credenciales remotas completas")
        print("   Verifica que el archivo .env tenga las credenciales correctas")

except Exception as e:
    print(f"✗ Error al cargar la configuración: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
print("CONTENIDO DE .env (si existe)")
print("=" * 70)
print()

if env_file.exists():
    content = env_file.read_text()
    lines = content.splitlines()

    print(f"Total de líneas: {len(lines)}")
    print()

    # Show content with sensitive data masked
    for i, line in enumerate(lines, 1):
        if line.strip() and not line.strip().startswith("#"):
            if "=" in line:
                key, value = line.split("=", 1)
                # Mask password in URLs
                if "://" in value and "@" in value:
                    # Extract and mask password
                    protocol = value.split("://")[0]
                    rest = value.split("://")[1]
                    if "@" in rest:
                        credentials, host_part = rest.split("@", 1)
                        if ":" in credentials:
                            user, _ = credentials.split(":", 1)
                            masked_value = f"{protocol}://{user}:***@{host_part}"
                        else:
                            masked_value = f"{protocol}://{credentials}@{host_part}"
                        print(f"{i:3}. {key}={masked_value}")
                    else:
                        print(f"{i:3}. {key}={value}")
                else:
                    print(f"{i:3}. {line}")
            else:
                print(f"{i:3}. {line}")
        else:
            print(f"{i:3}. {line}")
else:
    print("⚠️  Archivo .env NO EXISTE")
    print()
    print("Para crear el archivo .env con las credenciales remotas:")
    print("   cp .env.example .env")
    print("   # Luego edita .env con las credenciales correctas")

print()
print("=" * 70)

