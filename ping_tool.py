import subprocess
import platform
from datetime import datetime

def check_host_status(host):
    """
    Verifica si un host (IP o dominio) está en línea usando el comando ping
    """
    
    # 1. Validación: Si el host está vacío, salimos
    if not host:
        print("Error: No has ingresado ningún host.")
        return

    # 2. Definir los parámetros de ping según el sistema operativo (OS)
    if platform.system().lower() == 'windows':
        command = f"ping -n 1 {host}" 
        shell_execution = True
        command_list = None
    else:
        command = ['ping', '-c', '1', host]
        shell_execution = False
        command_list = command

    try:
        # 3. Ejecutar el comando
        result = subprocess.run(
            command if shell_execution else command_list, # Pasa la cadena o la lista
            shell=shell_execution,
            capture_output=True, 
            text=True, 
            timeout=5,
            check=False # No lanza excepción por un código de retorno distinto de 0
        )

        # 4. VERIFICACIÓN CLAVE: returncode
        if result.returncode == 0:
            status = "UP (En Línea)"
            color = "\033[92m" # Verde
        else:
            status = "DOWN (Fuera de Línea)"
            color = "\033[91m" # Rojo
            
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Host: {host} -> {color}{status}\033[0m")
        
        # Debug para returncode de result por si el ping no se ejecuta bien.
        # if result.returncode != 0:
        #     print(f"   DEBUG - CMD: {command}")
        #     print(f"   DEBUG - STDOUT: {result.stdout.strip()}")
        
    except Exception as e:
        # Error 
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Host: {host} -> Error al intentar hacer ping: {e}")

if __name__ == "__main__":
    print("\n--- Ping Tool ---")
    
    # 1. Objetivos
    hosts_input = input("Ingresa Hosts/IPs (separados por coma o espacio): ")
    
    # 2. List comprehension para iterar sobre la lista
    hosts = [h.strip() for h in hosts_input.replace(',', ' ').split() if h.strip()]

    if not hosts:
        print("No se ingresaron hosts. Saliendo.")
    else:
        print(f"\nVerificando {len(hosts)} hosts...")
        # 3. ITERAR: Aquí se pasa CADA HOST a la función
        for host in hosts:
            check_host_status(host)
            
    print("\n--- Verificación Finalizada ---")