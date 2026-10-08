from abc import ABC, abstractmethod
import re

# 1. CLASSE ABSTRATA (MODELAGEM BASE)

class Conta(ABC):
    def __init__(self, titular, email, saldo_inicial=0.0):
        self.titular = titular
        self.email = email
        # O atributo com dois underlines ativa o name mangling para encapsulamento estrito
        self.__saldo = 0.0
        self.saldo = saldo_inicial # Dispara o setter para realizar a validacao

    @property
    def titular(self):
        return self._titular

    @titular.setter
    def titular(self, valor):
        if not valor or not valor.strip():
            raise ValueError("O nome do titular nao pode ser vazio.")
        self._titular = valor.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        padrao = r"^[\w.-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}$"
        if not re.match(padrao, valor.strip()):
            raise ValueError(f"O e-mail '{valor}' possui um formato invalido.")
        self._email = valor.strip()

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, valor):
        if valor < 0:
            raise ValueError("O saldo inicial nao pode ser negativo.")
        self.__saldo = float(valor)

    # Metodo abstrato que obriga as classes filhas a implementarem regras de saque
    @abstractmethod
    def sacar(self, valor):
        pass

    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("O valor do deposito deve ser maior que zero.")
        self.__saldo += float(valor)

    # Metodos dunder (Especiais) solicitados pelo exercicio
    def __str__(self):
        return f"Titular: {self.titular} | Saldo: R$ {self.saldo:.2f}"

    def __repr__(self):
        return f"{self.__class__.__name__}(titular='{self.titular}', email='{self.email}', saldo={self.saldo})"

    def __eq__(self, outra):
        if not isinstance(outra, Conta):
            return False
        return self.saldo == outra.saldo

    def __lt__(self, outra):
        if not isinstance(outra, Conta):
            return NotImplemented
        return self.saldo < outra.saldo

# 2. CLASSES FILHAS (HERANCA E POLIMORFISMO)

class ContaCorrente(Conta):
    def __init__(self, titular, email, saldo_inicial=0.0, limite_cheque_especial=0.0):
        # Chamada ao construtor da classe mae para reaproveitar as validacoes
        super().__init__(titular, email, saldo_inicial)
        self.limite_cheque_especial = limite_cheque_especial

    @property
    def limite_cheque_especial(self):
        return self._limite_cheque_especial

    @limite_cheque_especial.setter
    def limite_cheque_especial(self, valor):
        if valor < 0:
            raise ValueError("O limite do cheque especial nao pode ser negativo.")
        self._limite_cheque_especial = float(valor)

    # Sobrescrita de metodo (Polimorfismo) adaptada para as regras da conta corrente
    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("O valor do saque deve ser maior que zero.")
        if valor > (self.saldo + self.limite_cheque_especial):
            raise ValueError(f"Saldo e limite insuficientes para o saque de R$ {valor:.2f}.")
        
        # Como o saldo real e privado (__saldo), usamos uma operacao matematica via setter
        novo_saldo = self.saldo - valor
        # Permite saldo negativo controlado pelo limite do cheque especial
        self._Conta__saldo = novo_saldo 

    def __str__(self):
        return f"{super().__str__()} [Corrente | Limite: R$ {self.limite_cheque_especial:.2f}]"


class ContaPoupanca(Conta):
    def __init__(self, titular, email, saldo_inicial=0.0, taxa_rendimento=0.005):
        super().__init__(titular, email, saldo_inicial)
        self.taxa_rendimento = taxa_rendimento

    @property
    def taxa_rendimento(self):
        return self._taxa_rendimento

    @taxa_rendimento.setter
    def taxa_rendimento(self, valor):
        if valor < 0:
            raise ValueError("A taxa de rendimento nao pode ser negativa.")
        self._taxa_rendimento = float(valor)

    # Aplicacao de rendimento mensal exclusiva da poupanca
    def aplicar_rendimento(self):
        rendimento = self.saldo * self.taxa_rendimento
        self.depositar(rendimento)

    # Sobrescrita de metodo (Polimorfismo) adaptada para as regras da poupanca (nao permite saldo negativo)
    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("O valor do saque deve ser maior que zero.")
        if valor > self.saldo:
            raise ValueError(f"Saldo insuficiente na poupanca para o saque de R$ {valor:.2f}.")
        self.saldo -= valor

    def __str__(self):
        return f"{super().__str__()} [Poupanca | Rendimento: {self.taxa_rendimento * 100:.1f}%]"

