"""
Script de diagnóstico completo de conexión a bases de datos.
Determina si el problema es del servidor o de la configuración local.
"""

import socket
import sys
from urllib.parse import urlparse
import subprocess
import platform


def test_dns_resolution(hostname):
    """Prueba resolución DNS"""
    print(f"\n🔍 1. RESOLUCIÓN DNS para '{hostname}'")
    try:
        ip = socket.gethostbyname(hostname)
        print(f"   ✅ DNS resuelve correctamente")
        print(f"   📍 IP: {ip}")
        return ip
    except socket.gaierror as e:
        print(f"   ❌ Error DNS: {e}")
        return None


def test_ping(hostname):
    """Prueba conectividad básica con ping"""
    print(f"\n🏓 2. PING a '{hostname}'")
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '4', hostname]

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("   ✅ Servidor responde a ping")
            return True
        else:
            print("   ⚠️  Servidor NO responde a ping (puede estar bloqueado por firewall)")
            return False
    except Exception as e:
        print(f"   ⚠️  No se pudo hacer ping: {e}")
        return False


def test_port_connection(host, port, service_name, timeout=5):
    """Prueba conexión a puerto específico"""
    print(f"\n🔌 3.{port} CONEXIÓN A PUERTO {port} ({service_name})")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        print(f"   Intentando conectar a {host}:{port}...")
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"   ✅ Puerto {port} ABIERTO y aceptando conexiones")
            sock.close()
            return True
        else:
            print(f"   ❌ Puerto {port} CERRADO o rechazando conexiones")
            print(f"   📋 Código de error: {result}")
            sock.close()
            return False
    except socket.timeout:
        print(f"   ⏱️  TIMEOUT: El puerto {port} no responde (firewall o servidor apagado)")
        sock.close()
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        sock.close()
        return False


def test_postgresql_connection():
    """Prueba conexión real a PostgreSQL"""
    print(f"\n🐘 4. PRUEBA DE CONEXIÓN POSTGRESQL")
    try:
        import psycopg2
        from app.core.config import settings

        # Parsear la URL
        parsed = urlparse(settings.DATABASE_URL)

        print(f"   Intentando conectar a:")
        print(f"   Host: {parsed.hostname}")
        print(f"   Puerto: {parsed.port}")
        print(f"   Base de datos: {parsed.path[1:]}")
        print(f"   Usuario: {parsed.username}")

        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password,
            connect_timeout=5
        )

        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()

        print(f"   ✅ CONEXIÓN EXITOSA")
        print(f"   📊 Versión PostgreSQL: {version[0][:50]}...")

        # Verificar PostGIS
        try:
            cursor.execute("SELECT PostGIS_version();")
            postgis = cursor.fetchone()
            print(f"   📍 PostGIS: {postgis[0]}")
        except:
            print(f"   ⚠️  PostGIS no disponible")

        cursor.close()
        conn.close()
        return True

    except ImportError:
        print("   ⚠️  psycopg2 no instalado (ejecuta: pip install psycopg2-binary)")
        return False
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        print(f"   📋 Tipo de error: {type(e).__name__}")

        # Diagnóstico específico
        error_str = str(e).lower()
        if "authentication failed" in error_str or "password" in error_str:
            print(f"   💡 Problema de AUTENTICACIÓN: Usuario o contraseña incorrectos")
        elif "does not exist" in error_str:
            print(f"   💡 Problema: Base de datos o usuario no existe")
        elif "connection refused" in error_str:
            print(f"   💡 Problema: Servidor rechaza conexión (apagado o firewall)")
        elif "timeout" in error_str:
            print(f"   💡 Problema: Timeout - firewall o red lenta")

        return False


