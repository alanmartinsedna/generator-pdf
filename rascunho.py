from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie

# =========================
# DADOS
# =========================
empresa_nome = "Empresa Exemplo LTDA"
logo_path = "logo.png"  # coloque sua logo aqui

grupos = [
    ("Colaboradores", 50, 50, 0, [90, 50, 20, 30]),
    ("Financeiro", 20, 10, 10, [25, 10, 66, 39]),
    ("Produção", 45, 35, 10, [45, 45, 68, 73]),
    ("Serviços Gerais", 120, 80, 40, [73, 27, 18, 79]),
]

# =========================
# FUNÇÕES
# =========================
def media(lista):
    return sum(lista) / len(lista)

def classificacao(valor):
    if valor <= 20:
        return "Muito Ruim"
    elif valor <= 40:
        return "Ruim"
    elif valor <= 60:
        return "Razoável"
    elif valor <= 80:
        return "Bom"
    else:
        return "Excelente"

def gerar_recomendacao(valor):
    if valor <= 20:
        return "Muito Ruim: Situação crítica com alto risco psicossocial. Requer intervenção imediata, revisão estrutural do ambiente de trabalho, apoio psicológico intensivo e ações emergenciais de gestão."
    elif valor <= 40:
        return "Ruim: Indica problemas relevantes no ambiente psicossocial. Recomenda-se análise detalhada dos fatores de risco, implementação de melhorias na comunicação e suporte aos colaboradores."
    elif valor <= 60:
        return "Razoável: Situação moderada. Existem pontos de atenção que devem ser monitorados e melhorados gradualmente através de ações preventivas e treinamentos."
    elif valor <= 80:
        return "Bom: Ambiente relativamente saudável. Manter práticas atuais, reforçar cultura organizacional positiva e monitorar possíveis oscilações."
    else:
        return "Excelente: Ambiente altamente saudável. Manter estratégias atuais, fortalecer boas práticas e utilizar como referência para outras áreas."

# =========================
# DOCUMENTO
# =========================
doc = SimpleDocTemplate("relatorio.pdf", pagesize=A4)
styles = getSampleStyleSheet()
elements = []

# =========================
# HEADER
# =========================
elements.append(Paragraph(f"<b>{empresa_nome}</b>", styles['Title']))
elements.append(Spacer(1, 10))

elements.append(Paragraph("DIAGNÓSTICO DE RISCOS PSICOSSOCIAIS", styles['Heading1']))
elements.append(Spacer(1, 20))

# =========================
# TABELA
# =========================
tabela = [["Grupo", "Total", "Responderam", "Não Resp.", "Aderência %"]]

total_geral = 0
resp_geral = 0
nao_resp_geral = 0

for nome, total, resp, nao_resp, _ in grupos:
    aderencia = (resp / total) * 100
    tabela.append([nome, total, resp, nao_resp, f"{aderencia:.1f}%"])
    
    total_geral += total
    resp_geral += resp
    nao_resp_geral += nao_resp

table = Table(tabela)
table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.grey),
    ('GRID', (0,0), (-1,-1), 1, colors.black)
]))

elements.append(table)
elements.append(Spacer(1, 20))

# =========================
# RESUMO
# =========================
elements.append(Paragraph("<b>Resumo do Diagnóstico</b>", styles['Heading2']))

perc_resp = (resp_geral / total_geral) * 100
perc_nao = (nao_resp_geral / total_geral) * 100

elements.append(Paragraph(f"Total: {total_geral}", styles['Normal']))
elements.append(Paragraph(f"Responderam: {resp_geral} ({perc_resp:.1f}%)", styles['Normal']))
elements.append(Paragraph(f"Não responderam: {nao_resp_geral} ({perc_nao:.1f}%)", styles['Normal']))

elements.append(Spacer(1, 20))

# =========================
# GRÁFICO DE PIZZA
# =========================
drawing = Drawing(200, 150)
pie = Pie()

pie.data = [resp_geral, nao_resp_geral]
pie.labels = ["Responderam", "Não responderam"]

drawing.add(pie)
elements.append(drawing)

elements.append(PageBreak())

# =========================
# GRUPOS
# =========================
for nome, total, resp, nao_resp, agrupadores in grupos:
    
    media_grupo = media(agrupadores)
    
    elements.append(Paragraph(f"<b>Grupo: {nome}</b>", styles['Heading2']))
    elements.append(Paragraph(f"Média Geral: {media_grupo:.1f}% ({classificacao(media_grupo)})", styles['Normal']))
    elements.append(Spacer(1, 10))

    for i, valor in enumerate(agrupadores):
        elements.append(Paragraph(f"Agrupador {i+1}: {valor}% ({classificacao(valor)})", styles['Normal']))
        elements.append(Paragraph(gerar_recomendacao(valor), styles['Normal']))
        elements.append(Spacer(1, 8))

    elements.append(Spacer(1, 20))

# =========================
# GERAR PDF
# =========================
doc.build(elements)