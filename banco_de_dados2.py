import sqlite3

class banco_de_dados2:

    def __init__(self, db_name):
        self.db_name = db_name
        self.con = sqlite3.connect(self.db_name)
        self.cursor = self.con.cursor()

    def Criar_tabela(self):
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS banco_de_dados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            senha TEXT NOT NULL,
            saldo REAl DEFAULT 0
        );
        ''')
        #verificar se já existe esse nome de usuario
    def verificar_nome_usuari(self, usuario):
        self.cursor.execute("SELECT * FROM banco_de_dados WHERE usuario = ?", (usuario,))
        resultado = self.cursor.fetchone()
        if resultado:
            return True
        else:
            return False
       
        #verificar se a senha e o nome de usuario então certos
    def verificar_usuario(self, usuario, senha):
        self.cursor.execute("SELECT * FROM banco_de_dados WHERE usuario = ? AND senha = ?", (usuario, senha))
        resultado = self.cursor.fetchone()
        if resultado:
            return True
        else:
            return False

    def adicionar_usuarios(self, usuario, senha):
        self.cursor.execute(''' INSERT INTO banco_de_dados (usuario,senha, saldo) VALUES (?, ?, ?)''', (usuario, senha, 0.0))
        print('Usuario adicionado com sucesso')

    def depositar(self, senha, valor):
        try:
            # Consulta o saldo pelo campo senha
            self.cursor.execute('SELECT saldo FROM banco_de_dados WHERE senha = ?', (senha,))
            saldo_atual = self.cursor.fetchone()
            saldo_atual = saldo_atual[0]

        # Verifica se a senha é válida
            if saldo_atual is None:
                return False

        # Valida o valor do depósito
            if not isinstance(valor, (int, float)) or valor <= 0:
                return False

        # Calcula o novo saldo e atualiza no banco
            saldo_novo = saldo_atual + valor
            self.cursor.execute('UPDATE banco_de_dados SET saldo = ? WHERE senha = ?', (saldo_novo, senha))

        # Exibe o saldo atualizado e retorna sucesso
            return True

        except sqlite3.Error as e:
        # Trata erros de banco de dados
            return False
            
    def sacar(self, senha, valor):
        try:
            # Consulta o saldo pelo campo senha
            self.cursor.execute('SELECT saldo FROM banco_de_dados WHERE senha = ?', (senha,))
            saldo_atual = self.cursor.fetchone()

        # Verifica se a senha é válida
            if saldo_atual is None:
                return False

        # Extrai o saldo atual
            saldo_atual = saldo_atual[0]  # Extrai o valor numérico da tupla

        # Valida o valor do saque
            if not isinstance(valor, (int, float)) or valor > saldo_atual:
                return False

        # Calcula o novo saldo e atualiza no banco
            saldo_novo = saldo_atual - valor
            self.cursor.execute('UPDATE banco_de_dados SET saldo = ? WHERE senha = ?', (saldo_novo, senha))

        # Exibe o saldo atualizado e retorna sucesso
            return True

        except sqlite3.Error as e:
        # Trata erros de banco de dados
            return False

    def ver_saldo(self, senha):
        self.cursor.execute('SELECT saldo FROM banco_de_dados WHERE senha = ?', (senha,))
        resultado = self.cursor.fetchone()

        if resultado is not None:
            saldo = resultado[0]
            return saldo
        else:
            return None


    def salvar(self):

       if self.con:
        self.con.commit()
