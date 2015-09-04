# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 21:31:58 2015

@author: GnacikM
"""

from Tkinter import *
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import webbrowser
import subprocess
from sympy.physics.quantum.operator import HermitianOperator, UnitaryOperator,  Operator, IdentityOperator
from sympy.physics.quantum.dagger import Dagger 



###############################################################################
""" Class of a Noncommutative Calculator """#################################
###############################################################################
class Application():

    def __init__(self, app):
        self.app = app
        app.title('Noncommutative calculator')
        app.geometry('800x600+200+200')
        app.wm_iconbitmap(bitmap = "latex.ico")
        app.resizable(0,0)
        self.Status = StringVar()
        self.Status.set(None)

    def add_button(self, your_text, your_width, your_command, your_pady, status= False, pos_x=0, pos_y=0):
        name = Button(self.app, text=your_text, width = your_width, command = your_command)
        name.pack(side='top', padx=15, pady=your_pady)
        if status==True:
            name.place(x=pos_x, y=pos_y)
        
    def add_text(self, value, your_text,  your_font, your_justify=CENTER, your_height = 2):
        name = StringVar(value)
        name.set(your_text)
        name_label = Label(self.app, textvariable = name, height=your_height, font=your_font, justify=your_justify)
        name_label.pack()
        
    def add_text_writable(self, your_label, your_font, pos_x, pos_y):
        name_label = Label(self.app, textvariable = your_label, height=2, font=your_font, bg="white")
        name_label.pack()
        name_label.place(x=pos_x, y=pos_y)
         
        
    def add_text_move(self, value, your_text,  your_font, pos_x, pos_y):
        name = StringVar(value)
        name.set(your_text)
        name_label = Label(self.app, textvariable = name, height=2, font=your_font)
        name_label.pack()
        name_label.place(x=pos_x, y=pos_y)
    
    def add_radio(self,your_text, your_value, status, your_status, pos_x, pos_y):
        name = Radiobutton(self.app, text=your_text, value = your_value, variable= status)
        name.pack()
        if your_status ==True:
            name.select()
        name.place(x=pos_x, y=pos_y)
    
    def add_line(self, x0, y0, x1, y1, your_height):
        name = Canvas(self.app, width=800, height=your_height)
        name.pack()
        name.create_line(x0, y0, x1, y1)
      
    def add_rectangle(self):
        name = Canvas(self.app, width=800, height=180)
        name.pack()
        name.create_rectangle(1,10,800,150, fill="white")
    
    def add_img(self,picture,  pos_x, pos_y):
        c = Canvas(self.app, width=800, height=2)
        c.background = PhotoImage(file=picture)
        panel = Label(self.app, image = c.background )
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        panel.place(x=pos_x, y=pos_y)
        
        
    def add_strap(self, colour, pos_x, pos_y):
        strap = Label( self.app, text="", bg=colour, fg="white", width=200)  
        strap.pack(pady=100)
        strap.place(x=pos_x, y=pos_y)
    
    def add_link(self, your_text, pos_x, pos_y, function):
        name = Label(self.app, text=your_text, fg="blue", cursor="hand2", font = "Verdana 7")
        name.pack()
        name.bind("<Button-1>",  function)
        name.place(x=pos_x, y=pos_y)
        
class entry(Application):
    
    def __init__(self):   
        self.app = Application.__init__(self,root)
        self.expression_init = Entry(self.app, textvariable=StringVar(None), width=0)

    def add_entry(self, pos_x, pos_y, entry, your_width,function, extra=0,  your_state=NORMAL ):
        scrollbar = Scrollbar(self.app, orient="horizontal")       
        expression = Entry(self.app,xscrollcommand=scrollbar.set, highlightcolor="blue", textvariable=entry, width=your_width , state= your_state, readonlybackground="white" )
        expression.focus()   
        
        expression.pack(side="bottom",fill="x")
        expression.place(x=pos_x, y=pos_y) 
        expression.bind('<Button-3>',function, add='')
        
        if your_width==70:
            scrollbar.pack(side=BOTTOM, fill="x", expand=True)
            scrollbar.config(command=expression.xview, activerelief=SUNKEN)
            scrollbar.place(x=pos_x+extra, y=pos_y) 
        self.expression_init = expression  
        
        
###############################################################################   
""" Methods used in this application """########################################
###############################################################################
  
""" changing text labels of mathematical expressions """     
def simplify_math(Status):
    answer1 = str(c_input.expression_init.get())
    
    labelText1.set(answer1)
    answer2 = latex(non_commutative_sympify(c_input.expression_init.get(),Status.get(),False))
    if '\dag' in answer2:
        answer2 = answer2.replace('\dag', '*')
    labelText2.set(str(answer2))
    answer3= str(non_commutative_sympify(c_input.expression_init.get(),Status.get(), True)) 
    if 'Dagger' in answer3:
        answer3 = answer3.replace('Dagger', 'Ad')
    labelText3.set(answer3) 
    answer4 = str(latex(non_commutative_sympify(c_input.expression_init.get(),Status.get(), True)))
    if '\dag' in answer4:
        answer4 = answer4.replace('\dag', '*')
    labelText4.set(answer4)
    fo = open("latex_code.txt", "a")
    fo.write('Your initial expression in LaTeX was: \n')
    fo.write(answer2+'\n \n')
    fo.write('Simplified epression in LaTeX is: \n')
    fo.write(answer4+'\n \n')
    fo.close()
    
""" noncommutative symplifying expressions, 
    please visit http://stackoverflow.com/questions/32157468/non-commutative-sympify-or-simplify """
    
