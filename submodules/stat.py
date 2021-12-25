# Warning! Shit code.
from os import system


def show_stat(self):
    port = self.port
    clients = self.clients
    max_conns = self.clients.capacity
    sent = self.socket.total_sent
    recv = self.socket.total_recv
    system("clear")
    stat = print(
        f"""
========= Server is started =========
Port: {port}
======== Max connections: {max_conns} ========
{len(clients)} clients online!
"""
    )

    print(
        """
------------------------------------
ID     Client IP:PORT        Ping
------------------------------------
""",
        end="",
    )
    for client in clients:
        print(
            f"{str(client['id']).ljust(7)}{(str(client['addres'][0])+':'+str(client['addres'][1])).ljust(22)}{'1ms.'.ljust(7)}"
        )
    print("------------------------------------")

    

    print(
        f"""

=====================================
= Total data sent: {(str(sent//1024)+'KB.').ljust(17)}=
= Total data recived: {(str(recv//1024)+'KB.').ljust(14 )}=
====================================="""
    )
