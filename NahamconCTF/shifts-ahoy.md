# Shifty-ahoy

丟進ghidra，稍微修一下main function的變數名稱後，如下圖：  

![image](https://raw.githubusercontent.com/sarafciel/PwnWriteup/master/NahamconCTF/image.png)


本題是一個有加密跟解密功能的程式，選1會對輸入的字串做加密的動作，選2會跳出迴圈，然後執行decrypt。  
我們再進到encrypt去看：  

![image](https://github.com/sarafciel/PwnWriteup/blob/master/NahamconCTF/shifts-ahoy2.png)

fgets能塞的大小是0x60，buffer是72(0x48)，明顯是有buffer overflow可以用的

![image](https://github.com/sarafciel/PwnWriteup/blob/master/NahamconCTF/shifts-ahoy3.png)

整個encypt的stack frame是0x50，算上rbp跟return address，相當於0x50+0x08*2 = 0x60  
也就是說這題的overflow剛剛好是可以蓋到return address的長度，這是這一題考驗的地方  

checksec後可發現沒有保護，所以可以塞shellcode  
剩下來的難點就是怎麼去leak出來shellcode的address，或是把shellcode塞到我們已知的位置上去  
這邊採用後者，利用stack pivoting先把rbp改成某個.data段上面的位置:

![image](https://github.com/sarafciel/PwnWriteup/blob/master/NahamconCTF/shifts-ahoy4.png)

執行完 **[0x4012e5] leaveq**
後rbp就會改到我們要的某個位置上，由於整個encrypt，包含fgets的部分都是rbp based的  
所以return address我們可以直接塞 **[0x401257]** 重跑一次encrypt  
此時fgets就會讀到rbp - 0x50的位置上面去  
shellcode的位置就是已知了(rbp-0x50)，所以第二次fgets把這個值跟shellcode塞到return address去即可拿到shell  
最後由於這一段有做一個簡單的+0xd的加密，在shellcode上面做-0xd的動作補回來即可
