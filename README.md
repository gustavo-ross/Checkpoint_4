# ERP SHOW

## 📌 O que é o projeto?
O **ERP SHOW** é um Sistema de Gestão de Estoque (ERP) desenvolvido para uso em computadores (Desktop). Diferente de sistemas de controle antigos, complexos e visualmente defasados, este software foi arquitetado com um cuidado gigantesco na interface e na experiência de uso. 

Construído em Python, ele une um banco de dados local robusto a uma navegação fluida em abas, gráficos interativos gerados em tempo real e um design moderno (com suporte a Modo Claro e Escuro). Por baixo dos panos, o projeto utiliza a arquitetura MVC (Modelo-Visão-Controlador), garantindo que a inteligência do sistema, os dados salvos e as telas visuais funcionem de forma rápida, segura e escalável.

## 🚀 Para que serve na prática?
O sistema serve para eliminar o caos na rotina de pequenos e médios negócios, centralizando o controle de mercadorias e finanças em um único lugar. Ele foi desenhado para que um operador ou dono de loja consiga:

- **Automatizar o Fluxo de Estoque:** Ao registrar a venda de um item, o sistema calcula o valor total e retira o produto do inventário de forma automática, impedindo furos no estoque (incluindo uma trava de segurança para não registrar produtos com o mesmo nome).
- **Auditar Mudanças Financeiras:** Através de uma aba de Histórico, o sistema cria um rastro de segurança. Se um preço for alterado, o ERP salva para sempre o valor antigo, o novo e a data exata da mudança.
- **Agilizar o Atendimento:** Com barras de pesquisa inteligentes implementadas em todas as telas, o operador encontra produtos ou registros do histórico digitando apenas parte do nome, sem precisar rolar listas infinitas.
- **Tomar Decisões Visuais:** Em vez de forçar o usuário a ler tabelas maçantes, o Dashboard traduz os números do banco de dados em gráficos limpos. É possível bater o olho e ver imediatamente o faturamento do mês, picos de vendas por dia, os 5 produtos que mais saem e a fatia exata que cada produto ocupa no armazenamento da loja.

---

## ✨ Funcionalidades que Fazem a Diferença

- 🌗 **Modo Escuro Nativo:** Um switch no cabeçalho permite alternar instantaneamente entre os temas Claro e Escuro, invertendo cores de textos, tabelas e até dos gráficos automaticamente para maior conforto visual.
- 📊 **Visualização Alternável (Switch Pizza):** Na aba de produtos, o utilizador pode alternar entre a lista tradicional e um gráfico de pizza que exibe a proporção volumétrica do estoque atual.
- 🛡️ **Bloqueio Hardcore de Duplicatas:** O sistema impede o cadastro de produtos com nomes idênticos (mesmo variando maiúsculas e minúsculas), mantendo a integridade do banco de dados.

---

## 🏗️ Organização do Sistema (Estrutura MVC)

O código foi totalmente modularizado e separado em arquivos independentes para facilitar futuras melhorias e a manutenção por outros programadores:

- `main_erp_estoque.py`: O ponto de partida que inicia a aplicação.
- `config.py`: Central de estilo. Concentra todas as cores, hovers e regras visuais do Modo Claro e Escuro.
- `modelo.py` (Model): Responsável direto pela comunicação segura com o banco de dados SQLite (`erp_estoque.db`).
- `controlador.py` (Controller): O cérebro do software. Valida os campos, impede valores negativos e aplica as regras de negócio.
- `tela_principal.py` & `aba_*.py` / `modal_*.py` (View): Camada inteiramente visual construída com **CustomTkinter** e **Matplotlib** utilizando herança de classes.

---

## 💻 Criado por

Gustavo Ross © 2026