# 3. CLASSE DE COMPOSICAO (COMPLEMENTAR)

class Banco:
    def __init__(self, nome):
        self.nome = nome
        self.contas = []

    def adicionar_conta(self, conta):
        if not isinstance(conta, Conta):
            raise TypeError("Apenas objetos derivados da classe Conta podem ser adicionados.")
        self.contas.append(conta)

    def __str__(self):
        return f"Banco: {self.nome} | Total de contas administradas: {len(self.contas)}"

# 4. AMBIENTE DE DEMONSTRACAO E TESTES

if __name__ == "__main__":
    meu_banco = Banco("Banco Central de Testes")
    
    print("--- 1. CRIANDO 10 INSTANCIAS DE OBJETOS ---")
    
    # Criacao manual de 10 instancias validas atendendo ao requisito do exercicio
    c1 = ContaCorrente("Ana Silva", "ana@email.com", 1500.0, 500.0)
    c2 = ContaCorrente("Bruno Souza", "bruno@email.com", 2500.0, 1000.0)
    c3 = ContaCorrente("Carlos Lima", "carlos@email.com", 100.0, 200.0)
    c4 = ContaCorrente("Daniela Reis", "daniela@email.com", 0.0, 100.0)
    c5 = ContaCorrente("Eduardo Costa", "eduardo@email.com", 8000.0, 5000.0)
    
    p1 = ContaPoupanca("Fernanda Alves", "fernanda@email.com", 10000.0, 0.006)
    p2 = ContaPoupanca("Gabriel Cruz", "gabriel@email.com", 500.0, 0.005)
    p3 = ContaPoupanca("Helena Dias", "helena@email.com", 12500.0, 0.007)
    p4 = ContaPoupanca("Igor Gomes", "igor@email.com", 300.0, 0.005)
    p5 = ContaPoupanca("Julia Martins", "julia@email.com", 450.0, 0.005)

    # Adicionando todas as instancias na lista do objeto Banco
    lista_contas = [c1, c2, c3, c4, c5, p1, p2, p3, p4, p5]
    for conta in lista_contas:
        meu_banco.adicionar_conta(conta)
        
    print(meu_banco)
    print("Instancias salvas com sucesso.")

    print("\n--- 2. DEMONSTRACAO DE POLIMORFISMO (SAQUE DE R$ 200 EM TODAS AS CONTAS) ---")
    # Iterando sobre objetos de classes distintas e chamando o mesmo metodo (sacar)
    for conta in meu_banco.contas:
        try:
            print(f"Estado original -> {conta}")
            conta.sacar(200.0)
            print(f"Apos saque R$ 200 -> {conta}")
            print("-" * 50)
        except ValueError as e:
            print(f"Nao foi possivel realizar o saque para {conta.titular}. Motivo: {e}")
            print("-" * 50)

    print("\n--- 3. TRATAMENTO DE EXCECOES (ENTRADAS INVALIDAS COM TRY/EXCEPT) ---")
    
    # Teste de validacao de E-mail
    try:
        print("Tentando criar conta com e-mail incorreto...")
        conta_erro = ContaCorrente("Marcos Viana", "marcos_email_sem_arroba.com", 500.0)
    except ValueError as e:
        print(f"[ERRO CAPTURADO]: {e}")

    # Teste de validacao de Saldo Negativo
    try:
        print("\nTentando criar conta com saldo negativo...")
        conta_erro2 = ContaPoupanca("Patricia Rosa", "patricia@email.com", -150.0)
    except ValueError as e:
        print(f"[ERRO CAPTURADO]: {e}")

    print("\n--- 4. INTEGRACAO COM METODOS ESPECIAIS (DUNDER) ---")
    # Teste dos metodos __lt__ (ordenacao por saldo) e __eq__ (comparacao de saldos)
    print(f"Conta da Ana Silva: R$ {c1.saldo:.2f}")
    print(f"Conta do Bruno Souza: R$ {c2.saldo:.2f}")
    print(f"Ana Silva tem menos saldo que Bruno Souza? {c1 < c2}")
    
    # Ordenando a lista completa com base no saldo por conta do metodo __lt__
    print("\nContas ordenadas por saldo crescente:")
    meu_banco.contas.sort()
    for conta in meu_banco.contas:
        print(f" * R$ {conta.saldo:<10.2f} | {conta.titular}")
