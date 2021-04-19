_M='Helvetica 11'
_L='Left'
_K='Right'
_J='Delete'
_I='Tab'
_H='oddrow'
_G='#5'
_F='#4'
_E='#3'
_D='#2'
_C='#1'
_B='values'
_A='evenrow'
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import sqlite3
def event_treeListSelected(event):
	global tree_idx
	for A in tk_tree_bill_items.selection():tree_idx=tk_tree_bill_items.index(A);print('index@select='+str(tree_idx))
def event_bind_barcode(bind_barcode):
	A=bind_barcode;global db_cur;global tree_row_prev
	if len(A.get())>9:
		db_cur.execute("SELECT item_name, unit_price from items where item_code = '"+A.get()+"'");B=db_cur.fetchone()
		if B is None:print('Item not found')
		else:
			item_name.set(B[0]);D=float(B[1]);E=1.0;F=D*E
			if tree_row_prev==_A:C=_H
			else:C=_A
			tk_tree_bill_items.insert('',tk.END,values=(A.get(),item_name.get(),str(E),str(D),str(F)),tags=(C,));A.set('');get_item_total();tree_row_prev=C
def event_keyClick(event,arg):
	K='tags';J='.!panedwindow.!frame2.!treeview';D=arg;global tree_idx;global bind_bill_tot;print(D,tk_root.focus_get());A=tk_tree_bill_items.focus();H=tk_tree_bill_items.next(A);I=tk_tree_bill_items.prev(A)
	if D==_I:
		if str(tk_root.focus_get())=='.!panedwindow.!frame.!entry':
			if len(tk_tree_bill_items.get_children())>0:A=tk_tree_bill_items.get_children()[0];tk_tree_bill_items.focus(A);tk_tree_bill_items.selection_set(A);get_item_total()
	if D==_J:
		if str(tk_root.focus_get())==J:
			if len(tk_tree_bill_items.get_children())>0:
				tk_tree_bill_items.delete(A)
				if len(tk_tree_bill_items.get_children())>0:
					if H!='':A=H
					elif I!='':A=I
					else:A=''
					tk_tree_bill_items.focus(A);tk_tree_bill_items.selection_set(A)
			get_item_total()
	if D==_K:
		if str(tk_root.focus_get())==J:
			if len(tk_tree_bill_items.get_children())>0:B=tk_tree_bill_items.item(A)[_B];E=tk_tree_bill_items.item(A)[K];print(str(B[1]));tk_tree_bill_items.delete(A);C=float(B[2]);C=C+1;F=float(B[3]);G=F*C;B[2]=str(C);B[4]=str(G);tk_tree_bill_items.insert('',tree_idx,values=B,tags=E);A=tk_tree_bill_items.get_children()[tree_idx];print(tk_tree_bill_items.get_children()[tree_idx]);tk_tree_bill_items.focus(A);tk_tree_bill_items.selection_set(A)
			get_item_total()
	if D==_L:
		if str(tk_root.focus_get())==J:
			if len(tk_tree_bill_items.get_children())>0:
				B=tk_tree_bill_items.item(A)[_B];E=tk_tree_bill_items.item(A)[K];print(str(B[1]));tk_tree_bill_items.delete(A);C=float(B[2])
				if C>1:C=C-1
				F=float(B[3]);G=F*C;B[2]=str(C);B[4]=str(G);tk_tree_bill_items.insert('',tree_idx,values=B,tags=E);A=tk_tree_bill_items.get_children()[tree_idx];print(tk_tree_bill_items.get_children()[tree_idx]);tk_tree_bill_items.focus(A);tk_tree_bill_items.selection_set(A)
			get_item_total()
def get_item_total():
	A=0;B=tk_tree_bill_items.get_children()
	for C in B:A+=float(tk_tree_bill_items.item(C)[_B][4])
	print('tot:',A);bind_bill_tot.set(str(A))
