import socket
import board
import neopixel  # Adafruit
import click

# defaults that mirror the hardcoded values used previously
DEFAULT_IP = "0.0.0.0"  # Listen on all interfaces
DEFAULT_PORT = 19444  # Must match Hyperion's output port
DEFAULT_LED_COUNT = 64  # 8x8 matriz
DEFAULT_LED_PIN = "D18"  # name of the board pin
DEFAULT_ORDER = "GRB"  # color order for the strip


@click.command()
@click.option("--ip", "-i", default=DEFAULT_IP, help="IP address to listen on")
@click.option(
    "--port", "-p", default=DEFAULT_PORT, type=int, help="UDP port to bind to"
)
@click.option(
    "--led-count",
    "-c",
    default=DEFAULT_LED_COUNT,
    type=int,
    help="Number of LEDs in the strip/matrix",
)
@click.option(
    "--led-pin",
    "-P",
    default=DEFAULT_LED_PIN,
    help="Board pin name connected to DIN (e.g. D18)",
)
@click.option(
    "--order",
    "-o",
    default=DEFAULT_ORDER,
    help="Color order for NeoPixel (e.g. RGB, GRB)",
)
def main(ip, port, led_count, led_pin, order):
    """Run the Hyperion UDP listener and drive the NeoPixel strip.

    All of the configuration values from the original script are available as
    command-line options; the hardcoded values are used as defaults so the
    behaviour is unchanged when invoked without arguments.
    """

    udp_ip = ip
    udp_port = port

    # resolve board pin and neopixel order from the provided strings
    try:
        pin = getattr(board, led_pin)
    except AttributeError:
        raise click.BadParameter(f"{led_pin!r} is not a valid board pin")

    try:
        color_order = getattr(neopixel, order)
    except AttributeError:
        raise click.BadParameter(f"{order!r} is not a valid NeoPixel color order")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))

    print(f"Escuchando paquetes UDP en {udp_ip}:{udp_port} ...")

    pixels = neopixel.NeoPixel(
        pin, led_count, auto_write=False, pixel_order=color_order
    )

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            # Cada LED = 3 bytes
            for i in range(led_count):
                r = data[i * 3]
                g = data[i * 3 + 1]
                b = data[i * 3 + 2]
                pixels[i] = (r, g, b)
            pixels.show()
    except KeyboardInterrupt:
        print("Cerrando...")
        pixels.fill((0, 0, 0))
        pixels.show()
        sock.close()


if __name__ == "__main__":
    main()
