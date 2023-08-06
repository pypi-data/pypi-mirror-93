import socket

host = socket.gethostbyname(socket.gethostname())
port = 8085                   

with socket.socket() as s:
  s.connect((host,port))

  file = open('enviar.pdf', 'rb')

  document = file.read()

  s.sendall(document)
  print("Enviado!!!")

  file.close()
  s.close()
