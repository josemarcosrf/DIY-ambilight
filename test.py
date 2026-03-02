import socket
import click

# Parámetros por defecto para la escucha UDP
DEFAULT_IP = "0.0.0.0"  # Escucha en todas las interfaces
DEFAULT_PORT = 19444


@click.command()
@click.option("--ip", "-i", default=DEFAULT_IP, help="IP address to listen on")
@click.option(
    "--port", "-p", default=DEFAULT_PORT, type=int, help="UDP port to bind to"
)
def main(ip, port):
    """Simple UDP listener for Hyperion packets.

    You can configure the IP and port via command line options.
    """
    udp_ip = ip
    udp_port = port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))

    print(f"Escuchando paquetes UDP en {udp_ip}:{udp_port} ...")

    try:
        while True:
            data, addr = sock.recvfrom(1024)  # tamaño máximo de paquete
            print(f"Paquete recibido de {addr}, {len(data)} bytes")
            # Normalmente Hyperion envía RGB por LED
            print(
                list(data[: min(24, len(data))])
            )  # imprime los primeros 8 LEDs (3 bytes cada uno)
    except KeyboardInterrupt:
        print("Cerrando listener...")
        sock.close()


if __name__ == "__main__":
    main()
