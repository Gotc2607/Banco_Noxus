import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk
from banco_de_dados2 import banco_de_dados2

class menu_interface(banco_de_dados2):
    
    def __init__(self):
        super().__init__("usuarios.db")  
        self.Criar_tabela()  
        self.janela = tk.Tk()
        self.janela.title("Menu Principal")
        self.janela.geometry('400x300')
        self.janela.resizable(False, False)
        self.tela_login() 

    
    def tela_principal(self, usuario, senha, saldo):
        
        self.limpar_tela()

        self.usuario_atual = usuario
        self.senha_atual = senha

        tk.Label(self.janela, text='Bem vindo a Noxus', font=('Arial',16),fg='red', bg='black').pack(pady=10)

        if saldo is not None:
            tk.Label(self.janela, text=(f'Saldo Atual: {saldo:.2f}'), font=('Arial', 14), fg='red', bg='black').pack(pady=10)
        else:
            tk.Label(self.janela, text='Erro ao carregar o saldo.', font=('Arial', 14),fg='red', bg='black').pack(pady=10)

        tk.Button(self.janela, text='Depositar', command=self.tela_deposito, fg='red', bg='gray').pack(pady=5) 

        tk.Button(self.janela, text='Sacar', command=self.tela_saque, fg='red', bg='gray').pack(pady=5)

        tk.Button(self.janela, text='Sair', command=self.finalizar_sessão, fg='red', bg='gray').pack(pady=5)

    def tela_login(self):
        
        self.limpar_tela()

        self.janela.configure(bg='black')

        self.janela.grid_columnconfigure(0, weight=1) 
        self.janela.grid_columnconfigure(1, weight=1)


        tk.Label(self.janela, text= 'Junte-se a Noxus', font=('Arial', 16), fg='red', bg='black').grid(row=0, column=0, columnspan=2, pady=5)

        
        tk.Label(self.janela, text='Usuario:', fg='red', bg='black').grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        self.nome_usuario = tk.Entry(self.janela, bg='grey')
        self.nome_usuario.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        
        tk.Label(self.janela, text='Senha:', fg='red', bg='black').grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        self.senha_usuario = tk.Entry(self.janela, show='*', bg='grey')
        self.senha_usuario.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        tk.Button(self.janela, text='Login', command=self.fazer_login, fg='red', bg='grey').grid(row=5, column=1,pady=3) 
        tk.Button(self.janela, text='Cadastrar', command= self.tela_novo_usuario,fg='red', bg='grey').grid(row=5, column=0,pady=3) 
        tk.Button(self.janela, text='Sair', command=self.finalizar, fg='red', bg='grey').grid(row=6, column=0, columnspan=2, pady=5)

    def fazer_login(self): 
    
        usuario = self.nome_usuario.get()
        senha = self.senha_usuario.get()

    
        if self.verificar_usuario(usuario, senha):
            messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {usuario}!")
            saldo = self.ver_saldo(senha)
            self.tela_principal(usuario, senha, saldo)  
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos!")

    def tela_novo_usuario(self):
        
        self.limpar_tela()

        tk.Label(self.janela, text='Cadastre-se aqui', font=('Arial', 16), fg='red', bg='black').pack(pady=10)

        tk.Label(self.janela, text='Nome de usuario:', fg='red', bg='black').pack(pady=10)
        self.nome_usuario = tk.Entry(self.janela,bg='gray')
        self.nome_usuario.pack(pady=10) 

        tk.Label(self.janela, text='Crie uma senha:', fg='red', bg='black').pack(pady=10)
        self.senha_usuario = tk.Entry(self.janela, show='*', bg='gray')
        self.senha_usuario.pack(pady=8)

        tk.Button(self.janela, text='Cadastrar', command=self.cadastrar_usuario, fg='red', bg='gray').pack(pady=10)        


    def cadastrar_usuario(self):
    
        Nusuario = self.nome_usuario.get()
        Nsenha = self.senha_usuario.get()

        if self.verificar_nome_usuari(Nusuario):
            messagebox.showerror('Erro',' Nome de usuario já existente')
        else:
            self.adicionar_usuarios(Nusuario, Nsenha)
            self.salvar()
            messagebox.showinfo('Sucesso','Usuario cadastrado com sucesso')
            self.tela_principal(Nusuario, Nsenha, 0.0)

    def tela_deposito(self):
        self.limpar_tela()

        tk.Label(self.janela, text='Valor do depósito:', font=('Arial', 16), fg='red', bg='black').pack(pady=10)
        valor_deposito = tk.Entry(self.janela, text='Valor', bg='gray')
        valor_deposito.pack(pady=5)

        def realizar_deposito():
            try:
                valor = float(valor_deposito.get())
                sucesso = self.depositar(self.senha_atual, valor)
                if sucesso:
                    messagebox.showinfo("Sucesso", f"Depósito de R${valor:.2f} realizado com sucesso!")
                    self.tela_principal(self.usuario_atual, self.senha_atual, self.ver_saldo(self.senha_atual))  
                else:
                    messagebox.showerror("Erro", "Falha ao realizar o depósito. Verifique os dados.")
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira um valor válido.")

        
        tk.Button(self.janela, text='Confirmar Depósito', command=realizar_deposito, fg='red', bg='gray').pack(pady=10)

        
        tk.Button(self.janela, text='Voltar', command=lambda: self.tela_principal(self.usuario_atual, self.senha_atual, self.ver_saldo(self.senha_atual)), fg='red', bg='gray').pack(pady=10)
    
    


    def tela_saque(self):
        self.limpar_tela()

        tk.Label(self.janela, text='Valor do saque:', font=('Arial', 16), fg='red', bg='black').pack(pady=10)
        valor_saque = tk.Entry(self.janela, text='Valor', bg='gray')
        valor_saque.pack(pady=5)

        def realizar_saque():
            try:
                valor = float(valor_saque.get())
                sucesso = self.sacar(self.senha_atual, valor)
                if sucesso:
                    messagebox.showinfo("Sucesso", f"Saque de R${valor:.2f} realizado com sucesso!")
                    self.tela_principal(self.usuario_atual, self.senha_atual, self.ver_saldo(self.senha_atual)) 
                else:
                    messagebox.showerror("Erro", "Falha ao realizar o saque. Verifique os dados.")
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira um valor válido.")

        
        tk.Button(self.janela, text='Confirmar Saque', command=realizar_saque, fg='red', bg='gray').pack(pady=10)

        
        tk.Button(self.janela, text='Voltar', command=lambda:self.tela_principal(self.usuario_atual, self.senha_atual, self.ver_saldo(self.senha_atual)), fg='red', bg='gray').pack(pady=10)

    def finalizar_sessão(self):
        self.limpar_tela()
        self.con.commit()
        self.tela_login()

    def finalizar(self):
        self.con.commit()
        self.con.close()
        self.janela.destroy()

    def limpar_tela(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
    

    
