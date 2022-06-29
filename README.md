### Documentation and Notes

* * *

## RESTRUCTURED --- 
I restructured everything into two files. Please study about classes and objects if you need to. This is pretty good code.  But certainly not great yet. :)

**btcscan.py** contains all the working scanner code, but reorganized into a class.  The GOAL is that there are not any print statements generated here.  Objects should return data and the caller can choose if to print or not.  

The **class btcscan** is structured so we can make it multithreaded fairly easily.  Then we can increase performance.

**main.py** contains the basic control.  I also added the ability to manually load addressses without editing the code.  Just fill in the dictionary.  


* * *

## TODO List - TEXT version
1. [done] Implement Functions and Objects
2. [done] Add ability to manually enter a btc address
3. [done] Keep count from where left off so we have all-time counts.

## TODO List - Graphical version
1. Add a graphical interface with TK and/or HTML
2. Display all discovered data on screen, including historical
3. Add refresh button that rechecks known hits for current balance.
4. Upload results into Google firebase database
5. Show all scanning output in UI
6. Build database of all tested wallet IDs to prevent rescanning

* * * 


