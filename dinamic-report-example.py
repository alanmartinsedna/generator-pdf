from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Table, TableStyle, Spacer
)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

# print("⬆️ ⬅️ ➡️ ⬇️")

'''
    ➡️ Importa os componentes principais do motor de layout (Platypus):

    BaseDocTemplate → estrutura base do documento (nível avançado)
    Frame → área onde o conteúdo vai ser renderizado
    PageTemplate → define o “modelo da página”
    Paragraph → texto com estilo
    Table → tabela
    TableStyle → estilo da tabela

    from reportlab.lib.pagesizes import A4
    ➡️ Define o tamanho da página (A4)

    A4[0] = largura
    A4[1] = altura

    - from reportlab.lib import colors
    ➡️ Cores prontas (cinza, preto, branco, etc.)

    - from reportlab.lib.styles import getSampleStyleSheet
    ➡️ Traz estilos prontos:

    Title
    Normal
    Heading
'''

# =========================
# HEADER E FOOTER
# ========================= 

def header_footer(canvas, doc):
    '''
        ➡️ Função chamada em TODAS as páginas

        canvas → onde desenha
        doc → contexto (ex: número da página)

        canvas.saveState()
        ➡️ Salva o estado atual do canvas
        (boa prática pra não “vazar” configurações)
    '''
    canvas.saveState()

    # HEADER
    # Define tamanho de fonte
    canvas.setFont("Helvetica-Bold", 10)
    # Desenha o titulo
    canvas.drawString(2 * cm, A4[1] - 2 * cm, "Relatório de Exemplo")

    # linha abaixo do header
    canvas.line(2 * cm, A4[1] - 2.2 * cm, A4[0] - 2 * cm, A4[1] - 2.2 * cm)

    # FOOTER
    canvas.setFont("Helvetica", 9)
    page_number_text = f"Página {doc.page}"
    canvas.drawRightString(A4[0] - 2 * cm, 1.5 * cm, page_number_text)

    canvas.restoreState()


# =========================
# DOCUMENTO BASE
# =========================
'''
    ➡️ Cria o documento PDF

    nome do arquivo
    tamanho da página

    📌 Aqui você está usando modo avançado (não SimpleDocTemplate)
'''

doc = BaseDocTemplate("relatorio_profissional.pdf", pagesize=A4)

# =========================
# FRAME (ÁREA DO CONTEÚDO)
# =========================

'''
    ➡️ Define a área onde o conteúdo vai fluir
'''

frame = Frame(
    x1=2 * cm, # ➡️ margem esquerda
    y1=2.5 * cm, # ➡️ margem inferior (começo do frame)
    width=A4[0] - 4 * cm, # ➡️ largura total - margens esquerda/direita
    height=A4[1] - 5 * cm,  # ➡️ altura total - espaço de header + footer
    id="normal" # ➡️ identificador do frame (útil em layouts complexos)
)

# =========================
# TEMPLATE DA PÁGINA
# =========================
'''
    ➡️ Define como a página funciona
    id = ➡️ nome do template
    frames=[frame] = ➡️ diz qual área será usada para conteúdo
    onPage=header_footer = ➡️ “toda vez que uma página for criada, executa isso”
    doc.addPageTemplates([template]) = ➡️ registra o template no documento
'''
template = PageTemplate(
    id="template_principal",
    frames=[frame],
    onPage=header_footer
)

doc.addPageTemplates([template])

# =========================
# ESTILOS
# =========================
'''
    ➡️ carrega estilos prontos
'''

styles = getSampleStyleSheet()

# =========================
# CONTEÚDO DINÂMICO
# =========================
'''
    elements = [] = 📦 CONTEÚDO DINÂMICO
    ➡️ lista de elementos que serão renderizados
'''
elements = []

# Título
elements.append(Paragraph("Relatório Dinâmico", styles["Title"]))
elements.append(Spacer(1, 12))

# Texto longo
'''
    loop for = ➡️ simula conteúdo vindo do backend
    Paragraph = ➡️ adiciona parágrafo
    Spacer = ➡️ espaço abaixo do título
'''
for i in range(5):
    elements.append(Paragraph(
        "Este é um exemplo de parágrafo dinâmico que será repetido várias vezes "
        "para demonstrar quebra automática de página no ReportLab.",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 10)) 

# =========================
# TABELA GRANDE (DINÂMICA)
# =========================
'''
    ➡️ cabeçalho da tabela
'''
data = [["Nome Completo do usuário", "Idade", "Cidade onde reside"]]
'''
    loop for = ➡️ simula dados do backend
    data.append = ➡️ adiciona linha
'''

for i in range(50):  # simula dados do backend
    data.append([f"Pessoa {i}", str(20 + i), "Cidade XYZ"])
'''
    table ➡️ cria tabela
'''
table = Table(data, repeatRows=1)
'''
    table.style = ➡️ aplica estilo
    ("BACKGROUND", (0, 0), (-1, 0), colors.grey), ➡️ fundo do cabeçalho
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ➡️ texto branco no cabeçalho
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black), ➡️ bordas da tabela
'''
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
]))
'''
    ➡️ adiciona tabela ao fluxo
'''
elements.append(table)

# =========================
# BUILD DO PDF
# =========================
'''
    Fluxo interno:

    - pega cada elemento
    - joga no Frame
    - calcula altura (wrap)
    - desenha (draw)
    - verifica se cabe
    - quebra página se necessário
    - chama header_footer em cada página

    💡💡 O insight mais importante 💡💡

    ➡️ Você não posiciona elementos manualmente
    ➡️ Você só empilha eles:
    ➡️ ponto chave elements.append(...)
    ➡️ O ReportLab:
    ➡️ calcula posição
    ➡️ controla quebra
    ➡️ renderiza
'''

doc.build(elements)