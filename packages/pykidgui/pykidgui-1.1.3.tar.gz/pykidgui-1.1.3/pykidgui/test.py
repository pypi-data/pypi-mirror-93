import pykidgui as pk


print(pk)
'''
print(pk.version)
pk.text_title= "Loja"
pk.window_geometry = "550x550"
pk.window_name("home")

pk.add_build_map("checkbox")
pk.new_checkbox("check1")

pk.add_build_map("checkbox:LEFT")
pk.new_checkbox("check2")
pk.add_build_map("checkbox:left")
pk.new_checkbox("check clique3")



pk.add_build_map("label")
pk.new_label("Loja teste")

pk.add_build_map("on_click")
pk.new_on_click_text = "cadastar produtos"
pk.new_on_click_var=te.j

pk.add_build_map("label")



pk.add_build_map("button")
pk.new_button("sair")



print(pk.build_map)
pk.star()
'''

"""
#on click def

def login():
     
     pk.new_label("button 1")
     pk.add_build_map("label")
     
def k():
    x = 500
    y = 500
    result = x+y
    try:
       pk.Label(text =result).pack()
    except:
        pk.new_message_title("Erro","Erro de script")


def x():
     pk.new_label("button 1")
     pk.add_build_map("label")
     pk.window_name("test")
     pk.gui()

     
pk.new_label("button 1")
pk.add_build_map("label")

pk.new_click_text("message teste") 
pk.new_on_click(login)
pk.add_build_map("on_click")


pk.new_label("button 2")
pk.add_build_map("label")


pk.new_click_text("Resultado") 
pk.new_on_click(x)
pk.add_build_map("on_click")
"""

"""
pk.text_title="Loja"
pk.window_geometry="200x200"

pk.Label(text ="test").pack()
pk.Button(text="Erro",command =pk.new_message_erro).pack()
pk.Label(text ="play").pack()
pk.Button(text="play",command =x).pack()
#canvas

C = pk.Canvas(bg ="yellow", 
           height = 250, width = 300) 
  
line = C.create_line(108, 120,  
                     320, 40,  
                     fill ="green") 
  
arc = C.create_arc(180, 150, 80,  
                   210, start = 0, 
                   extent = 220,  
                   fill ="red") 
  
oval = C.create_oval(80, 30, 140,  
                     150,  
                     fill ="blue") 
  
C.pack()
"""
"""
def pri():
     user = e1.get()
     webbrowser.open(str(user), new=0, autoraise=True)
     print(user)

import webbrowser

e1 = pk.Entry()
x1 = pk.Label(text ="link do site:")
e1.grid(row=0, column=2)
x1.grid(row=0,column=1)
btn = pk.Button(text="Pesquisar",command =pri)
btn.grid(row=2,column=1)
"""
def perfil():
      pk.messagebox.showinfo("Perfil", "Logado com sucesso!")

def user():
     user = pk.entry[0].get()
     senha = pk.entry[1].get()
     if user == "ronan" and senha == "123":
          perfil()
     else:
          pk.messagebox.showwarning("Erro de Login", "Senha ou Usuario não esta correto!")    

pk.new_label("Usuario")
pk.add_build_map("label")

pk.new_entry("1")
pk.add_build_map("entry")

pk.new_label("Senha")
pk.add_build_map("label")

pk.new_entry("2")
pk.add_build_map("entry")

pk.new_label("")
pk.add_build_map("label")

pk.new_click_text("login") 
pk.new_on_click(user)
pk.add_build_map("on_click")



pk.text_title="Login"
pk.window_geometry="200x200"

pk.gui()

