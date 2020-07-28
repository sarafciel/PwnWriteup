![image](https://github.com/sarafciel/PwnWriteup/blob/master/redpwnCTF/secret-flag/secret-flag.png)

本題symbol是拿掉的，所以先進entry看  
可以知道libc_start_main之後跳到了FUN_0010091a上:  

![image](https://github.com/sarafciel/PwnWriteup/blob/master/redpwnCTF/secret-flag/secret-flag2.png)

看到程式碼就很明確了，程式先從flag.txt把flag讀進來  
然後留了一個format string的漏洞，長度限制在20byte  
我們先來看一下stack_frame的長相:  

![image](https://github.com/sarafciel/PwnWriteup/blob/master/redpwnCTF/secret-flag/secret-flag3.png)
rsp指到rbp-0x30的位置  
open打開的fd在-0x2c  
malloc要的chunk pointer在-0x28，這個同時也是flag讀進來存的位置  
所以算下來要leak的目標是[rsp +0x8]，相當於是stack上第二個參數  
按systemV規定的amd64 calling convention，前六個參數存在register  
第七個開始塞stack，我們要的相當於是第八個參數，而且要dereference  
所以foramt string要下%7$s  

