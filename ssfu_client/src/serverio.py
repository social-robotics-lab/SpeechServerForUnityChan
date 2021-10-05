import socket

def recv(ip:str, port:int) -> str:
    conn = connect(ip, port)
    size = read_size(conn)
    data = read_data(conn, size)
    close(conn)
    return data.decode('utf-8')

def send(ip:str, port:int, data:str):
    conn = connect(ip, port)
    size = len(data)
    conn.send(size.to_bytes(4, byteorder='big'))
    conn.send(data)
    close(conn)

def connect(ip:str, port:int):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((ip, port))
    return conn

def close(conn:socket):
    conn.shutdown(1)
    conn.close()

def read_size(conn:socket):
    b_size = conn.recv(4)
    return int.from_bytes(b_size, byteorder='big')

def read_data(conn:socket, size:int):
    chunks = []
    bytes_recved = 0
    while bytes_recved < size:
        chunk = conn.recv(size - bytes_recved)
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        chunks.append(chunk)
        bytes_recved += len(chunk)
    return b''.join(chunks)
