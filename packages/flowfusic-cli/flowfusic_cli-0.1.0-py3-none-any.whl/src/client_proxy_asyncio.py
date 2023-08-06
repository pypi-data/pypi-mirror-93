import asyncio
import socket, ssl
import jwt
import datetime


class ParaviewSocketClient:
    """
    Proxy socket client for paraview

    Connects with paraview local client and backend cloud proxy server
    """

    def __init__(self, token=False):
        if token:
            self.token = token
        else:
            self.token = self.__getKey()

        self.api_address = self.__getApiAddress()

    # used in dev only:
    def __getKey(self):
        encoded_jwt = jwt.encode(
            {
                "username": "mskarysz_user6",
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            "kksjdfhkjsdf",
            algorithm="HS256",
        )

        return encoded_jwt.decode()

    def __getApiAddress(self):
        return ("api.gcp.flowfusic.com", 8081)

    async def __pipe(self, reader, writer):
        try:
            while not reader.at_eof():
                writer.write(await reader.read(2048))
        finally:
            writer.close()

    async def __auth(self, reader, writer):
        # send auth header:
        writer.write(("Auth " + self.token).encode())
        await writer.drain()

        msg = ""
        data = await reader.read(1024)
        while data:
            msg = data.decode()
            if (msg == "auth_ok") or (msg == "auth_not_ok"):
                break
            data = await reader.read(1024)
        return msg == "auth_ok"

    async def __ready(self, reader, writer):

        msg = ""
        data = await reader.read(1024)
        while data:
            msg = data.decode()
            if (msg == "render_server_ready") or (msg == "render_server_not_ready"):
                break
            data = await reader.read(1024)
        return msg == "render_server_ready"

    async def __handle_client(self, reader, writer):

        withSsl = True

        if withSsl:
            context = ssl.create_default_context()
        else:
            context = None

        try:
            remote_reader, remote_writer = await asyncio.open_connection(
                self.api_address[0], self.api_address[1], ssl=context, loop=self.loop
            )

            addrto = remote_writer.get_extra_info("peername")
            addrfrom = writer.get_extra_info("peername")

            isauth = await self.__auth(remote_reader, remote_writer)

            if isauth:
                isready = await self.__ready(remote_reader, remote_writer)
                if isready:
                    try:
                        pipe1 = self.__pipe(reader, remote_writer)
                        pipe2 = self.__pipe(remote_reader, writer)

                        print("[+] piping", addrfrom, "to", addrto)

                        await asyncio.gather(pipe1, pipe2)

                    except ConnectionResetError:
                        pass
                    finally:
                        print("[-]", "Close the connection", addrfrom, "to", addrto)
                        writer.close()
                        remote_writer.close()
                else:
                    print("[-] render server not ready")
                    print("[-]", "Close the connection", addrfrom, "to", addrto)
                    writer.close()
                    remote_writer.close()
            else:
                print("[-] auth not ok")
                print("[-]", "Close the connection", addrfrom, "to", addrto)
                writer.close()
                remote_writer.close()

        except ConnectionRefusedError:
            print("Cannot connect to the server. Try again.")
            writer.close()

        if self.stop_when_closed:
            self.server.close()
            await self.server.wait_closed()
            self.loop.stop()

    def setup_server(self):

        self.loop = asyncio.get_event_loop()
        coroutine = asyncio.start_server(
            self.__handle_client, "127.0.0.1", 0, loop=self.loop
        )

        self.server = self.loop.run_until_complete(coroutine)
        print("Serving on {}".format(self.server.sockets[0].getsockname()))

        self.address = self.server.sockets[0].getsockname()

    def __run_server(self, stop_when_closed=False):
        self.stop_when_closed = stop_when_closed
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

        print("Closing server...")
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.close()

    def run_server(self):
        self.__run_server(stop_when_closed=True)

    def run_server_forever(self):
        self.__run_server()


if __name__ == "__main__":
    ParaviewSocketClient().run_server_forever()