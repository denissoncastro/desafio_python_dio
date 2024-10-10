import textwrap
from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class PessoaJuridica(Cliente):
    def __init__(self, nome_fantasia, cnpj, endereco):
        super().__init__(endereco)
        self.nome_fantasia = nome_fantasia
        self.cnpj = cnpj


class Conta(ABC):
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        elif valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False
        else:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

    @abstractmethod
    def __str__(self):
        pass


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_realizados = 0

    def sacar(self, valor):
        if self._saques_realizados >= self._limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False
        elif valor > self._limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False
        else:
            sucesso = super().sacar(valor)
            if sucesso:
                self._saques_realizados += 1
            return sucesso

    def __str__(self):
        return f"Agência: {self.agencia}\nC/C: {self.numero}\nTitular: {self.cliente.nome}"


class ContaPoupanca(Conta):
    def __init__(self, numero, cliente, taxa_rendimento=0.005):
        super().__init__(numero, cliente)
        self._taxa_rendimento = taxa_rendimento

    def calcular_rendimento(self, dias=30):
        rendimento = self._saldo * (1 + self._taxa_rendimento) ** dias - self._saldo
        self._saldo += rendimento
        print(f"\n=== Rendimento de R$ {rendimento:.2f} creditado na conta! ===")

    def __str__(self):
        return f"Agência: {self.agencia}\nC/P: {self.numero}\nTitular: {self.cliente.nome}"


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

def depositar(clientes):
    cpf = input("Informe o CPF/CNPJ do cliente: ")
    cliente = next((c for c in clientes if isinstance(c, PessoaFisica) and c.cpf == cpf or 
                    isinstance(c, PessoaJuridica) and c.cnpj == cpf), None)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    # Recuperar a primeira conta do cliente (pode ser modificado para escolher entre contas)
    conta = cliente.contas[0] if cliente.contas else None
    if conta:
        cliente.realizar_transacao(conta, transacao)
    else:
        print("\n@@@ Cliente não possui conta! @@@")

def exibir_extrato(clientes):
    cpf = input("Informe o CPF/CNPJ do cliente: ")
    cliente = next((c for c in clientes if isinstance(c, PessoaFisica) and c.cpf == cpf or 
                    isinstance(c, PessoaJuridica) and c.cnpj == cpf), None)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = cliente.contas[0] if cliente.contas else None
    if not conta:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(f"{transacao['tipo']}: R$ {transacao['valor']:.2f} - Data: {transacao['data']}")
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("==========================================")

def sacar(clientes):
    cpf = input("Informe o CPF/CNPJ do cliente: ")
    cliente = next((c for c in clientes if isinstance(c, PessoaFisica) and c.cpf == cpf or 
                    isinstance(c, PessoaJuridica) and c.cnpj == cpf), None)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = cliente.contas[0] if cliente.contas else None
    if not conta:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)


def menu():
    menu = """\n
    ================ MENU ================
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova conta
    [lc] Listar contas
    [npf] Novo cliente Pessoa Física
    [npj] Novo cliente Pessoa Jurídica
    [r] Calcular rendimento (Conta Poupança)
    [q] Sair
    => """
    return input(textwrap.dedent(menu))


def criar_cliente_pf(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = next((c for c in clientes if isinstance(c, PessoaFisica) and c.cpf == cpf), None)
    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
    clientes.append(cliente)
    print("\n=== Cliente Pessoa Física criado com sucesso! ===")


def criar_cliente_pj(clientes):
    cnpj = input("Informe o CNPJ (somente número): ")
    cliente = next((c for c in clientes if isinstance(c, PessoaJuridica) and c.cnpj == cnpj), None)
    if cliente:
        print("\n@@@ Já existe cliente com esse CNPJ! @@@")
        return

    nome_fantasia = input("Informe o nome fantasia: ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    cliente = PessoaJuridica(nome_fantasia, cnpj, endereco)
    clientes.append(cliente)
    print("\n=== Cliente Pessoa Jurídica criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF/CNPJ do cliente: ")
    cliente = next((c for c in clientes if isinstance(c, PessoaFisica) and c.cpf == cpf or 
                    isinstance(c, PessoaJuridica) and c.cnpj == cpf), None)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    tipo = input("Informe o tipo de conta (1: Corrente, 2: Poupança): ")
    if tipo == "1":
        conta = ContaCorrente.nova_conta(cliente, numero_conta)
    elif tipo == "2":
        conta = ContaPoupanca.nova_conta(cliente, numero_conta)
    else:
        print("\n@@@ Tipo de conta inválido! @@@")
        return

    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("\n=== Conta criada com sucesso! ===")


def calcular_rendimento(clientes):
    cpf = input("Informe o CPF/CNPJ do cliente: ")
    cliente = next((c for c in clientes if isinstance(c, PessoaFisica) and c.cpf == cpf or 
                    isinstance(c, PessoaJuridica) and c.cnpj == cpf), None)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = next((c for c in cliente.contas if isinstance(c, ContaPoupanca)), None)
    if not conta:
        print("\n@@@ O cliente não possui conta poupança! @@@")
        return

    dias = int(input("Informe o número de dias para calcular rendimento: "))
    conta.calcular_rendimento(dias)


def listar_contas(contas):
    for conta in contas:
        print("=" * 30)
        print(conta)


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "npf":
            criar_cliente_pf(clientes)
        elif opcao == "npj":
            criar_cliente_pj(clientes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "r":
            calcular_rendimento(clientes)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            break
        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


main()
