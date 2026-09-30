# Sistema de Controle de Qualidade e Gestão de Peças

Solução desenvolvida em **Python 3** para automação de triagem, inspeção dimensional/massa/cor e empacotamento em linha de produção industrial.

---

## 📌 Sumário
1. [Sobre o Projeto](#-sobre-o-projeto)
2. [Critérios de Qualidade e Regras de Negócio](#-critérios-de-qualidade-e-regras-de-negócio)
3. [Estrutura do Código e Funcionamento](#-estrutura-do-código-e-funcionamento)
4. [Como Rodar o Programa](#-como-rodar-o-programa)
5. [Menu Interativo](#-menu-interativo)
6. [Exemplos Práticos de Entrada e Saída](#-exemplos-práticos-de-entrada-e-saída)

---

## 🏭 Sobre o Projeto

O projeto substitui inspeções manuais por triagem algorítmica automatizada, reduzindo gargalos operacionais e eliminando erros humanos na conferência de peças manufaturadas. O sistema processa os atributos físicos de cada unidade, decide sua aprovação ou refugo e realiza o empacotamento dinâmico em caixas de capacidade limitada.

---

## 📏 Critérios de Qualidade e Regras de Negócio

Para que uma peça seja **Aprovada**, ela deve satisfazer cumulativamente:

| Parâmetro | Faixa / Valor Permitido | Comportamento em Não Conformidade |
| :--- | :--- | :--- |
| **Peso** | Entre `95.0g` e `105.0g` | Rejeição com registro da massa fora da faixa |
| **Cor** | `azul` ou `verde` (insensível a maiúsculas/espaços) | Rejeição por tonalidade não homologada |
| **Comprimento** | Entre `10.0cm` e `20.0cm` | Rejeição por desvio dimensional |

### Regras de Armazenamento
- Cada caixa comporta até **10 peças aprovadas**.
- Ao atingir a capacidade máxima (10 itens), a caixa é considerada **FECHADA** e uma nova é aberta dinamicamente.
- Peças reprovadas **não** entram nas caixas e são direcionadas ao registro de refugo com todos os motivos de falha associados.
- Caso uma peça seja removida, a distribuição das caixas é recalculada em tempo real para manter a consistência física.

---

## ⚙️ Estrutura do Código e Funcionamento

O sistema adota o paradigma estruturado/funcional, sem a complexidade de classes, garantindo alta legibilidade e manutenibilidade:

- `validar_peca(...)`: Executa a conferência técnica dos 3 parâmetros e retorna a lista de falhas.
- `reconstruir_caixas(...)`: Agrupa as peças aprovadas em lotes de até 10 unidades.
- `cadastrar_peca(...)`: Entrada de dados, validação de duplicidade de ID e triagem.
- `listar_pecas(...)`: Exibe o inventário detalhado de peças conformes e refugos.
- `remover_peca(...)`: Remove registros pelo identificador e reorganiza as caixas.
- `listar_caixas_fechadas(...)`: Filtra e apresenta exclusivamente os lotes que completaram 10 peças.
- `gerar_relatorio_final(...)`: Emite o balanço consolidado de produção e refugo.
- `menu_interativo(...)`: Interface de linha de comando (CLI) em loop infinito com menu de opções.

---

## 🚀 Como Rodar o Programa

### Pré-requisitos
- **Python 3.8** ou superior instalado no computador.
- Não é necessária a instalação de nenhuma biblioteca externa (o sistema utiliza apenas a biblioteca padrão do Python).

### Passo a Passo

1. **Baixar ou clonar o projeto:**
   Salve o arquivo do código como `main.py` na pasta de sua preferência.

2. **Abrir o Terminal ou Prompt de Comando:**
   Navegue até o diretório onde o arquivo `main.py` foi salvo:
   ```bash
   cd /caminho/para/a/pasta
   ```

3. **Verificar a versão do Python:**
   ```bash
   python --version
   # ou
   python3 --version
   ```

4. **Executar a aplicação:**
   ```bash
   python main.py
   # ou no Linux/macOS:
   python3 main.py
   ```

---

## 🖥️ Menu Interativo

Ao iniciar, o terminal exibirá a interface de controle:

```text
=============================================
     SISTEMA INDUSTRIAL DE CONTROLO DE QUALIDADE
=============================================
1. Cadastrar nova peça
2. Listar peças aprovadas/reprovadas
3. Remover peça cadastrada
4. Listar caixas fechadas
5. Gerar relatório final
0. Sair

Selecione uma opção (0-5):
```

---

## 📋 Exemplos Práticos de Entrada e Saída

### Exemplo 1: Cadastrando uma Peça Aprovada (Opção 1)
**Entrada do operador:**
```text
Selecione uma opção (0-5): 1

--- 1. CADASTRAR NOVA PEÇA ---
ID da peça: P-101
Peso (g): 100.5
Cor (azul/verde): azul
Comprimento (cm): 15.2
```
**Saída do sistema:**
```text
✔ Peça 'P-101' APROVADA com sucesso!
```

---

### Exemplo 2: Cadastrando uma Peça com Múltiplas Não Conformidades (Opção 1)
**Entrada do operador:**
```text
Selecione uma opção (0-5): 1

--- 1. CADASTRAR NOVA PEÇA ---
ID da peça: P-102
Peso (g): 92.0
Cor (azul/verde): amarelo
Comprimento (cm): 25.0
```
**Saída do sistema:**
```text
✖ Peça 'P-102' REPROVADA:
   - Peso fora do intervalo (92.0g | esperado: 95g a 105g)
   - Cor não autorizada ('amarelo' | esperado: azul ou verde)
   - Comprimento fora do intervalo (25.0cm | esperado: 10cm a 20cm)
```

---

### Exemplo 3: Listagem de Peças (Opção 2)
**Entrada:** `2`  
**Saída gerada:**
```text
--- 2. LISTAGEM DE PEÇAS APROVADAS / REPROVADAS ---

[PEÇAS APROVADAS]
  • ID: P-101      | Peso: 100.5g | Cor: azul | Comprimento: 15.2cm

[PEÇAS REPROVADAS]
  • ID: P-102      | Peso: 92.0g | Cor: amarelo | Comprimento: 25.0cm
      ↳ Peso fora do intervalo (92.0g | esperado: 95g a 105g)
      ↳ Cor não autorizada ('amarelo' | esperado: azul ou verde)
      ↳ Comprimento fora do intervalo (25.0cm | esperado: 10cm a 20cm)
```

---

### Exemplo 4: Listagem de Caixas Fechadas (Opção 4)
*Cenário com 12 peças aprovadas cadastradas (uma caixa fechada e uma em andamento):*  
**Entrada:** `4`  
**Saída gerada:**
```text
--- 4. LISTAGEM DE CAIXAS FECHADAS ---
Total de caixas fechadas: 1

  • Caixa 01 [FECHADA] - 10/10 peças:
    Itens: P-01, P-02, P-03, P-04, P-05, P-06, P-07, P-08, P-09, P-10
```

---

### Exemplo 5: Remoção de Peça (Opção 3)
**Entrada do operador:**
```text
Selecione uma opção (0-5): 3

--- 3. REMOVER PEÇA CADASTRADA ---
Introduza o ID da peça a remover: P-101
```
**Saída do sistema:**
```text
✔ Peça 'P-101' (Aprovada) removida com sucesso. As caixas foram reorganizadas.
```

---

### Exemplo 6: Relatório Consolidado de Produção (Opção 5)
**Entrada:** `5`  
**Saída gerada:**
```text
=================================================================
                 RELATÓRIO CONSOLIDADO DE PRODUÇÃO
=================================================================
Total de peças inspecionadas : 12
Total de peças aprovadas     : 11
Total de peças reprovadas    : 1
Quantidade total de caixas   : 2
-----------------------------------------------------------------
STATUS DE ARMAZENAMENTO DAS CAIXAS:
  • Caixa 01: 10/10 peças [FECHADA]
    Conteúdo: P-01, P-02, P-03, P-04, P-05, P-06, P-07, P-08, P-09, P-10
  • Caixa 02: 01/10 peças [EM ANDAMENTO]
    Conteúdo: P-11
-----------------------------------------------------------------
DETALHAMENTO DOS MOTIVOS DE REPROVAÇÃO:
  • Peça ID: P-102
    - Peso fora do intervalo (92.0g | esperado: 95g a 105g)
    - Cor não autorizada ('amarelo' | esperado: azul ou verde)
    - Comprimento fora do intervalo (25.0cm | esperado: 10cm a 20cm)
=================================================================
```
