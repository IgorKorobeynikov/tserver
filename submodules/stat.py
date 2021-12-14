# Warning! Shit code.
from os import system


def show_stat(self):
    port = self.port
    clients = self.clients
    max_conns = self.clients.capacity
    sent = self.total_sent
    recv = self.total_recv
    system("clear")
    stat = f"""
========= Server is started =========
Port: {port}
======== Max connections: {max_conns} ========
{len(clients)} clients online!
"""

    some_bruh = """
————————————————————————————————————
ID     Client IP:PORT        Ping
————————————————————————————————————
"""
    for client in clients:
        some_bruh += f"{'?'.ljust(7)}{(str(client[0])+':'+str(client[1])).ljust(22)}{'1ms.'.ljust(7)}\n"
    some_bruh += "————————————————————————————————————"

    stat += some_bruh
    stat += f"""

=====================================
= Total data sent: {(str(sent//1024)+'KB.').ljust(17)}=
= Total data recived: {(str(recv//1024)+'KB.').ljust(14 )}=
====================================="""
    print(stat)