tk_root=ThemedTk(theme='radiance')
tk_root.title('Point Of Sale')
tree_idx=0
tree_row_prev=_A
bind_barcode=tk.StringVar()
bind_bill_tot=tk.StringVar()
item_name=tk.StringVar()
unit_price=tk.DoubleVar()
item_qty=tk.DoubleVar()
item_price=tk.DoubleVar()
tk_label_form=ttk.Label(tk_root,text='BILLING')
tk_label_form.pack(padx=0,pady=10)
tk_panwin=ttk.Panedwindow(tk_root)
tk_panwin.pack()
tk_frame_entry=ttk.Frame(tk_panwin,width=600,height=50)
tk_frame_list=ttk.Frame(tk_panwin,width=600,height=300)
tk_frame_summary=ttk.Frame(tk_panwin,width=600,height=50)
tk_panwin.add(tk_frame_entry,weight=1)
tk_panwin.add(tk_frame_list,weight=4)
tk_panwin.add(tk_frame_summary,weight=4)
tk_label_barcode=ttk.Label(tk_frame_entry,text='Barcode:')
tk_label_barcode.grid(column=1,row=1,sticky=tk.W)
bind_barcode.trace('w',lambda name,index,mode,bind_barcode=bind_barcode:event_bind_barcode(bind_barcode))
tk_entry_barcode=ttk.Entry(tk_frame_entry,textvariable=bind_barcode,font=_M,width=14)
tk_entry_barcode.grid(column=2,row=1,sticky=tk.W)
tk_entry_barcode.focus()
tree_columns=_C,_D,_E,_F,_G
tk_tree_bill_items=ttk.Treeview(tk_frame_list,columns=tree_columns,show='headings',selectmode='browse')
tk_tree_bill_items.grid(row=0,column=0,sticky='nsew')
tk_tree_bill_items.heading(_C,text='Item Code')
tk_tree_bill_items.heading(_D,text='Item Name')
tk_tree_bill_items.heading(_E,text='Quantity')
tk_tree_bill_items.heading(_F,text='Unit Price')
tk_tree_bill_items.heading(_G,text='Cost')
tk_tree_bill_items.column(_C,minwidth=0,width=100)
tk_tree_bill_items.column(_D,minwidth=0,width=500)
tk_tree_bill_items.column(_E,minwidth=0,width=60,anchor='e')
tk_tree_bill_items.column(_F,minwidth=0,width=150,anchor='e')
tk_tree_bill_items.column(_G,minwidth=0,width=150,anchor='e')
tk_scbar_bill_items=ttk.Scrollbar(tk_frame_list,orient=tk.VERTICAL,command=tk_tree_bill_items.yview)
tk_tree_bill_items.configure(yscroll=tk_scbar_bill_items.set)
tk_tree_bill_items.tag_configure(_H,background='bisque')
tk_scbar_bill_items.grid(row=0,column=1,sticky='ns')
tk_label_bill_tot=ttk.Label(tk_frame_summary,text='Bill Total:')
tk_label_bill_tot.grid(column=1,row=1,sticky=tk.W)
tk_entry_bill_tot=ttk.Entry(tk_frame_summary,textvariable=bind_bill_tot,font=_M,width=14,justify='right')
tk_entry_bill_tot.grid(column=2,row=1,sticky=tk.E)
tk_entry_bill_tot.config(state='disabled')
tk_tree_bill_items.bind('<<TreeviewSelect>>',event_treeListSelected)
tk_root.bind('<Left>',lambda event,arg=_L:event_keyClick(event,arg))
tk_root.bind('<Right>',lambda event,arg=_K:event_keyClick(event,arg))
tk_root.bind('<Up>',lambda event,arg='Up':event_keyClick(event,arg))
tk_root.bind('<Down>',lambda event,arg='Down':event_keyClick(event,arg))
tk_root.bind('<Tab>',lambda event,arg=_I:event_keyClick(event,arg))
tk_root.bind('<Delete>',lambda event,arg=_J:event_keyClick(event,arg))
db_conn=sqlite3.connect('POSLITE')
db_cur=db_conn.cursor()
tk_root.mainloop()