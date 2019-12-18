from PIL import Image
import io
import SQLUtilities
import os


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


def sendimage(s,image):
    bytes = bytearray(image)
    size = len(bytes)
    size = size.to_bytes(size.bit_length(), byteorder='big')
    s.send(size)
    answer = s.recv(4096)
    # send image to server
    if answer == b'GOT SIZE':
        s.sendall(bytes)

        # check what server send
        answer = s.recv(4096)
        if answer == b'GOT IMAGE':
            None
        else:
            print("send error")
            return

def SeparateData(data):
    commands = data.split(";")
    return commands


def ReadCommand(command):
    list = command.split("::")
    return list


def ReciveImage(connection):
    data = connection.recv(4096)
    size = int.from_bytes(data, "big")
    connection.sendall(b'GOT SIZE')
    data = recvall(connection,size)
    image = Image.open(io.BytesIO(data))
    connection.sendall(b"GOT IMAGE")
    return image


def run(connection):
        data = SeparateData(str(connection.recv(4096).decode()))
        username = None
        password = None
        for cmd in data:
            read = ReadCommand(cmd)
            if read[0] == "user":
                username = read[1]
            elif read[0] == "password":
                password = read[1]
            else:
                connection.sendall(b"ack::n")
                print(username + " rejected")
                return
        if SQLUtilities.TryConnection(username, password) == False:
            connection.sendall(b"ack::n")
            print(username + " rejected")
        else:
            connection.sendall(b"ack::y")
            print(username + " ready")
            try:
                while True:
                    data = SeparateData(connection.recv(4096).decode())
                    for cmd in data:
                        read = ReadCommand(cmd)
                        print(read)
                        if read[0] == "getimg":
                            cursor = SQLUtilities.ExecuteQuery("Select img from pictures where name = '"+read[1]+"'", username, password)
                            data2 = cursor.fetchval()
                            print(data2)
                            leng = len(data2)
                            connection.sendall(str(leng).encode())
                            connection.sendall(data2)

                        elif read[0] == "getcloud":
                            cursor = SQLUtilities.ExecuteQuery("Select img from clouds where name = '"+read[1]+"'", username, password)
                            data2 = cursor.fetchval()
                            print(data2)
                            leng = len(data2)
                            connection.sendall(str(leng).encode())
                            connection.sendall(data2)

                        elif read[0] == "sql":
                            cursor = SQLUtilities.ExecuteQuery(read[1], username, password)
                            data2 = cursor.fetchall()
                            connection.sendall(data2)
                        elif read[0] == "approve":
                            SQLUtilities.InsertData("Update clouds set approved = 'y' where name= '"+read[1]+"'", username, password)
                        elif read[0] == "sendimg":
                            connection.sendall(("ack").encode())
                            image = ReciveImage(connection)
                            image.save(read[1] + ".jpg")
                            SQLUtilities.InsertImage(read[1] + ".jpg", read[1], username, password)
                            #SQLUtilities.InsertData("update pictures set [user] = "+username+",timestamp = CURRENT_TIMESTAMP WHERE name = " + read[1], username, password)
                            if os.path.exists(read[1]+".jpg"):
                                os.remove(read[1]+".jpg")
                        elif read[0] == "sendcloud":
                            connection.sendall(("ack").encode())
                            image = ReciveImage(connection)
                            image.save(read[1] + ".jpg")
                            SQLUtilities.InsertCloud(read[1] + ".jpg", read[1], username, password)
                            if os.path.exists(read[1]+".jpg"):
                                os.remove(read[1]+".jpg")
                        elif read[0] == "getall":
                            cursor = SQLUtilities.ExecuteQuery("Select name from pictures where [user] = '"+username+"'", username, password)
                            data2 = cursor.fetchall()
                            toSend = ""
                            for d in range(len(data2)):
                                toSend = toSend + str(data2[d][0])
                                if d != len(data2) -1:
                                    toSend = toSend + "!@"
                            connection.sendall(toSend.encode())
                        else:
                            connection.sendall(("error::exception in protocol").encode())
            except Exception as e:
                print(str(e))
                connection.sendall(("error:closing").encode())
            finally:
                # Clean up the connection
                connection.close()
