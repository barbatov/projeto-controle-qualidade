# Constantes de Qualidade e Limites de Embalagem
CAPACIDADE_CAIXA = 10
PESO_MIN, PESO_MAX = 95.0, 105.0
COMPRIMENTO_MIN, COMPRIMENTO_MAX = 10.0, 20.0
CORES_PERMITIDAS = {"azul", "verde"}


def validar_peca(peso: float, cor: str, comprimento: float) -> list:
    """
    Avalia se a peça cumpre os requisitos técnicos de qualidade estabelecidos.

    Parâmetros:
        peso (float): Massa da peça em gramas.
        cor (str): Tonalidade da peça.
        comprimento (float): Extensão dimensional em centímetros.

    Retorno:
        list: Lista com as descrições dos critérios violados (vazia se aprovada).
    """
    motivos = []
    cor_normalizada = cor.strip().lower()

    if not (PESO_MIN <= peso <= PESO_MAX):
        motivos.append(f"Peso fora do intervalo ({peso}g | esperado: 95g a 105g)")

    if cor_normalizada not in CORES_PERMITIDAS:
        motivos.append(f"Cor não autorizada ('{cor}' | esperado: azul ou verde)")

    if not (COMPRIMENTO_MIN <= comprimento <= COMPRIMENTO_MAX):
        motivos.append(f"Comprimento fora do intervalo ({comprimento}cm | esperado: 10cm a 20cm)")

    return motivos


def reconstruir_caixas(pecas_aprovadas: list) -> list:
    """
    Reorganiza a distribuição das peças aprovadas nas caixas de 10 unidades.

    Garante a integridade do empacotamento após inclusões ou remoções de peças.

    Parâmetros:
        pecas_aprovadas (list): Lista de dicionários contendo os dados das peças aprovadas.

    Retorno:
        list: Lista de listas, onde cada sublita representa uma caixa com até 10 itens.
    """
    if not pecas_aprovadas:
        return []

    caixas = []
    for i in range(0, len(pecas_aprovadas), CAPACIDADE_CAIXA):
        lote = [p["id"] for p in pecas_aprovadas[i:i + CAPACIDADE_CAIXA]]
        caixas.append(lote)

    return caixas


def cadastrar_peca(pecas_aprovadas: list, pecas_reprovadas: list):
    """
    Solicita os dados técnicos de uma peça ao utilizador, avalia os critérios
    de qualidade e armazena o registo na categoria correspondente.

    Parâmetros:
        pecas_aprovadas (list): Registo acumulado de peças aprovadas.
        pecas_reprovadas (list): Registo acumulado de peças rejeitadas.
    """
    print("\n--- 1. CADASTRAR NOVA PEÇA ---")
    id_peca = input("ID da peça: ").strip()

    # Validação de unicidade do ID
    ids_existentes = [p["id"] for p in pecas_aprovadas] + [p["id"] for p in pecas_reprovadas]
    if id_peca in ids_existentes:
        print(f"\n[ERRO] O ID '{id_peca}' já se encontra registado no sistema.")
        return

    try:
        peso = float(input("Peso (g): ").replace(",", "."))
        cor = input("Cor (azul/verde): ").strip()
        comprimento = float(input("Comprimento (cm): ").replace(",", "."))
    except ValueError:
        print("\n[ERRO] Peso e comprimento têm de ser números válidos.")
        return

    falhas = validar_peca(peso, cor, comprimento)
    dados = {
        "id": id_peca,
        "peso": peso,
        "cor": cor,
        "comprimento": comprimento
    }

    if not falhas:
        pecas_aprovadas.append(dados)
        print(f"\n✔ Peça '{id_peca}' APROVADA com sucesso!")
    else:
        dados["motivos"] = falhas
        pecas_reprovadas.append(dados)
        print(f"\n✖ Peça '{id_peca}' REPROVADA:")
        for falha in falhas:
            print(f"   - {falha}")


def listar_pecas(pecas_aprovadas: list, pecas_reprovadas: list):
    """
    Apresenta a listagem completa e discriminada de todas as peças inspecionadas,
    detalhando os motivos de rejeição para as não conformes.

    Parâmetros:
        pecas_aprovadas (list): Lista de peças aprovadas.
        pecas_reprovadas (list): Lista de peças reprovadas.
    """
    print("\n--- 2. LISTAGEM DE PEÇAS APROVADAS / REPROVADAS ---")

    print("\n[PEÇAS APROVADAS]")
    if not pecas_aprovadas:
        print("  Nenhuma peça aprovada registada.")
    else:
        for p in pecas_aprovadas:
            print(f"  • ID: {p['id']:<10} | Peso: {p['peso']}g | Cor: {p['cor']} | Comprimento: {p['comprimento']}cm")

    print("\n[PEÇAS REPROVADAS]")
    if not pecas_reprovadas:
        print("  Nenhuma peça reprovada registada.")
    else:
        for p in pecas_reprovadas:
            print(f"  • ID: {p['id']:<10} | Peso: {p['peso']}g | Cor: {p['cor']} | Comprimento: {p['comprimento']}cm")
            for m in p["motivos"]:
                print(f"      ↳ {m}")