def test_mongodb_connection():
    """Prueba conexión real a MongoDB"""
    print(f"\n🍃 5. PRUEBA DE CONEXIÓN MONGODB")
    try:
        from pymongo import MongoClient
        from app.core.config import settings

        if not settings.NOSQL_URI:
            print("   ⚠️  NOSQL_URI no configurado")
            return False

        # Enmascarar contraseña en el log
        uri_display = settings.NOSQL_URI
        if "@" in uri_display:
            parts = uri_display.split("://")
            if len(parts) > 1:
                credentials, rest = parts[1].split("@", 1)
                if ":" in credentials:
                    user = credentials.split(":")[0]
                    uri_display = f"{parts[0]}://{user}:***@{rest}"

        print(f"   Intentando conectar a: {uri_display[:70]}...")

        client = MongoClient(
            settings.NOSQL_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000
        )

        # Forzar conexión
        client.admin.command('ping')

        print(f"   ✅ CONEXIÓN EXITOSA")

        # Info del servidor
        server_info = client.server_info()
        print(f"   📊 Versión MongoDB: {server_info.get('version', 'desconocida')}")
        print(f"   📁 Base de datos: {settings.NOSQL_DB_NAME}")

        # Listar bases de datos
        dbs = client.list_database_names()
        print(f"   📋 Bases de datos disponibles: {', '.join(dbs[:5])}")

        # Verificar si existe la base de datos configurada
        if settings.NOSQL_DB_NAME in dbs:
            db = client[settings.NOSQL_DB_NAME]
            collections = db.list_collection_names()
            print(f"   📑 Colecciones en '{settings.NOSQL_DB_NAME}': {len(collections)}")
            if collections:
                print(f"      └─ {', '.join(collections[:5])}")
        else:
            print(f"   ⚠️  Base de datos '{settings.NOSQL_DB_NAME}' no existe aún (se creará al insertar datos)")

        client.close()
        return True

    except ImportError:
        print("   ⚠️  pymongo no instalado (ejecuta: pip install pymongo)")
        return False
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        print(f"   📋 Tipo de error: {type(e).__name__}")

        # Diagnóstico específico
        error_str = str(e).lower()
        if "authentication failed" in error_str:
            print(f"   💡 Problema de AUTENTICACIÓN: Usuario o contraseña incorrectos")
        elif "connection refused" in error_str:
            print(f"   💡 Problema: Servidor rechaza conexión (apagado o firewall)")
        elif "timeout" in error_str:
            print(f"   💡 Problema: Timeout - firewall o red lenta")

        return False


def check_firewall_rules():
    """Verifica si hay reglas de firewall que puedan estar bloqueando"""
    print(f"\n🛡️  6. VERIFICACIÓN DE FIREWALL LOCAL")

    system = platform.system().lower()

    if system == 'darwin':  # macOS
        print("   💡 En macOS, verifica:")
        print("      - Preferencias del Sistema > Seguridad > Firewall")
        print("      - Asegúrate de que Python/PyCharm tenga permisos de red")
        print("      - Comando: /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate")
    elif system == 'linux':
        print("   💡 En Linux, verifica:")
        print("      - sudo iptables -L (reglas de firewall)")
        print("      - sudo ufw status (si usa UFW)")
    elif system == 'windows':
        print("   💡 En Windows, verifica:")
        print("      - Firewall de Windows Defender")
        print("      - wf.msc para ver reglas avanzadas")


