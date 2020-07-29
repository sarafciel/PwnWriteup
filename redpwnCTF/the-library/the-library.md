![image](https://github.com/sarafciel/PwnWriteup/blob/master/redpwnCTF/the-library/the-library1.png)

先下checksec，可以看到除了NX其他都沒有開  

![image](https://github.com/sarafciel/PwnWriteup/blob/master/redpwnCTF/the-library/the-library2.png)

下objdump -d看assembly，這題的code很單純，main開了一個大小為0x10的buffer  
但read的時候長度是0x100，所以我們有bof的空間  
由於NX有開，本題沒意外就是要寫rop chain來解了  

![image](https://github.com/sarafciel/PwnWriteup/blob/master/redpwnCTF/the-library/the-library3.png)

先看一下got hajacking時可以用的東西，有setbuf、puts跟read  

![image](https://github.com/sarafciel/PwnWriteup/blob/master/redpwnCTF/the-library/the-library4.png)

下ropgadget看有那些東西可用，可以看到有一個pop rdi，  
所以我們可以改掉rdi之後跳到puts上面做leak  

![image](https://github.com/sarafciel/PwnWriteup/blob/master/redpwnCTF/the-library/the-library5.png)

由於本題很好心的有附上使用的libc.so，所以直接拿one-gadget找可以用的execve("//bin//sh")  
這裡挑了第二個offset[0x4f322]，因為條件比較簡單  

到這邊整理一下流程就差不多了
1.利用bof蓋掉ret address組rop chain  
2.把rdi改成想要leak的位置後跳回main function裡的puts做leak，這裡選read的libc位置  
3.程式繼續執行到read，組第二個payload，此時我們已經有read的libc位置，可以算出one-gadget在libc的位置  
4.在滿足one-gadget要求的條件(rsp+0x40 == null)下把算好的位置重新塞回去即可拿到shell  
