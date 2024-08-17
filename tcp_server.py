import socket # imports the socket mod
import time # imports the time mod

def __main():
    # connecting by going to "localhost:8080" in a web browser

    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 8080

    # connection process for TCP
    # 1. client to server; 2. server to client acknowledgement; 3. client to server acknowledgement 4. connection opened

    # socket.AF_INET => indicates that we are creating an IPv4 type web socket
    # socket.SOCK_STREAM => TCP type web socket
    my_server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); # creates a socket; socket.SOCK_DGRAM == UDP connection instead

    # socket.SOL_SOCKET => TCP/IP protocol level independent
    # socket.SOL_REUSEADDR => socket reuse directly following connection close
    my_server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    # bind the IPv4 address to a specific port
    # 0.0.0.0 => allows us to access server eveywhere, while passing "127.0.0.1" would only allow local access
    # 8080 => port number not bound to the OS
    my_server_sock.bind((SERVER_HOST, SERVER_PORT))

    # 5 => maximum number of allowed connections in the connection queue
    my_server_sock.listen(5) # allows server to begin listening for incoming connections within a queue

    print(f"Server listening on port {SERVER_PORT}") # message to the end user to indicate that the server is ready to accept incoming connections

    # infinite listening loop
    while True:
        # returns a tuple containing the clients socket and the IPv4 address of the client
        cli_socket, cli_addr = my_server_sock.accept() # begins to proceess connections in the queue
        req = cli_socket.recv(1024).decode() # receives data and specifies maximum number of bytes per packet and converts it to a string
        http_headers = req.split('\n') # spilts the request by a newline character
        topline_header_components = http_headers[0].split() # prints the http method used

        http_method = topline_header_components[0]
        path = topline_header_components[1] 

        if http_method == 'GET':
            if path == '/': # if we are going directly to the page...
                file_input = open('index.html') # open my basic html file inr ead only mode

            elif path == '/about': # if we add an about extension to the page...
                file_input = open('about.json') # open my basic html file inr ead only mode

            else:
                res = 'HTTP/1.1 404 Not Found\n\n<h1>404 Not Found</h1>'
                continue

            shown_content = file_input.read() # read the file
            file_input.close() # close the file

            res = 'HTTP/1.1 200 STATUS_OK\n\n' + shown_content 

        else:
            # implement 404n not fout message
            pass

        cli_socket.sendall(res.encode()) # sends the entirety of the response to the client encoded back into bytes from a string
        cli_socket.close() # closes the client socket

__main() # calls the server to be created