def remover_peca(pecas_aprovadas: list, pecas_reprovadas: list):
    """
    Remove uma peça do sistema através do seu ID e atualiza os registos.

    Parâmetros:
        pecas_aprovadas (list): Lista de peças aprovadas.
        pecas_reprovadas (list): Lista de peças reprovadas.
    """
    print("\n--- 3. REMOVER PEÇA CADASTRADA ---")
    id_busca = input("Introduza o ID da peça a remover: ").strip()

    # Procura nas aprovadas
    for idx, p in enumerate(pecas_aprovadas):
        if p["id"] == id_busca:
            pecas_aprovadas.pop(idx)
            print(f"\n✔ Peça '{id_busca}' (Aprovada) removida com sucesso. As caixas foram reorganizadas.")
            return

    # Procura nas reprovadas
    for idx, p in enumerate(pecas_reprovadas):
        if p["id"] == id_busca:
            pecas_reprovadas.pop(idx)
            print(f"\n✔ Peça '{id_busca}' (Reprovada) removida do registo de refugo.")
            return

    print(f"\n[AVISO] A peça com ID '{id_busca}' não foi encontrada.")


def listar_caixas_fechadas(pecas_aprovadas: list):
    """
    Identifica e lista apenas as caixas que atingiram a capacidade máxima de 10 peças.

    Parâmetros:
        pecas_aprovadas (list): Lista de peças aprovadas.
    """
    print("\n--- 4. LISTAGEM DE CAIXAS FECHADAS ---")
    caixas = reconstruir_caixas(pecas_aprovadas)
    caixas_fechadas = [c for c in caixas if len(c) == CAPACIDADE_CAIXA]

    if not caixas_fechadas:
        print("Nenhuma caixa atingiu o limite de fecho (10 peças).")
    else:
        print(f"Total de caixas fechadas: {len(caixas_fechadas)}\n")
        for idx, caixa in enumerate(caixas_fechadas, 1):
            print(f"  • Caixa {idx:02d} [FECHADA] - 10/10 peças:")
            print(f"    Itens: {', '.join(caixa)}")


def gerar_relatorio_final(pecas_aprovadas: list, pecas_reprovadas: list):
    """
    Gera e imprime o relatório executivo consolidado com totais, distribuição
    de caixas (fechadas e em curso) e o detalhamento de todos os motivos de reprovação.

    Parâmetros:
        pecas_aprovadas (list): Lista de peças aprovadas.
        pecas_reprovadas (list): Lista de peças reprovadas.
    """
    caixas = reconstruir_caixas(pecas_aprovadas)
    total_aprovadas = len(pecas_aprovadas)
    total_reprovadas = len(pecas_reprovadas)
    total_geral = total_aprovadas + total_reprovadas

    print("\n" + "=" * 65)
    print("                 RELATÓRIO CONSOLIDADO DE PRODUÇÃO")
    print("=" * 65)
    print(f"Total de peças inspecionadas : {total_geral}")
    print(f"Total de peças aprovadas     : {total_aprovadas}")
    print(f"Total de peças reprovadas    : {total_reprovadas}")
    print(f"Quantidade total de caixas   : {len(caixas)}")
    print("-" * 65)

    print("STATUS DE ARMAZENAMENTO DAS CAIXAS:")
    if not caixas:
        print("  Nenhuma caixa em uso.")
    else:
        for idx, caixa in enumerate(caixas, 1):
            status = "FECHADA" if len(caixa) == CAPACIDADE_CAIXA else "EM ANDAMENTO"
            print(f"  • Caixa {idx:02d}: {len(caixa):02d}/{CAPACIDADE_CAIXA} peças [{status}]")
            print(f"    Conteúdo: {', '.join(caixa)}")

    print("-" * 65)
    print("DETALHAMENTO DOS MOTIVOS DE REPROVAÇÃO:")
    if not pecas_reprovadas:
        print("  Nenhuma não conformidade registada.")
    else:
        for p in pecas_reprovadas:
            print(f"  • Peça ID: {p['id']}")
            for motivo in p["motivos"]:
                print(f"    - {motivo}")

    print("=" * 65)


def menu_interativo():
    """
    Gere o ciclo principal da interface de linha de comandos (CLI),
    encaminhando as opções do operador para as respetivas funções do sistema.
    """
    pecas_aprovadas = []
    pecas_reprovadas = []

    while True:
        print("\n" + "=" * 45)
        print("     SISTEMA INDUSTRIAL DE CONTROLO DE QUALIDADE")
        print("=" * 45)
        print("1. Cadastrar nova peça")
        print("2. Listar peças aprovadas/reprovadas")
        print("3. Remover peça cadastrada")
        print("4. Listar caixas fechadas")
        print("5. Gerar relatório final")
        print("0. Sair")

        opcao = input("\nSelecione uma opção (0-5): ").strip()

        if opcao == "1":
            cadastrar_peca(pecas_aprovadas, pecas_reprovadas)
        elif opcao == "2":
            listar_pecas(pecas_aprovadas, pecas_reprovadas)
        elif opcao == "3":
            remover_peca(pecas_aprovadas, pecas_reprovadas)
        elif opcao == "4":
            listar_caixas_fechadas(pecas_aprovadas)
        elif opcao == "5":
            gerar_relatorio_final(pecas_aprovadas, pecas_reprovadas)
        elif opcao == "0":
            print("\nA encerrar o sistema de automação...")
            gerar_relatorio_final(pecas_aprovadas, pecas_reprovadas)
            break
        else:
            print("\n[ERRO] Opção inválida. Por favor escolha um número de 0 a 5.")


if __name__ == "__main__":
    menu_interativo()