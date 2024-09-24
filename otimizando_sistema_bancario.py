def menu():
    print("=== Bem-vindo ao Banco Python! ===")
    print("1. Depositar")
    print("2. Sacar")
    print("3. Exibir Extrato")
    print("4. Criar Usuário")
    print("5. Filtrar Usuário")
    print("6. Criar Conta")
    print("7. Listar Contas")
    print("0. Sair")
    return int(input("Digite a opção desejada: "))

def depositar(saldo, valor, extrato):
    saldo += valor
    extrato.append(f"Depósito: R$ {valor:.2f}")
    return saldo

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("Saldo insuficiente.")
        return saldo
    if valor > limite:
        print("Valor acima do limite para saque.")
        return saldo
    if numero_saques >= limite_saques:
        print("Limite de saques excedido.")
        return saldo
    saldo -= valor
    extrato.append(f"Saque: R$ {valor:.2f}")
    numero_saques += 1
    return saldo

def exibir_extrato(saldo, /, *, extrato):
    print("\n=== Extrato Bancário ===")
    for transacao in extrato:
        print(transacao)
    print(f"Saldo: R$ {saldo:.2f}")

def criar_usuario(usuarios):
    nome = input("Digite o nome do usuário: ")
    cpf = input("Digite o CPF do usuário: ")
    novo_usuario = {'nome': nome, 'cpf': cpf, 'contas': []}
    usuarios.append(novo_usuario)
    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            return usuario
    return None

def criar_conta(agencia, numero_conta, usuarios):
    usuario = filtrar_usuario(input("Digite o CPF do usuário: "), usuarios)
    if usuario:
        nova_conta = {'agencia': agencia, 'numero_conta': numero_conta, 'saldo': 0, 'extrato': []}
        usuario['contas'].append(nova_conta)
        print("Conta criada com sucesso!")
    else:
        print("Usuário não encontrado.")

def listar_contas(contas):
    for usuario in usuario:
        for conta in usuario['contas']:
            print(f"Agência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}")

def main():
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 0:
            break

        elif opcao == 1:
            cpf = input("Digite o CPF do usuário: ")
            usuario = filtrar_usuario(cpf, usuarios)

            if usuario:
                conta_selecionada = selecionar_conta(usuario)  # Função para selecionar a conta
                if conta_selecionada:
                    valor = float(input("Digite o valor a ser depositado: "))
                    conta_selecionada['saldo'] = depositar(conta_selecionada['saldo'], valor, conta_selecionada['extrato'])
                    print("Depósito realizado com sucesso!")
                else:
                    print("Usuário não possui contas.")
            else:
                print("Usuário não encontrado.")

        elif opcao == 2:
            cpf = input("Digite o CPF do usuário: ")
            usuario = filtrar_usuario(cpf, usuarios)

            if usuario:
                conta_selecionada = selecionar_conta(usuario)
                if conta_selecionada:
                    valor = float(input("Digite o valor a ser sacado: "))
                # Validações
                if valor > conta_selecionada['saldo']:
                    print("Saldo insuficiente.")
                elif valor > limite:
                    print("Valor acima do limite para saque.")
                elif numero_saques >= limite_saques:
                    print("Limite de saques excedido.")
                else:
                    # Atualização de dados
                    conta_selecionada['saldo'] = sacar(conta_selecionada['saldo'], valor, conta_selecionada['extrato'], limite, numero_saques, limite_saques)
                    print("Saque realizado com sucesso!")
            else:
                print("Usuário não possui contas.")
        else:
            print("Usuário não encontrado.")
            pass
        # Função para selecionar a conta do usuário
        def selecionar_conta(usuario):
            if len(usuario['contas']) == 1:
                return usuario['contas'][0]
            else:
                print("O usuário possui mais de uma conta. Selecione uma:")
                for i, conta in enumerate(usuario['contas']):
                    print(f"{i+1}. Agência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}")
                opcao_conta = int(input("Digite o número da conta: ")) - 1
                if 0 <= opcao_conta < len(usuario['contas']):
                    return usuario['contas'][opcao_conta]
                else:
                    return None

if __name__ == "__main__":
   main()