def main():
    print("=" * 80)
    print("🔬 DIAGNÓSTICO COMPLETO DE CONEXIÓN A BASES DE DATOS")
    print("=" * 80)
    print()
    print("Este script determinará si el problema es:")
    print("  1. El servidor está apagado")
    print("  2. El firewall está bloqueando")
    print("  3. Las credenciales son incorrectas")
    print("  4. Hay un problema de red/configuración")
    print()

    # Cargar configuración
    try:
        from app.core.config import settings
        host = "darcano.duckdns.org"
        pg_port = 15433
        mongo_port = 47017
    except Exception as e:
        print(f"❌ No se pudo cargar la configuración: {e}")
        return

    # Tests progresivos
    results = {
        'dns': False,
        'ping': False,
        'pg_port': False,
        'mongo_port': False,
        'pg_connection': False,
        'mongo_connection': False
    }

    # 1. DNS
    ip = test_dns_resolution(host)
    results['dns'] = ip is not None

    # 2. Ping
    if results['dns']:
        results['ping'] = test_ping(host)
    else:
        print("\n⏭️  Omitiendo ping (DNS falló)")

    # 3. Puerto PostgreSQL
    if results['dns']:
        results['pg_port'] = test_port_connection(host, pg_port, "PostgreSQL", timeout=5)
    else:
        print(f"\n⏭️  Omitiendo prueba de puerto PostgreSQL (DNS falló)")

    # 4. Puerto MongoDB
    if results['dns']:
        results['mongo_port'] = test_port_connection(host, mongo_port, "MongoDB", timeout=5)
    else:
        print(f"\n⏭️  Omitiendo prueba de puerto MongoDB (DNS falló)")

    # 5. Conexión PostgreSQL
    if results['pg_port']:
        results['pg_connection'] = test_postgresql_connection()
    else:
        print("\n🐘 4. PRUEBA DE CONEXIÓN POSTGRESQL")
        print("   ⏭️  Omitida (puerto cerrado o no accesible)")

    # 6. Conexión MongoDB
    if results['mongo_port']:
        results['mongo_connection'] = test_mongodb_connection()
    else:
        print("\n🍃 5. PRUEBA DE CONEXIÓN MONGODB")
        print("   ⏭️  Omitida (puerto cerrado o no accesible)")

    # 7. Firewall
    check_firewall_rules()

    # Resumen final
    print("\n" + "=" * 80)
    print("📊 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 80)

    print(f"\n{'Prueba':<40} {'Estado':<20} {'Significado'}")
    print("-" * 80)
    print(f"{'1. Resolución DNS':<40} {'✅ OK' if results['dns'] else '❌ FALLA':<20} {'Dominio válido' if results['dns'] else 'Dominio no existe'}")
    print(f"{'2. Ping al servidor':<40} {'✅ OK' if results['ping'] else '⚠️  NO RESP':<20} {'Servidor activo' if results['ping'] else 'Firewall o apagado'}")
    print(f"{'3. Puerto PostgreSQL (15433)':<40} {'✅ ABIERTO' if results['pg_port'] else '❌ CERRADO':<20} {'Servicio activo' if results['pg_port'] else 'Servicio apagado'}")
    print(f"{'4. Puerto MongoDB (47017)':<40} {'✅ ABIERTO' if results['mongo_port'] else '❌ CERRADO':<20} {'Servicio activo' if results['mongo_port'] else 'Servicio apagado'}")
    print(f"{'5. Autenticación PostgreSQL':<40} {'✅ OK' if results['pg_connection'] else '❌ FALLA':<20} {'Credenciales OK' if results['pg_connection'] else 'Revisar credenciales'}")
    print(f"{'6. Autenticación MongoDB':<40} {'✅ OK' if results['mongo_connection'] else '❌ FALLA':<20} {'Credenciales OK' if results['mongo_connection'] else 'Revisar credenciales'}")

    # Diagnóstico y recomendaciones
    print("\n" + "=" * 80)
    print("💡 DIAGNÓSTICO Y RECOMENDACIONES")
    print("=" * 80)

    if not results['dns']:
        print("\n❌ PROBLEMA CRÍTICO: DNS no resuelve")
        print("   🔧 Solución:")
        print("      - Verifica que 'darcano.duckdns.org' esté correctamente configurado en DuckDNS")
        print("      - Prueba con nslookup darcano.duckdns.org")
        print("      - Como alternativa temporal, usa la IP directamente")
        print("\n   🎯 ESTO ES UN PROBLEMA DEL SERVIDOR (dominio mal configurado)")

    elif not results['pg_port'] and not results['mongo_port']:
        print("\n❌ PROBLEMA CRÍTICO: Ningún puerto responde")
        print("   🔧 Posibles causas:")
        print("      1. ❌ El servidor está APAGADO")
        print("      2. 🛡️  Firewall del servidor bloqueando TODO el tráfico externo")
        print("      3. 🔌 Los servicios PostgreSQL y MongoDB no están corriendo")
        print("      4. 🌐 Problema de red/ISP bloqueando conexiones")
        print("\n   🎯 ESTO ES UN PROBLEMA DEL SERVIDOR - No es tu culpa")
        print("\n   📞 ACCIÓN REQUERIDA: Contacta al administrador del servidor para:")
        print("      - Verificar que el servidor esté encendido")
        print("      - Iniciar servicios: sudo systemctl start postgresql mongod")
        print("      - Abrir puertos: sudo ufw allow 15433 && sudo ufw allow 47017")

    elif not results['pg_port']:
        print("\n❌ PROBLEMA: Puerto PostgreSQL (15433) no accesible")
        print("   🎯 ESTO ES UN PROBLEMA DEL SERVIDOR")
        print("   🔧 El administrador debe:")
        print("      1. Iniciar PostgreSQL:")
        print("         sudo systemctl start postgresql")
        print("      2. Verificar que escucha en el puerto correcto:")
        print("         sudo netstat -tulpn | grep 15433")
        print("      3. Abrir puerto en firewall:")
        print("         sudo ufw allow 15433/tcp")
        print("      4. Configurar postgresql.conf:")
        print("         listen_addresses = '*'")
        print("         port = 15433")
        print("      5. Configurar pg_hba.conf para aceptar conexiones remotas")

    elif not results['mongo_port']:
        print("\n❌ PROBLEMA: Puerto MongoDB (47017) no accesible")
        print("   🎯 ESTO ES UN PROBLEMA DEL SERVIDOR")
        print("   🔧 El administrador debe:")
        print("      1. Iniciar MongoDB:")
        print("         sudo systemctl start mongod")
        print("      2. Verificar que escucha en el puerto correcto:")
        print("         sudo netstat -tulpn | grep 47017")
        print("      3. Abrir puerto en firewall:")
        print("         sudo ufw allow 47017/tcp")
        print("      4. Configurar mongod.conf:")
        print("         net:")
        print("           port: 47017")
        print("           bindIp: 0.0.0.0")

    elif results['pg_port'] and not results['pg_connection']:
        print("\n⚠️  PROBLEMA: Puerto PostgreSQL abierto pero autenticación falla")
        print("   🔧 Posibles causas:")
        print("      1. Usuario 'air_quality_app' no existe")
        print("      2. Contraseña incorrecta")
        print("      3. Base de datos 'air_quality_db' no existe")
        print("      4. pg_hba.conf no permite la conexión desde tu IP")
        print("\n   🎯 Puede ser problema del servidor O de las credenciales proporcionadas")
        print("\n   📞 Verifica con el administrador:")
        print("      - Usuario: air_quality_app")
        print("      - Base de datos: air_quality_db")
        print("      - Permisos correctos")

    elif results['mongo_port'] and not results['mongo_connection']:
        print("\n⚠️  PROBLEMA: Puerto MongoDB abierto pero autenticación falla")
        print("   🔧 Posibles causas:")
        print("      1. Usuario 'air_quality_app' no existe en MongoDB")
        print("      2. Contraseña incorrecta")
        print("      3. authSource 'air_quality_config' incorrecto")
        print("      4. Base de datos 'air_quality_config' no existe")
        print("\n   🎯 Puede ser problema del servidor O de las credenciales proporcionadas")
        print("\n   📞 Verifica con el administrador:")
        print("      - Usuario: air_quality_app")
        print("      - Base de datos: air_quality_config")
        print("      - authSource: air_quality_config")

    elif results['pg_connection'] and results['mongo_connection']:
        print("\n✅ ¡TODO FUNCIONA PERFECTAMENTE!")
        print("   🎉 Ambas bases de datos están conectadas y autenticadas")
        print("   🚀 Tu configuración está CORRECTA")
        print("   ✨ Puedes ejecutar la aplicación sin problemas")
        print("\n   Comandos para iniciar:")
        print("      uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")

    # Conclusión final
    print("\n" + "=" * 80)
    print("🎯 CONCLUSIÓN FINAL")
    print("=" * 80)

    if results['pg_connection'] and results['mongo_connection']:
        print("\n✅ TU CONFIGURACIÓN ESTÁ PERFECTA - Todo funciona")
    elif not results['dns']:
        print("\n❌ PROBLEMA DEL SERVIDOR: Dominio DNS no configurado")
    elif not results['pg_port'] or not results['mongo_port']:
        print("\n❌ PROBLEMA DEL SERVIDOR: Servicios apagados o firewall bloqueando")
        print("   NO ES TU CULPA - El administrador debe revisar el servidor")
    else:
        print("\n⚠️  PROBLEMA DE CREDENCIALES: Puertos abiertos pero autenticación falla")
        print("   Verifica las credenciales con el administrador del servidor")

    print("\n" + "=" * 80)
    print("📝 COMANDOS ÚTILES PARA EL ADMINISTRADOR DEL SERVIDOR")
    print("=" * 80)
    print("""
# Verificar estado de servicios:
sudo systemctl status postgresql
sudo systemctl status mongod

# Iniciar servicios:
sudo systemctl start postgresql
sudo systemctl start mongod

# Verificar puertos en escucha:
sudo netstat -tulpn | grep -E '15433|47017'
sudo ss -tulpn | grep -E '15433|47017'

# Ver logs:
sudo tail -f /var/log/postgresql/postgresql-*.log
sudo tail -f /var/log/mongodb/mongod.log

# Firewall (ufw):
sudo ufw status
sudo ufw allow 15433/tcp comment 'PostgreSQL'
sudo ufw allow 47017/tcp comment 'MongoDB'
sudo ufw reload

# Probar localmente en el servidor:
psql -h localhost -p 15433 -U air_quality_app -d air_quality_db
mongosh "mongodb://air_quality_app:password@localhost:47017/air_quality_config?authSource=air_quality_config"
    """)

    print("=" * 80)
    print()


if __name__ == "__main__":
    main()

