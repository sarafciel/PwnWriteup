# Conveyor

丟進ghidra，main function如下：  

![image](https://github.com/sarafciel/PwnWriteup/blob/master/NahamconCTF/conveyor/conveyor1.png)
  
題目是一個選單，看起來是heap題，選單的功能如下：  
0.exit  
1.add_part  
2.safty_check
  
![image](https://github.com/sarafciel/PwnWriteup/blob/master/NahamconCTF/conveyor/conveyor2.png)
  
先看一下add_part  
add_part會去要一塊大小0x80的chunk，然後做寫入的動作  
寫入後會有一個strstr的check，檢查輸入是否有sh  
如果有就直接free掉剛剛這塊chunk，沒有就會塞上一塊要到的chunck pointer到offset 0x78的位置上
  
![image](https://github.com/sarafciel/PwnWriteup/blob/master/NahamconCTF/conveyor/conveyor3.png)

然後是safety_check的部分  
safty_check會先印出chunk，然後問這個part是否安全，  
若否則可以重新對這個part做寫入，然後用offset 0x78的pointer access下一個chunk  
值得注意的是就算是重新寫入，程式依然會access下一個chunk  
而這邊給的大小是0x80，也就代表我們可以改掉0x78的pointer後在這邊把它印出來  
就可以leak出任意位置的內容  

同樣在這邊leak完之後選N可以再做一次寫入  
所以這邊直接做got hijacking，  
先leak出幾個libc function的位置再用https://libc.blukat.me/  
可以算出題目主機用的libc version是2.27  
然後再用leak出來的位置去算出來system，然後做got hajacking改掉got的某個函式  
因為add_part裡strstr的參數可控，因此這裡挑strstr來用





