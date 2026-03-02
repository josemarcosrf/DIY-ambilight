use tokio::net::UdpSocket;
use std::error::Error;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let socket = UdpSocket::bind("0.0.0.0:19444").await?;
    println!("Escuchando paquetes UDP en 0.0.0.0:19444 ...");

    let mut buf = [0u8; 1024];

    loop {
        let (len, addr) = socket.recv_from(&mut buf).await?;
        println!("Paquete recibido de {} ({} bytes)", addr, len);
        println!("Primeros 24 bytes (8 LEDs): {:?}", &buf[..len.min(24)]);
    }
}
