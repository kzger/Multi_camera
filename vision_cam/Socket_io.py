import socket
import multiprocessing as mp

class socket_io(object):

    def __init__(self):
        self.ip = self.get_host_ip()
        self.connected = False


    def get_host_ip(self):
        try:
            st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            st.connect(('192.168.0.1', 80))
            ip = st.getsockname()[0]
        except socket.error as msg:
            print("socket error: ", msg)
            return 0
        finally:
            if "st" in locals():
                st.close()
        return ip

    def setting_server(self):
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse tcp
                print("Socket ok")
                s.bind((str(self.ip), 9999))
                s.listen(2)
                break
            except socket.error as msg:
                s.close()
                print('Could not open socket: ', msg)
                continue
        return s

    def connection_process(self, queue):
        s = self.setting_server()
        while True:
            if not self.connected:
                print("waiting connection")
                sock, addr = s.accept()
                self.connected = True
            else:
                try:
                    data = sock.recv(1024).decode('ascii')
                    queue.put(data)
                    sock.close()
                except socket.error:
                    self.connected = False

    def run_socket(self):
        queue = mp.Queue(maxsize=2)
        # Test daemon
        tmp_p = mp.Process(target=self.connection_process, args=(queue, ))
        tmp_p.daemon = True
        tmp_p.start()
        return queue



if __name__ == "__main__":
    ip = get_host_ip()
    print(f"IP:{ip}")