def non_commutative_sympify(expr_string, status, boolean):
    if "^" in expr_string:
        expr_string = expr_string.replace("^", "**")
        
    if "Ad" in expr_string:
        expr_string = expr_string.replace("Ad", "Dagger")
        
    fixed_string=""
    if 'Dagger' in expr_string:
        fixed_string = expr_string.replace("Dagger", "sin")
    else:
        fixed_string = expr_string
    temp_evaluated_expr = parse_expr(
        fixed_string, 
        evaluate=False
    )
    if status =='0':
        status1= False
    elif status =='1':
        status1= True
        
    new_locals = {sym.name:Symbol(sym.name, commutative=status1)
                  for sym in temp_evaluated_expr.atoms(Symbol)}
      
    #new_locals = {}                
    #for sym in temp_evaluated_expr.atoms(Symbol):                 
     #       new_locals.update({sym.name:Operator(sym.name)})
      
    #{'C': C, 'E': E, 'I': I, 'N': N, 'O': O, 'Q': Q, 'S': S}
            
    new_locals.update({'U':UnitaryOperator('U')})
    new_locals.update({'W':UnitaryOperator('W')})
    new_locals.update({'V':UnitaryOperator('V')})
    new_locals.update({'u':UnitaryOperator('u')})
    new_locals.update({'w':UnitaryOperator('w')})
    new_locals.update({'v':UnitaryOperator('v')})
    new_locals.update({'H':HermitianOperator('H')})
    new_locals.update({'A':HermitianOperator('A')})
    new_locals.update({'C':Operator('C')})
    new_locals.update({'Dagger':Dagger})

    return sympify(expr_string, locals=new_locals, evaluate=boolean)
    

""" method that open latex_code.txt """
def openInstruction():
    subprocess.Popen("notepad latex_code.txt")
    
""" Erasing content of latex_code.txt """
def erase():
    fo = open("latex_code.txt", "w")
    fo.close()
    
""" Opening a link as an email and GitHub profile """
def callback1(event):
    webbrowser.open_new( r"mailto:michal@gnacik.eu")
    
def callback2(event):
    webbrowser.open_new( r"https://github.com/Nty24")
    
def rClicker(e):
    ''' right click context menu for all Tk Entry and Text widgets
    '''

    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')

        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')

        e.widget.focus()

        nclst=[
               (' Cut', lambda e=e: rClick_Cut(e)),
               (' Copy', lambda e=e: rClick_Copy(e)),
               (' Paste', lambda e=e: rClick_Paste(e)),
               ]

        rmenu = Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")

    except TclError:
        print ' - rClick menu, something wrong'
        pass

    return "break"
    
def rClicker_ro(e):
    ''' right click context menu for all Tk Entry and Text widgets
    '''

    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        e.widget.focus()

        nclst=[
               (' Copy', lambda e=e: rClick_Copy(e)),
               ]

        rmenu = Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")

    except TclError:
        print ' - rClick menu, something wrong'
        pass

    return "break"


def rClickbinder(r):

    try:
        for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
            r.bind_class(b, sequence='<Button-3>',
                         func=rClicker, add='')
    except TclError:
        print ' - rClickbinder, something wrong'
        pass       

