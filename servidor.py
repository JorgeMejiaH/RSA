#Servidor
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Configuración del servidor
host = 'localhost'
port = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print(f"Servidor escuchando en {host}:{port}")

# Aceptar conexión entrante
client_socket, addr = server_socket.accept()
print(f"Conexión entrante desde {addr}")

# Generar par de claves RSA para el servidor
server_key = RSA.generate(2048)
server_public_key = server_key.publickey().export_key()
server_private_key = server_key.export_key()

# Enviar clave pública del servidor al cliente
client_socket.send(server_public_key)

# Recibir clave pública del cliente
client_public_key = client_socket.recv(4096)

# Crear objeto para cifrar con la clave pública del cliente
cipher = PKCS1_OAEP.new(RSA.import_key(client_public_key))

while True:
    # Recibir mensaje cifrado del cliente
    encrypted_message = client_socket.recv(4096)

    # Utilizar clave privada del servidor para descifrar el mensaje
    cipher_server = PKCS1_OAEP.new(server_key)
    decrypted_message = cipher_server.decrypt(encrypted_message)

    print("Mensaje cifrado recibido:", encrypted_message)
    print("\nMensaje decifrado recibido:", decrypted_message.decode())

    # Si se recibe un mensaje de salida, salir del bucle
    if decrypted_message.lower() == b'exit':
        break
    
# Cerrar conexión
client_socket.close()
server_socket.close()