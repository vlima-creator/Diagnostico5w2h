# 📋 Diagnóstico 5W2H - Gerador de Plano de Ação

Um aplicativo Streamlit interativo para reuniões de start com clientes, que permite capturar ações e gerar automaticamente um plano 5W2H completo com relatórios profissionais.

## 🎯 Funcionalidades

- **Captura de Reunião**: Interface intuitiva para preencher dados da reunião de start
- **Banco de 20 Ações Pré-definidas**: Ações estratégicas com 5W2H já estruturado
- **Customização Automática**: Ajuste duração, impacto e esforço conforme necessário
- **Ajuste de Prazo**: Opção para ajustar o prazo (dias) de cada ação individualmente. Caso não seja preenchido, o prazo pré-determinado será utilizado.
- **Cálculo de Score**: Score automático baseado em Impacto e Esforço
- **Plano 5W2H Completo**: What, Why, Where, When, Who, How, How Much
- **Timeline Visual**: Gráfico Gantt com a duração da ação
- **Exportação**: Relatórios em PDF e Excel
- **Histórico**: Acompanhamento de todos os planos gerados
- **Estatísticas**: Análise de scores, categorias e indicadores

## 🚀 Como Usar

### 1. Instalação

```bash
# Clone o repositório
git clone https://github.com/vlima-creator/Diagnostico5w2h.git
cd Diagnostico5w2h

# Instale as dependências
pip install -r requirements.txt
```

### 2. Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá em `http://localhost:8501`

### 3. Fluxo de Uso

#### Aba 1: Captura de Reunião
1. Preencha o **Nome do Cliente**
2. Preencha o **Responsável pela Execução**
3. Selecione a **Data de Início**
4. Escolha a **Ação** do banco de dados
5. Customize se necessário:
   - Duração (dias)
   - Impacto (1-5)
   - Esforço (1-5)
6. Adicione **Notas da Reunião**
7. Clique em **Gerar Plano 5W2H**

#### Aba 2: Plano 5W2H
- Visualize o plano completo em abas (WHAT, WHY, WHERE, WHEN, WHO, HOW, HOW MUCH)
- Veja a timeline visual
- Exporte em **PDF** ou **Excel**

#### Aba 3: Histórico
- Acompanhe todos os planos gerados
- Veja estatísticas e gráficos de análise
- Analise scores, categorias e indicadores

## 📊 Banco de Ações Disponíveis

O aplicativo inclui 20 ações pré-definidas em 8 categorias:

### Categorias:
- **Precificação**: Ajustar precificação
- **Pessoas**: Contratar colaborador, Contratar RP
- **Canais**: Utilização de canal, Entrada em novo canal
- **Operação**: Ativar fulfillment, Gestão de Atendimento, Expedicao, Entrada Produtos
- **Midia**: Ativar publicidade, Ads e Campanhas
- **Comercial**: Trabalhar com promocoes
- **Catalogo**: Melhorar conteudo, Padronizacao de Anuncios, Padronizacao de Cadastros
- **Gestao**: Implantar rotina de indicadores, Rotinas e processos, Analisar curva ABC
- **Compras**: Gestao de Compras, Compras

## 🧮 Fórmula de Score

```
Score = (Impacto × Peso Impacto) - (Esforço × Peso Esforço)
Score = (Impacto × 10) - (Esforço × 2)
```

**Exemplo:**
- Impacto: 4/5
- Esforço: 3/5
- Score = (4 × 10) - (3 × 2) = 40 - 6 = **34**

## 📄 Exportação

### PDF
- Relatório profissional com:
  - Dados do cliente
  - Plano 5W2H completo
  - Indicadores de sucesso
  - Notas da reunião

### Excel
- Planilha estruturada com:
  - Dados do cliente
  - Plano 5W2H completo
  - Indicadores
  - Formatação profissional

## ⚙️ Configuração

As configurações padrão estão no início do arquivo `app.py`:

```python
CONFIG = {
    "peso_impacto": 10,      # Peso do impacto no score
    "peso_esforco": 2,       # Peso do esforço no score
    "dias_ciclo": 30         # Dias do ciclo padrão
}
```

## 🔧 Customização

### Adicionar Novas Ações

Adicione um novo dicionário à lista `BANCO_ACOES` em `app.py`:

```python
{
    "id": 21,
    "acao": "Nome da Ação",
    "categoria": "Categoria",
    "what": "O quê será feito?",
    "why": "Por quê fazer?",
    "where": "Onde será feito?",
    "how": "Como será feito? (passo a passo)",
    "indicadores": "Indicadores de sucesso",
    "dia_inicio_padrao": 1,
    "duracao_dias": 14,
    "custo_padrao": 0,
    "impacto_padrao": 4,
    "esforco_padrao": 3
}
```

### Modificar Pesos do Score

Edite a seção `CONFIG` em `app.py` para ajustar os pesos:

```python
CONFIG = {
    "peso_impacto": 15,  # Aumentar importância do impacto
    "peso_esforco": 3,   # Aumentar penalidade do esforço
    "dias_ciclo": 30
}
```

### Ajustar Duração das Ações

Na aba "Selecionar Ações", ao adicionar uma ação, um campo "Duração (dias)" será exibido. Você pode alterar o valor padrão para customizar o prazo da ação. Se o campo for deixado com o valor padrão, ele será utilizado.

## 📋 Estrutura do Plano 5W2H

| Campo | Descrição | Exemplo |
|-------|-----------|----------|
| **WHAT** | O quê será feito? | Revisar e ajustar preços |
| **WHY** | Por quê fazer? | Melhorar conversão e margem |
| **WHERE** | Onde será feito? | Mercado Livre, Shopee, Amazon |
| **WHEN** | Quando será feito? | 01/03/2026 a 08/03/2026 |
| **WHO** | Quem vai fazer? | João Silva |
| **HOW** | Como será feito? | 6 passos detalhados |
| **HOW MUCH** | Quanto custará? | R$ 0,00 |

## 📈 Indicadores de Sucesso

Cada ação inclui indicadores sugeridos:
- Margem, conversão, visitas, buy box, GMV, ticket médio
- ROAS, ACOS, CPC, share de impressão
- Tempo de resposta, reputação, NPS
- E muitos outros conforme a ação

## 🔐 Segurança

- Dados armazenados apenas em session state (não persistem após fechar)
- Nenhuma informação é enviada para servidores externos
- Relatórios gerados localmente

## 📝 Notas

- O aplicativo usa session state do Streamlit para armazenar dados
- Os dados são perdidos ao recarregar a página
- Para persistência, considere adicionar banco de dados
- Recomenda-se usar em reuniões ao vivo com o cliente

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Adicionar novas ações
- Melhorar a interface
- Adicionar novos recursos
- Reportar bugs

## 📄 Licença

MIT License - Veja LICENSE para detalhes

## 👨‍💼 Autor

Desenvolvido para otimizar reuniões de start com clientes e estruturar planos de ação estratégicos.

---

**Versão:** 1.1.0  
**Última atualização:** Fevereiro 2026
