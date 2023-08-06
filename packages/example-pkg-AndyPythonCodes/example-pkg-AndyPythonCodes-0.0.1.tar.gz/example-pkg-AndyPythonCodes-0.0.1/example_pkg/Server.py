import socket

host = socket.gethostbyname(socket.gethostname())
port = 8085

with socket.socket() as s:
   s.bind((host, port))            

   s.listen()                     
   client , address = s.accept()

   document = open("recibido.pdf", "wb")

   while True:
      data = client.recv(1024)
      if data:
         document.write(data)
      else:
         break

   document.close()
   print("Recibido!!!")

   #Este cliente ha terminado de enviar, pero aún puede recibir
   client.shutdown(1)

   client.close()
   s.close()