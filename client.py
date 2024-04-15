#Cliente
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Conexión con el servidor
host = 'localhost'
port = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Generar par de claves RSA
key = RSA.generate(2048)
public_key = key.publickey().export_key()
client_socket.send(public_key)

# Recibir clave pública del servidor
server_public_key = client_socket.recv(4096)

# Crear objeto para cifrar con la clave pública del servidor
cipher = PKCS1_OAEP.new(RSA.import_key(server_public_key))

while True:
    # Mensaje a cifrar y enviar al servidor
    message = input("Ingrese el mensaje que desea cifrar y enviar al servidor: ").encode()

    encrypted_message = cipher.encrypt(message)
    client_socket.send(encrypted_message)

    if message.lower() == b'exit':
        break
# Cerrar conexión
client_socket.close()