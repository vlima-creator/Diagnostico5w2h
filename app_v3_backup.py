# -*- coding: utf-8 -*-
"""
Aplicação Streamlit - Diagnóstico 5W2H para Reuniões de Start
Versão 3.0 - Funcional para Reuniões Reais
Captura dados do cliente, registra ações em tempo real e gera PDF profissional
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Diagnóstico 5W2H - Reunião de Start",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# BANCO DE DADOS DE AÇÕES (20 ações)
# ============================================================================

BANCO_ACOES = [
    {
        "id": 1,
        "acao": "Ajustar precificacao",
        "categoria": "Precificacao",
        "what": "Revisar e ajustar preços dos SKUs foco com base em margem, concorrência e regras de frete.",
        "why": "Melhorar conversão sem perder margem, reduzir perda para concorrentes e evitar preço abaixo do mínimo.",
        "where": "No(s) canal(is) priorizado(s) no ciclo (ex.: Mercado Livre, Shopee, Amazon, site).",
        "how": "1) Selecionar SKUs foco (top vendas e top visitas)\n2) Levantar custo total e preço mínimo\n3) Comparar com concorrentes e elasticidade\n4) Definir regras por faixa e por canal\n5) Atualizar preços e monitorar por 7 dias\n6) Ajustar a partir de conversão e margem",
        "indicadores": "Margem, conversão, visitas, buy box, GMV, ticket médio",
        "duracao_dias": 7,
        "impacto": 4,
        "esforco": 3
    },
    {
        "id": 2,
        "acao": "Contratar colaborador",
        "categoria": "Pessoas",
        "what": "Abrir vaga, selecionar e contratar colaborador para função definida.",
        "why": "Criar capacidade de execução, tirar gargalos e sustentar crescimento.",
        "where": "Time interno, remoto ou híbrido, conforme necessidade.",
        "how": "1) Definir escopo e metas da função\n2) Escrever descrição da vaga\n3) Divulgar e captar candidatos\n4) Triagem e entrevistas\n5) Teste prático\n6) Proposta e admissão\n7) Onboarding e metas de 30 dias",
        "indicadores": "Tempo de preenchimento, ramp-up, entregas no 30º dia, qualidade de execução",
        "duracao_dias": 21,
        "impacto": 4,
        "esforco": 4
    },
    {
        "id": 3,
        "acao": "Implementar ERP (sistema de integracao)",
        "categoria": "Sistemas",
        "what": "Selecionar, configurar e implementar um ERP para integração de dados de vendas, estoque e financeiro.",
        "why": "Centralizar informações, reduzir erros manuais, melhorar visibilidade operacional e facilitar decisões baseadas em dados.",
        "where": "Sistemas internos da empresa, integrando marketplaces, estoque e financeiro.",
        "how": "1) Definir requisitos e necessidades do negócio\n2) Pesquisar e avaliar opções de ERP (Bling, Omie, SAP, etc)\n3) Negociar contrato e implementação\n4) Configurar módulos (vendas, estoque, financeiro)\n5) Integrar com marketplaces e canais\n6) Treinar equipe no novo sistema\n7) Monitorar e ajustar conforme necessário",
        "indicadores": "Tempo de implementação, taxa de adoção, redução de erros, tempo de resposta, acurácia de estoque",
        "duracao_dias": 30,
        "impacto": 5,
        "esforco": 5
    },
    {
        "id": 4,
        "acao": "Utilizacao de canal (otimizacao do canal atual)",
        "categoria": "Canais",
        "what": "Revisar setup do canal atual e ajustar catálogo, preço, reputação, prazos e operação.",
        "why": "Aumentar conversão e relevância usando melhor o canal que já existe.",
        "where": "Canal atual prioritário (ex.: Mercado Livre).",
        "how": "1) Diagnóstico: reputação, métricas, prazos, políticas\n2) Ajustar cadastro e conteúdo de produtos\n3) Revisar preços e frete\n4) Ajustar estoque e ruptura\n5) Implementar melhorias identificadas\n6) Monitorar impacto por 7 dias\n7) Ajustar conforme resultados",
        "indicadores": "Conversão, reputação, ruptura, visitas, tempo de envio, devoluções",
        "duracao_dias": 14,
        "impacto": 4,
        "esforco": 3
    },
    {
        "id": 5,
        "acao": "Entrada em um novo canal",
        "categoria": "Canais",
        "what": "Abrir e operar um novo canal de vendas, com base em catálogo e capacidade logística.",
        "why": "Diversificar receita e capturar demanda onde o público já compra.",
        "where": "Novo canal escolhido (ex.: Amazon, Magalu, Shein, B2W, TikTok Shop).",
        "how": "1) Validar requisitos e custos do canal\n2) Escolher sortimento inicial (top SKUs)\n3) Preparar integração e cadastro\n4) Subir anúncios e políticas\n5) Treinar equipe no novo canal\n6) Primeiras vendas e ajustes\n7) Escalar com campanhas e reposição",
        "indicadores": "GMV por canal, CAC, conversão, margem, SLA, cancelamentos",
        "duracao_dias": 21,
        "impacto": 4,
        "esforco": 4
    },
    {
        "id": 6,
        "acao": "Ativar fulfillment",
        "categoria": "Operacao",
        "what": "Ativar modelo de fulfillment (estoque em CD) para SKUs elegíveis.",
        "why": "Ganhar prazo e relevância, reduzir falhas de expedição e melhorar conversão.",
        "where": "Programa do canal (ex.: Full, FBA, etc.) e centros de distribuição.",
        "how": "1) Selecionar SKUs (giro x margem x dimensões)\n2) Conferir custos e regras do programa\n3) Preparar etiquetagem e envio\n4) Enviar lote piloto\n5) Acompanhar nível de serviço e vendas\n6) Expandir sortimento conforme resultados",
        "indicadores": "Conversão, tempo de entrega, cancelamentos, devoluções, GMV, custo logística",
        "duracao_dias": 23,
        "impacto": 5,
        "esforco": 4
    },
    {
        "id": 7,
        "acao": "Ativar publicidade",
        "categoria": "Midia",
        "what": "Ativar campanhas pagas no canal (busca, produto, vitrine) com estrutura básica.",
        "why": "Gerar demanda previsível, acelerar vendas e aprender quais produtos respondem melhor.",
        "where": "Painel de anúncios do canal e/ou ferramentas integradas.",
        "how": "1) Definir objetivo e verba inicial\n2) Separar campanhas por objetivo (tráfego, conversão, marca)\n3) Escolher SKUs e palavras-chave\n4) Subir campanhas e anúncios\n5) Monitorar diário por 7 dias\n6) Ajustar lances, negativos e criativos",
        "indicadores": "ROAS/ACOS, CPC, conversão, share de impressão, GMV incremental",
        "duracao_dias": 26,
        "impacto": 5,
        "esforco": 4
    },
    {
        "id": 8,
        "acao": "Trabalhar com promocoes",
        "categoria": "Comercial",
        "what": "Planejar e executar promoções (cupons, descontos, kit) em SKUs estratégicos.",
        "why": "Aumentar volume e visibilidade em períodos de maior competição.",
        "where": "Calendário promocional do canal e página de ofertas.",
        "how": "1) Definir SKUs e limites de margem\n2) Escolher mecânica (cupom, desconto, kit)\n3) Criar calendário e comunicar internamente\n4) Rodar promo e monitorar\n5) Ajustar estoque e preços\n6) Avaliar pós-mortem e documentar resultados",
        "indicadores": "GMV, margem, conversão, ruptura, novos clientes, ranking",
        "duracao_dias": 14,
        "impacto": 4,
        "esforco": 2
    },
    {
        "id": 9,
        "acao": "Melhorar conteudo e cadastro",
        "categoria": "Catalogo",
        "what": "Padronizar títulos, imagens, atributos e descrições para aumentar relevância e conversão.",
        "why": "Reduzir atrito de compra e aumentar qualidade de anúncio.",
        "where": "Catálogo do canal e integrador (se houver).",
        "how": "1) Definir padrão por categoria\n2) Corrigir top 20 SKUs\n3) Replicar padrão no restante\n4) Auditar atributos obrigatórios\n5) Testar imagens e títulos\n6) Revisar mensalmente",
        "indicadores": "Conversão, visitas, reclamações, taxa de perguntas, índice de qualidade",
        "duracao_dias": 14,
        "impacto": 4,
        "esforco": 3
    },
    {
        "id": 10,
        "acao": "Implantar rotina de indicadores",
        "categoria": "Gestao",
        "what": "Criar rotina semanal de acompanhamento e decisão com base em indicadores.",
        "why": "Aumentar velocidade de decisão e manter foco no que traz resultado.",
        "where": "Reunião semanal e painel (Sheets/BI).",
        "how": "1) Definir KPIs e metas\n2) Montar painel simples (Sheets/BI)\n3) Ritual semanal: revisar, decidir, delegar\n4) Registrar plano de ação\n5) Documentar decisões e ações tomadas\n6) Fazer follow-up das ações na semana seguinte\n7) Revisar resultados em 30 dias",
        "indicadores": "GMV, margem, conversão, ruptura, ROAS, SLA, devoluções",
        "duracao_dias": 30,
        "impacto": 5,
        "esforco": 2
    },
    {
        "id": 11,
        "acao": "Rotinas e processos",
        "categoria": "Gestao",
        "what": "Estruturar e documentar rotinas operacionais e estratégicas.",
        "why": "Garantir padrão, previsibilidade e escalabilidade da operação.",
        "where": "Operação geral da empresa.",
        "how": "1) Mapear processos atuais\n2) Identificar gargalos e ineficiências\n3) Documentar fluxo ideal\n4) Definir responsáveis\n5) Treinar equipe nos novos processos\n6) Monitorar aderência por 2 semanas\n7) Ajustar conforme feedback",
        "indicadores": "Tempo de execução, retrabalho, erros operacionais",
        "duracao_dias": 30,
        "impacto": 5,
        "esforco": 3
    },
    {
        "id": 12,
        "acao": "Analisar a curva ABC",
        "categoria": "Gestao",
        "what": "Classificar produtos por representatividade de faturamento e margem.",
        "why": "Priorizar foco nos produtos que realmente movem o resultado.",
        "where": "Relatórios de vendas e ERP.",
        "how": "1) Exportar vendas (últimos 90 dias)\n2) Classificar por faturamento\n3) Separar A, B e C\n4) Definir estratégia por curva\n5) Criar plano de ação baseado na curva ABC\n6) Comunicar resultados à equipe\n7) Revisar mensalmente",
        "indicadores": "GMV por SKU, margem, giro",
        "duracao_dias": 5,
        "impacto": 4,
        "esforco": 2
    },
    {
        "id": 13,
        "acao": "Gestao de Compras (Mix de Produtos)",
        "categoria": "Compras",
        "what": "Definir mix ideal baseado em giro e margem.",
        "why": "Evitar ruptura e excesso de estoque.",
        "where": "ERP e relatórios de estoque.",
        "how": "1) Cruzar curva ABC com estoque\n2) Identificar ruptura e excesso\n3) Planejar reposição\n4) Negociar fornecedores\n5) Implementar novo mix no sistema\n6) Monitorar resultados por 7 dias\n7) Ajustar conforme performance",
        "indicadores": "Ruptura, giro, cobertura de estoque",
        "duracao_dias": 15,
        "impacto": 5,
        "esforco": 4
    },
    {
        "id": 14,
        "acao": "Gestao de Atendimento",
        "categoria": "Operacao",
        "what": "Padronizar e monitorar atendimento ao cliente.",
        "why": "Melhorar reputação e conversão.",
        "where": "Canal de atendimento do marketplace.",
        "how": "1) Criar scripts padrão\n2) Definir SLA (tempo de resposta)\n3) Monitorar tempo de resposta\n4) Revisar feedbacks e reclamações\n5) Implementar sistema de monitoramento\n6) Fazer reunião de feedback com equipe\n7) Treinar conforme necessidade",
        "indicadores": "Tempo resposta, reputação, NPS",
        "duracao_dias": 30,
        "impacto": 4,
        "esforco": 3
    },
    {
        "id": 15,
        "acao": "Padronizacao de Anuncios",
        "categoria": "Catalogo",
        "what": "Criar padrão de títulos, imagens e descrições.",
        "why": "Aumentar conversão e qualidade dos anúncios.",
        "where": "Anúncios ativos no marketplace.",
        "how": "1) Definir modelo padrão\n2) Ajustar top SKUs\n3) Replicar modelo\n4) Revisar atributos\n5) Testar padrão com A/B testing\n6) Monitorar performance por 7 dias\n7) Documentar aprendizados",
        "indicadores": "Conversão, visitas, índice de qualidade",
        "duracao_dias": 14,
        "impacto": 4,
        "esforco": 3
    },
    {
        "id": 16,
        "acao": "Padronizacao de Cadastros",
        "categoria": "Catalogo",
        "what": "Padronizar atributos e informações técnicas dos produtos.",
        "why": "Evitar erros e melhorar indexação.",
        "where": "ERP e marketplace.",
        "how": "1) Revisar atributos obrigatórios\n2) Criar checklist de validação\n3) Corrigir inconsistências\n4) Corrigir inconsistências identificadas\n5) Validar integração com marketplace\n6) Documentar padrão para referência futura\n7) Treinar equipe no novo padrão",
        "indicadores": "Erros de integração, qualidade de cadastro",
        "duracao_dias": 14,
        "impacto": 4,
        "esforco": 3
    },
    {
        "id": 17,
        "acao": "Ads e Campanhas",
        "categoria": "Midia",
        "what": "Estruturar campanhas de anúncios pagos.",
        "why": "Gerar demanda previsível e escalar vendas.",
        "where": "Painel de anúncios do canal.",
        "how": "1) Definir verba e objetivos\n2) Criar campanhas por objetivo\n3) Monitorar diário\n4) Ajustar palavras e lances\n5) Definir KPIs e metas de performance\n6) Criar dashboard de monitoramento\n7) Escalar vencedores",
        "indicadores": "ROAS, ACOS, CPC, GMV",
        "duracao_dias": 26,
        "impacto": 5,
        "esforco": 4
    },
    {
        "id": 18,
        "acao": "Expedicao (PICK & PACK)",
        "categoria": "Operacao",
        "what": "Organizar processo de separação e envio.",
        "why": "Reduzir erros e atrasos logísticos.",
        "where": "Centro de distribuição interno.",
        "how": "1) Mapear fluxo atual\n2) Criar padrão de separação\n3) Organizar layout do CD\n4) Treinar equipe\n5) Implementar sistema de rastreamento\n6) Fazer auditoria de qualidade\n7) Monitorar SLA",
        "indicadores": "Erros de envio, prazo, cancelamentos",
        "duracao_dias": 20,
        "impacto": 4,
        "esforco": 4
    },
    {
        "id": 19,
        "acao": "Entrada Produtos",
        "categoria": "Operacao",
        "what": "Padronizar recebimento e cadastro de novos produtos.",
        "why": "Evitar divergências de estoque.",
        "where": "Estoque e ERP.",
        "how": "1) Conferência física\n2) Cadastro correto no ERP\n3) Validação de custo\n4) Treinar equipe no novo processo\n5) Monitorar aderência\n6) Fazer auditoria de qualidade\n7) Documentar procedimento",
        "indicadores": "Erros de estoque, divergências",
        "duracao_dias": 10,
        "impacto": 4,
        "esforco": 3
    },
    {
        "id": 20,
        "acao": "Compras",
        "categoria": "Compras",
        "what": "Planejar e executar compras estratégicas.",
        "why": "Garantir abastecimento sem excesso de capital parado.",
        "where": "Fornecedores e ERP.",
        "how": "1) Analisar giro\n2) Definir necessidade\n3) Negociar com fornecedores\n4) Negociar prazos e condições de pagamento\n5) Confirmar data de entrega\n6) Acompanhar recebimento\n7) Validar qualidade e quantidade",
        "indicadores": "Cobertura estoque, margem, giro",
        "duracao_dias": 15,
        "impacto": 4,
        "esforco": 3
    }
]

CANAIS_DISPONIVEIS = [
    "Mercado Livre",
    "Shopee",
    "Amazon",
    "OLX",
    "Magalu",
    "B2W (Americanas)",
    "TikTok Shop",
    "Site Próprio",
    "WhatsApp",
    "Outro"
]

# ============================================================================
# INICIALIZAÇÃO DO SESSION STATE
# ============================================================================

if "cliente_data" not in st.session_state:
    st.session_state.cliente_data = {
        "nome": "",
        "cnpj": "",
        "canais": [],
        "data_reuniao": datetime.now()
    }

if "acoes_selecionadas" not in st.session_state:
    st.session_state.acoes_selecionadas = []

if "observacoes" not in st.session_state:
    st.session_state.observacoes = ""

# ============================================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================================

def obter_acao_por_id(acao_id):
    """Busca uma ação pelo ID"""
    for acao in BANCO_ACOES:
        if acao["id"] == acao_id:
            return acao
    return None

def calcular_score(impacto, esforco):
    """Calcula o score: (Impacto × 10) - (Esforço × 2)"""
    return (impacto * 10) - (esforco * 2)

def adicionar_acao(acao_id, observacao=""):
    """Adiciona uma ação ao histórico"""
    acao = obter_acao_por_id(acao_id)
    if acao:
        score = calcular_score(acao["impacto"], acao["esforco"])
        st.session_state.acoes_selecionadas.append({
            "id": acao_id,
            "acao": acao["acao"],
            "categoria": acao["categoria"],
            "duracao_dias": acao["duracao_dias"],
            "impacto": acao["impacto"],
            "esforco": acao["esforco"],
            "score": score,
            "observacao": observacao,
            "timestamp": datetime.now()
        })

def remover_acao(index):
    """Remove uma acao do historico"""
    if 0 <= index < len(st.session_state.acoes_selecionadas):
        st.session_state.acoes_selecionadas.pop(index)

def gerar_grafico_radar(acoes_selecionadas):
    """Gera um grafico radar com as categorias e quantidade de acoes"""
    if not acoes_selecionadas:
        return None
    
    # Contar acoes por categoria
    df_acoes = pd.DataFrame(acoes_selecionadas)
    categorias_count = df_acoes['categoria'].value_counts().to_dict()
    
    # Garantir que todas as categorias aparecam (mesmo com 0)
    todas_categorias = sorted(list(set([a["categoria"] for a in BANCO_ACOES])))
    valores = [categorias_count.get(cat, 0) for cat in todas_categorias]
    
    # Criar grafico radar
    fig = go.Figure(data=go.Scatterpolar(
        r=valores,
        theta=todas_categorias,
        fill='toself',
        name='Acoes por Categoria',
        line=dict(color='#1E3A8A'),
        fillcolor='rgba(30, 58, 138, 0.3)',
        hovertemplate='<b>%{theta}</b><br>Acoes: %{r}<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(valores) + 1 if valores else 1],
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=11)
            )
        ),
        showlegend=False,
        height=500,
        hovermode='closest',
        title=dict(
            text='<b>Analise de Deficiencias por Categoria</b>',
            font=dict(size=16, color='#1E3A8A')
        )
    )
    
    return fig

def calcular_prioridades(acoes_selecionadas):
    """Calcula as 3 categorias de prioridade baseado em impacto e quantidade"""
    if not acoes_selecionadas:
        return []
    
    df_acoes = pd.DataFrame(acoes_selecionadas)
    
    # Agrupar por categoria e calcular score de prioridade
    prioridades = []
    for categoria in df_acoes['categoria'].unique():
        df_cat = df_acoes[df_acoes['categoria'] == categoria]
        
        # Score de prioridade = (quantidade de acoes x 10) + (impacto medio x 5)
        qtd_acoes = len(df_cat)
        impacto_medio = df_cat['impacto'].mean()
        score_prioridade = (qtd_acoes * 10) + (impacto_medio * 5)
        
        prioridades.append({
            'categoria': categoria,
            'qtd_acoes': qtd_acoes,
            'impacto_medio': impacto_medio,
            'score_prioridade': score_prioridade
        })
    
    # Ordenar por score de prioridade (descendente)
    prioridades.sort(key=lambda x: x['score_prioridade'], reverse=True)
    
    # Retornar top 3
    return prioridades[:3]

def gerar_pdf_relatorio(cliente_data, acoes_selecionadas, observacoes):
    """Gera um PDF profissional com o plano de ação"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Estilos customizados
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#3B82F6'),
        spaceAfter=8,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold'
    )
    
    # Cabeçalho
    story.append(Paragraph("DIAGNÓSTICO 5W2H", titulo_style))
    story.append(Paragraph("Plano de Ação para Reunião de Start", subtitulo_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Dados do Cliente
    story.append(Paragraph("DADOS DO CLIENTE", subtitulo_style))
    
    cliente_info = f"""
    <b>Nome:</b> {cliente_data['nome']}<br/>
    <b>CNPJ:</b> {cliente_data['cnpj']}<br/>
    <b>Canais:</b> {', '.join(cliente_data['canais']) if cliente_data['canais'] else 'Não informado'}<br/>
    <b>Data da Reunião:</b> {cliente_data['data_reuniao'].strftime('%d/%m/%Y às %H:%M')}
    """
    story.append(Paragraph(cliente_info, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Ações Selecionadas
    if acoes_selecionadas:
        story.append(Paragraph("AÇÕES SELECIONADAS", subtitulo_style))
        
        # Tabela de ações
        dados_tabela = [["#", "Ação", "Categoria", "Duração", "Impacto", "Esforço", "Score"]]
        
        for idx, acao in enumerate(acoes_selecionadas, 1):
            dados_tabela.append([
                str(idx),
                acao["acao"][:30],
                acao["categoria"],
                f"{acao['duracao_dias']}d",
                f"{acao['impacto']}/5",
                f"{acao['esforco']}/5",
                str(acao["score"])
            ])
        
        tabela = Table(dados_tabela, colWidths=[0.5*inch, 2*inch, 1.2*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.7*inch])
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F3F4F6')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D1D5DB')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        
        story.append(tabela)
        story.append(Spacer(1, 0.3*inch))
        
        # Estatísticas
        total_acoes = len(acoes_selecionadas)
        duracao_total = sum(a["duracao_dias"] for a in acoes_selecionadas)
        impacto_medio = sum(a["impacto"] for a in acoes_selecionadas) / total_acoes if total_acoes > 0 else 0
        score_total = sum(a["score"] for a in acoes_selecionadas)
        
        stats = f"""
        <b>Total de Ações:</b> {total_acoes}<br/>
        <b>Duração Total:</b> {duracao_total} dias<br/>
        <b>Impacto Médio:</b> {impacto_medio:.1f}/5<br/>
        <b>Score Total:</b> {score_total}
        """
        story.append(Paragraph("ESTATÍSTICAS", subtitulo_style))
        story.append(Paragraph(stats, styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
    
    # Observações
    if observacoes:
        story.append(Paragraph("OBSERVAÇÕES E NOTAS", subtitulo_style))
        story.append(Paragraph(observacoes, styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
    
    # Detalhes das Ações
    if acoes_selecionadas:
        story.append(PageBreak())
        story.append(Paragraph("DETALHES DAS AÇÕES", subtitulo_style))
        story.append(Spacer(1, 0.2*inch))
        
        for idx, acao_selecionada in enumerate(acoes_selecionadas, 1):
            acao_completa = obter_acao_por_id(acao_selecionada["id"])
            
            story.append(Paragraph(f"{idx}. {acao_completa['acao']}", ParagraphStyle(
                'ActionTitle',
                parent=styles['Heading3'],
                fontSize=11,
                textColor=colors.HexColor('#1E3A8A'),
                spaceAfter=6,
                fontName='Helvetica-Bold'
            )))
            
            detalhes = f"""
            <b>Categoria:</b> {acao_completa['categoria']}<br/>
            <b>WHAT (O quê):</b> {acao_completa['what']}<br/>
            <b>WHY (Por quê):</b> {acao_completa['why']}<br/>
            <b>WHERE (Onde):</b> {acao_completa['where']}<br/>
            <b>Duração:</b> {acao_completa['duracao_dias']} dias<br/>
            <b>Indicadores:</b> {acao_completa['indicadores']}<br/>
            """
            
            if acao_selecionada["observacao"]:
                detalhes += f"<b>Observação:</b> {acao_selecionada['observacao']}<br/>"
            
            story.append(Paragraph(detalhes, styles['Normal']))
            story.append(Spacer(1, 0.15*inch))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

# ============================================================================
# INTERFACE STREAMLIT
# ============================================================================

# Header
st.markdown("""
<style>
    .header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .header h1 {
        margin: 0;
        font-size: 2.5rem;
    }
    .header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
</style>
<div class="header">
    <h1>📋 Diagnóstico 5W2H</h1>
    <p>Reunião de Start com Cliente - Gerador de Plano de Ação</p>
</div>
""", unsafe_allow_html=True)

# Abas principais
tab1, tab2, tab3, tab4 = st.tabs(["📝 Dados do Cliente", "✅ Selecionar Ações", "📊 Dashboard", "📋 Resumo e Relatório"])

# ============================================================================
# ABA 1: DADOS DO CLIENTE
# ============================================================================

with tab1:
    st.subheader("Informações do Cliente")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.cliente_data["nome"] = st.text_input(
            "Nome do Cliente",
            value=st.session_state.cliente_data["nome"],
            placeholder="Ex: Empresa XYZ Ltda"
        )
        
        st.session_state.cliente_data["cnpj"] = st.text_input(
            "CNPJ",
            value=st.session_state.cliente_data["cnpj"],
            placeholder="Ex: 12.345.678/0001-90"
        )
    
    with col2:
        st.session_state.cliente_data["data_reuniao"] = st.date_input(
            "Data da Reunião",
            value=st.session_state.cliente_data["data_reuniao"]
        )
        
        st.session_state.cliente_data["canais"] = st.multiselect(
            "Canais que o Cliente Trabalha",
            options=CANAIS_DISPONIVEIS,
            default=st.session_state.cliente_data["canais"]
        )
    
    st.markdown("---")
    
    # Resumo dos dados
    if st.session_state.cliente_data["nome"]:
        st.success("✅ Dados do cliente preenchidos")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Cliente", st.session_state.cliente_data["nome"][:30])
        with col2:
            st.metric("CNPJ", st.session_state.cliente_data["cnpj"] or "Não informado")
        with col3:
            st.metric("Canais", len(st.session_state.cliente_data["canais"]))

# ============================================================================
# ABA 2: SELECIONAR AÇÕES
# ============================================================================

with tab2:
    st.subheader("Selecione as Ações para o Plano")
    
    if not st.session_state.cliente_data["nome"]:
        st.warning("⚠️ Preencha os dados do cliente na aba anterior primeiro!")
    else:
        # Filtro por categoria
        categorias = sorted(list(set([a["categoria"] for a in BANCO_ACOES])))
        categoria_selecionada = st.selectbox("Filtrar por Categoria", ["Todas"] + categorias)
        
        # Filtrar ações
        if categoria_selecionada == "Todas":
            acoes_filtradas = BANCO_ACOES
        else:
            acoes_filtradas = [a for a in BANCO_ACOES if a["categoria"] == categoria_selecionada]
        
        # Exibir ações
        st.markdown("---")
        
        for acao in acoes_filtradas:
            col1, col2 = st.columns([0.8, 0.2])
            
            with col1:
                st.markdown(f"**{acao['acao']}** - {acao['categoria']}")
                st.caption(f"📋 {acao['what']}")
                
                # Mostrar métricas
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.caption(f"⏱️ {acao['duracao_dias']}d")
                with m2:
                    st.caption(f"📈 Impacto: {acao['impacto']}/5")
                with m3:
                    st.caption(f"💪 Esforço: {acao['esforco']}/5")
                with m4:
                    score = calcular_score(acao['impacto'], acao['esforco'])
                    st.caption(f"⭐ Score: {score}")
            
            with col2:
                if st.button("Adicionar", key=f"add_{acao['id']}", use_container_width=True):
                    adicionar_acao(acao['id'])
                    st.success(f"✅ {acao['acao']} adicionada!")
                    st.rerun()
        
        st.markdown("---")
        st.subheader("Ações Selecionadas")
        
        if st.session_state.acoes_selecionadas:
            for idx, acao in enumerate(st.session_state.acoes_selecionadas):
                col1, col2, col3 = st.columns([0.7, 0.2, 0.1])
                
                with col1:
                    st.markdown(f"**{idx + 1}. {acao['acao']}**")
                    st.caption(f"{acao['categoria']} | {acao['duracao_dias']}d | Impacto: {acao['impacto']}/5 | Score: {acao['score']}")
                
                with col2:
                    observacao = st.text_input(
                        "Observação",
                        value=acao.get("observacao", ""),
                        key=f"obs_{idx}",
                        placeholder="Adicionar nota..."
                    )
                    if observacao != acao.get("observacao", ""):
                        st.session_state.acoes_selecionadas[idx]["observacao"] = observacao
                
                with col3:
                    if st.button("❌", key=f"del_{idx}", use_container_width=True):
                        remover_acao(idx)
                        st.rerun()
                
                st.divider()
            
            # Estatísticas
            st.markdown("---")
            st.subheader("Estatísticas do Plano")
            
            col1, col2, col3, col4 = st.columns(4)
            
            total_acoes = len(st.session_state.acoes_selecionadas)
            duracao_total = sum(a["duracao_dias"] for a in st.session_state.acoes_selecionadas)
            impacto_medio = sum(a["impacto"] for a in st.session_state.acoes_selecionadas) / total_acoes
            score_total = sum(a["score"] for a in st.session_state.acoes_selecionadas)
            
            with col1:
                st.metric("Total de Ações", total_acoes)
            with col2:
                st.metric("Duração Total", f"{duracao_total} dias")
            with col3:
                st.metric("Impacto Médio", f"{impacto_medio:.1f}/5")
            with col4:
                st.metric("Score Total", score_total)
        else:
            st.info("👈 Selecione ações para criar o plano")

# ============================================================================
# ABA 3: RESUMO E RELATÓRIO
# ============================================================================

with tab3:
    st.subheader("Resumo e Geração de Relatório")
    
    if not st.session_state.acoes_selecionadas:
        st.warning("⚠️ Selecione pelo menos uma ação na aba anterior!")
    else:
        # Observações gerais
        st.markdown("---")
        st.subheader("Observações Gerais da Reunião")
        
        st.session_state.observacoes = st.text_area(
            "Adicione observações, restrições, combinados ou notas importantes",
            value=st.session_state.observacoes,
            height=150,
            placeholder="Ex: Cliente tem restrição orçamentária, priorizar ações de baixo custo..."
        )
        
        st.markdown("---")
        st.subheader("Resumo do Plano")
        
        # Exibir resumo
        col1, col2, col3, col4 = st.columns(4)
        
        total_acoes = len(st.session_state.acoes_selecionadas)
        duracao_total = sum(a["duracao_dias"] for a in st.session_state.acoes_selecionadas)
        impacto_medio = sum(a["impacto"] for a in st.session_state.acoes_selecionadas) / total_acoes
        score_total = sum(a["score"] for a in st.session_state.acoes_selecionadas)
        
        with col1:
            st.metric("Total de Ações", total_acoes)
        with col2:
            st.metric("Duração Total", f"{duracao_total} dias")
        with col3:
            st.metric("Impacto Médio", f"{impacto_medio:.1f}/5")
        with col4:
            st.metric("Score Total", score_total)
        
        st.markdown("---")
        st.subheader("Ações Selecionadas")
        
        df_acoes = pd.DataFrame(st.session_state.acoes_selecionadas)
        df_exibicao = df_acoes[["acao", "categoria", "duracao_dias", "impacto", "esforco", "score"]].copy()
        df_exibicao.columns = ["Ação", "Categoria", "Duração (dias)", "Impacto", "Esforço", "Score"]
        
        st.dataframe(df_exibicao, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("Gerar Relatório")
        
        # Botão para gerar PDF
        pdf_buffer = gerar_pdf_relatorio(
            st.session_state.cliente_data,
            st.session_state.acoes_selecionadas,
            st.session_state.observacoes
        )
        
        st.download_button(
            label="📄 Baixar Relatório em PDF",
            data=pdf_buffer,
            file_name=f"Plano_5W2H_{st.session_state.cliente_data['nome']}_{datetime.now().strftime('%d%m%Y')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem;">
    <p>Diagnóstico 5W2H v3.0 | Funcional para Reuniões de Start</p>
    <p>Desenvolvido para capturar dados do cliente e gerar planos de ação profissionais</p>
</div>
""", unsafe_allow_html=True)
