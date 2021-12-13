# Warning! Shit code.
from os import system


def show_stat(port: int, clients, max_conns: int):
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
    stat += """

=====================================
= Total data sent: 9KB.             =
= Total data recived: 3KB           =
====================================="""
    print(stat)
