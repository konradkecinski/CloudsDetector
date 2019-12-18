import socket
import SQLUtilities
import ClientHandler
import threading

#x = SQLUtilities.ExecuteQuery("SELECT img FROM pictures where id = 16","Admini","123Admini123")
#x = SQLUtilities.InsertImage("pictures", "[img]", "test.jpg", "Admini", "123Admini123")
# data = x.fetchval()
# with open('new.jpg', 'wb') as new_jpg:
#     new_jpg.write(data)
#     print(data)
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
server_address = ('localhost', 10000)
print('starting up on %s port %s' % server_address)
serversocket.bind(server_address)

# Listen for incoming connections
serversocket.listen(10)
while True:
    conn, addr = serversocket.accept()
    print("[-] Connected to " + addr[0] + ":" + str(addr[1]))
    x = threading.Thread(target=ClientHandler.run, args=(conn,))
    x.start()
