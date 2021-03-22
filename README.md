# poslite
POS application developed using python tkinter and sqlite

SETUP
-----
1) Install python version 3.7.3
2) Set path to python folder
3) In command prompt type 'python' and ensure it is launched
4) In python prompt click control z and enter to exit to command prompt
5) Install SQLite version 3.28.0
6) Set path to SQLite folder
7) In command prompt type 'sqlite' and ensure it is launched
8) In sqlite prompt type '.open POSLITE'
9) In sqlite prompt type 'CREATE TABLE items(item_code TEXT PRIMARY KEY, item_name TEXT, unit_price REAL);'
10) In sqlite prompt type 'INSERT INTO items values('ZZ10001099','Fenugreek seed',12.0);'
11) In sqlite prompt type 'INSERT INTO items values('ZZ10001100','Brinjal',35.0);'
12) In sqlite prompt type 'INSERT INTO items values('ZZ10001101','Sugar',30.0);'
13) In sqlite click control z and enter to exit to command prompt
14) Create folder 'poslite' in c:\
15) In command prompt change directory to poslite
16) Copy 'poslite.py' program in this folder
17) In command prompt type 'python poslite' 

USAGE
-----
Create Items in Billing List:
1) Enter a valid 10 character Barcode in the Top Entry field
2) A new Item row will be inserted into the Item Table with corresponding Item name and Unit price.
3) Quantity will be 1 by default
4) Repeat the above step for 2 more valid Barcodes
5) There will be 3 rows in the Item Table

Delete an Item from Billing List:
1) Set focus to Item table by clicking tab
2) First row of Item table will be highlighted
3) Using Up and Down arrow keys select the item to be deleted
4) Click Del key
5) The selected item will be deleted

Change the Quantity of an Item in the Billing List:
1) Set focus to Item table by clicking tab
2) First row of Item table will be highlighted
3) Using Up and Down arrow keys select the item for which the quantity has to be changed
4) Click Right arrow key to increase quantity by 1
5) Click Left arrow key to decrease quantity by 1