###############################################################################       
""" Adding elements (e.g. buttons, links, text) to this applicatio """   ######
###############################################################################
if __name__ == '__main__':
    
    """defining our Tkinker root"""
    root = Tk()
    
    """ associating a root with our class"""
    calculator = Application(root)

    """adding text"""
    calculator.add_text( None,"Please enter a mathematical expression, we will try to simplify it for you.", "Verdana 10 bold")
    
    """ adding an entry where we put mathematical expressions"""
    #calculator.add_entry()
    c_input = entry()
    input_value = StringVar(None)
    c_input.add_entry(100,38, input_value,100, rClicker)
    
    """adding "Simplify" button"""
    calculator.add_button("Simplify", 20, lambda : simplify_math(calculator.Status), 25)
    
    """adding radio button"""
    calculator.add_radio("all variables are noncommutative (default)",  False, calculator.Status, True, 500, 60)
    calculator.add_radio("switch to commutative variables", True, calculator.Status,  False, 500, 80)
    
    """adding a line"""
 #   calculator.add_line(0,2,800,2,2)
    
    """adding an image"""
   # calculator.add_img("manual.gif", 30, 130)
    
    """adding text"""
    #calculator.add_text( None,"Any typed letter e.g. x, y, z etc. will be treated as a variable.\nIt is recommended not to use I, E or O for variables or symbol names. \nUse I for an imaginary unit, and E for Euler's number. \nPlease remember to place * symbol for multiplication of variables, i.e, we write x*y instead of xy.", "Veranda 9", LEFT, 4)
    calculator.add_text_move(None, "User's manual:",  "Verdana 9 bold", 20, 310)
    calculator.add_text_move(None, " Remember to use '*' as the multiplication, e.g. type 'A*B' not just 'AB'.",  "Verdana 9", 20, 340)
    calculator.add_text_move(None, " It is recommended not to use I, E, S, N, O, or Q for variables. All lowercase letters work for variables.",  "Verdana 9", 20, 370)
    calculator.add_text_move(None, " Please use '1' as the identity operator, 'E' as Euler's number, 'I' as imaginary unit.",  "Verdana 9", 20, 400)
    calculator.add_text_move(None, " To expand an expression in the brackets type 'expand', e.g. 'expand((A+B)^2)' returns 'A^2+AB+BA+B^2'." ,  "Verdana 9", 20, 430)
    calculator.add_text_move(None, " For the adjoint use Ad(), e.g. the adjoint of B is Ad(B)." ,  "Verdana 9", 20, 460)
    calculator.add_text_move(None, " Letters 'U', 'W', 'V', 'u', 'w', 'v' are reserved for unitary operators and 'H', 'A' for selfadjoint operators." ,  "Verdana 9", 20, 490)
    """adding a line and a rectangle"""    
  #  calculator.add_line(0,10,800,10,10)
    calculator.add_rectangle()
    
    """adding Text Labels and Entries for the displayed expressions"""
    label1 = StringVar()
    label1.set("Your expression: ")
    calculator.add_text_writable(label1, "Verdana 9", 50, 135)
    label2 = StringVar()
    label2.set("Your expression in LaTeX: ")
    calculator.add_text_writable(label2,  "Verdana 9", 50, 165)
    label3 = StringVar()
    label3.set("Simplified expression: ")
    calculator.add_text_writable(label3, "Verdana 9", 50, 195)
    label4 = StringVar()
    label4.set("Simplified expression in LaTeX: ")
    calculator.add_text_writable(label4, "Verdana 9", 50, 225)
    
    labelText1_entry = entry()
    labelText1 = StringVar(None)
    labelText1_entry.add_entry(250, 142, labelText1,70, rClicker_ro,425,  "readonly")
    labelText2_entry = entry()
    labelText2 = StringVar(None)
    labelText2_entry.add_entry(250, 172, labelText2,70, rClicker_ro,425, "readonly")
    labelText3_entry = entry()
    labelText3 = StringVar(None)
    labelText3_entry.add_entry(250, 202, labelText3,70, rClicker_ro,425, "readonly")
    labelText4_entry = entry()
    labelText4 = StringVar(None)
    labelText4_entry.add_entry(250, 232, labelText4,70, rClicker_ro,425,"readonly")
    
    """adding a line"""
   # calculator.add_line(0,2,800,2,2)
    
    """adding buttons"""
    calculator.add_button("Click to open 'latex_code.txt' for the LaTeX code", 40, openInstruction, 5, True, 50, 280)
    calculator.add_button("Erase the content of 'latex_code.txt", 40, erase, 5, True, 400, 280)
    
    """adding text"""
    calculator.add_text_move( None,"Copyright © 2015 Michał Gnacik.", "Verdana 7", 20, 550)
    
    """ adding a navy strap"""
    calculator.add_strap("navy", 0, 530)
    
    """adding a link to the email"""
    calculator.add_link("Click to contact me.", 195, 556, callback1)
    calculator.add_link("Click to view my GitHub profile.", 300, 556, callback2)
    
    """initializing the app"""
    root.mainloop()


