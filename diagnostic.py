from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Flowable, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import re, json, html

def carregar_json(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)
    
data_json = carregar_json("data.json")
    
# =========================
# UTILIDADES
# =========================

# Converte pixel para pontos
def px_to_pt(px):
    return px * 0.75

# 👉 Converte cor HEX (CSS) → RGB (0 a 1)
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return (
        int(hex_color[0:2], 16) / 255,
        int(hex_color[2:4], 16) / 255,
        int(hex_color[4:6], 16) / 255,
    )

'''
👉 Faz transição suave entre duas cores
c1 = cor inicial
c2 = cor final
t = valor entre 0 e 1
'''
def interpolate_color(c1, c2, t):
    return (
        c1[0] + (c2[0] - c1[0]) * t,
        c1[1] + (c2[1] - c1[1]) * t,
        c1[2] + (c2[2] - c1[2]) * t,
    )

# =========================
# FUNÇÃO DE TEXTO COM (CORREÇÃO TOP-LEFT)
# =========================
def draw_text(
        pdf,
        x,
        y,
        text,
        size=12,
        font="Helvetica",
        weight=400,
        color=colors.black,
        align="left"
    ):
    pdf.saveState()

    pdf.translate(x, y)
    pdf.scale(1, -1)

    # =========================
    # 🎨 COR
    # =========================
    def parse_color(c):
        if isinstance(c, str) and c.startswith("#"):
            c = c.lstrip("#")
            r = int(c[0:2], 16) / 255
            g = int(c[2:4], 16) / 255
            b = int(c[4:6], 16) / 255
            return colors.Color(r, g, b)

        if isinstance(c, str):
            return getattr(colors, c, colors.black)

        if isinstance(c, tuple):
            if len(c) == 4:
                r, g, b, a = c
            else:
                r, g, b = c
                a = 1

            if max(r, g, b) > 1:
                r /= 255
                g /= 255
                b /= 255

            return colors.Color(r, g, b, alpha=a)

        return c

    pdf.setFillColor(parse_color(color))

    # =========================
    # 🔠 FONTE DINÂMICA
    # =========================
    def resolve_font(font_name, weight):
        """
        Tenta encontrar variações da fonte automaticamente:
        Ex:
        MinhaFonte → MinhaFonte-Bold
        """

        if weight >= 600:
            bold_name = f"{font_name}-Bold"

            if bold_name in pdfmetrics.getRegisteredFontNames():
                return bold_name

        return font_name

    font_name = resolve_font(font, weight)

    # valida se fonte existe
    if font_name not in pdfmetrics.getRegisteredFontNames():
        raise ValueError(f"Fonte '{font_name}' não registrada no ReportLab.")

    pdf.setFont(font_name, size)

    # =========================
    # 📐 ALINHAMENTO
    # =========================
    text_width = pdf.stringWidth(text, font_name, size)

    if align == "center":
        x_offset = -text_width / 2
    elif align == "right":
        x_offset = -text_width
    else:
        x_offset = 0

    # =========================
    # 🖊️ DESENHO
    # =========================
    pdf.drawString(x_offset, -size, text)

    pdf.restoreState()

'''
    # 👇 USO DO HELPER (CORRETO) - DA FUNÇÃO def draw_text()
    draw_text(pdf, 50, 80, "Texto padrão")
    draw_text(pdf, 50, 120, "Texto azul", color="#596CFF")
    draw_text(pdf, 50, 160, "Texto vermelho", color="red")
    draw_text(pdf, 50, 200, "RGB 255", color=(255, 0, 0))
    draw_text(pdf, 50, 240, "RGBA", color=(0, 0, 255, 0.5))
    draw_text(pdf, 50, 280, "Grande", size=22)
    draw_text(pdf, 50, 320, "Pequeno", size=8)
    draw_text(pdf, 50, 360, "Normal", weight=400)
    draw_text(pdf, 50, 400, "Negrito", weight=700)
    draw_text(pdf, 50, 360, "Normal", weight=400)
    draw_text(pdf, 50, 400, "Negrito", weight=700)
    draw_text(pdf, 300, 520, "Esquerda", align="left")
    draw_text(pdf, 300, 560, "Centralizado", align="center")
    draw_text(pdf,x=300,y=650,text="Diagnóstico de Riscos 1",size=20,font="Helvetica",weight=700,color="#596CFF",align="center")
    draw_text(pdf,x=300,y=675,text="Diagnóstico de Riscos 2",size=20,font="Helvetica",weight=700,color="#596CFF",align="center")
    draw_text(pdf,50,700,"Título Principal",size=24,weight=700,color="#1A1A1A")
    draw_text(pdf,50,740,"Subtítulo explicativo",size=14,color=(120, 120, 120))
    draw_text(pdf,x=400,y=780,text="Texto avançado RGBA + alinhado",size=16,font="Helvetica",weight=700,color=(255, 100, 50, 0.7),align="right")
'''

# =========================
# LOGO COMPANY
# =========================

def draw_logo_image(
        pdf,
        image_path,
        x=None,
        y=0,
        width=100,
        height=50,
        page_width=None,
        align="left"
    ):
    pdf.saveState()

    # =========================
    # SISTEMA TOP-LEFT (corrigir imagem)
    # =========================
    pdf.translate(0, 0)
    pdf.scale(1, -1)

    # =========================
    # LARGURA DA PÁGINA
    # =========================
    if page_width is None:
        page_width = pdf._pagesize[0]

    # =========================
    # 📐 LÓGICA DE ALINHAMENTO
    # =========================
    if x is None:
        if align == "center":
            x = (page_width - width) / 2
        elif align == "right":
            x = page_width - width
        else:  # left
            x = 0

    # =========================
    # 🖼️ DESENHO DA IMAGEM
    # =========================
    pdf.drawImage(
        image_path,
        x,
        -y - height,   # 👈 correção top-left
        width=width,
        height=height,
        mask='auto'
    )

    pdf.restoreState()

    '''
         # 👇 USO DO HELPER (CORRETO) - DA FUNÇÃO def draw_logo_image()
        draw_logo_image(pdf,"logo-edna-center.png",x=50,y=50,width=100,height=48)
        draw_logo_image(pdf,"logo-edna-center.png",x=None,y=150,width=100,height=48,align="left")
        draw_logo_image(pdf,"logo-edna-center.png",y=200,width=100,height=48,align="center")
        draw_logo_image(pdf,"logo-edna-center.png",y=250,width=100,height=48,align="right")
    '''


# =========================
# GRADIENTE
# =========================

def draw_css_gradient(pdf, width, height):
    steps = 300

    hex_colors = [
        "#c5dee9",
        "#d7e1f1",
        "#e9e5f3",
        "#f7e9f3",
        "#fafafa"
    ]

    rgb_colors = [hex_to_rgb(c) for c in hex_colors]
    segments = len(rgb_colors) - 1

    for i in range(steps):
        t_global = i / steps

        seg = min(int(t_global * segments), segments - 1)
        t_local = (t_global - seg / segments) * segments

        c1 = rgb_colors[seg]
        c2 = rgb_colors[seg + 1]

        r, g, b = interpolate_color(c1, c2, t_local)

        pdf.setFillColor(colors.Color(r, g, b))

        horizontal_position = (width / steps) * i
        pdf.rect(horizontal_position, 0, width / steps + 2, height, stroke=0, fill=1)

# =========================
# IMAGENS (AJUSTADAS PARA TOP-LEFT)
# =========================

def draw_images(pdf, width, height):
    scale_factor = 0.35

    # -------------------------Q
    # IMG 1 (top-right)
    # -------------------------
    img1_width = px_to_pt(883 * scale_factor)
    img1_height = px_to_pt(1175 * scale_factor)

    x1 = width - img1_width + px_to_pt(62)

    # 👇 AGORA top-left → não precisa inverter com height
    y1 = -px_to_pt(260)

    pdf.drawImage(
        "bg-img-1.png",
        x1,
        y1,
        width=img1_width,
        height=img1_height,

        mask='auto'
    )

    # -------------------------
    # IMG 2 (bottom-left)
    # -------------------------
    img2_width = px_to_pt(1598 * scale_factor)
    img2_height = px_to_pt(1825 * scale_factor)

    x2 = -px_to_pt(290)

    # 👇 agora Y cresce pra baixo
    y2 = height - img2_height + px_to_pt(380)

    pdf.drawImage(
        "bg-img-2.png",
        x2,
        y2,
        width=img2_width,
        height=img2_height,
        mask='auto'
    )

# =========================
# FUNÇÃO draw table
# =========================

def draw_table(pdf, data, x, y, table_width):

    num_cols = len(data[0])

    col_widths = [
        table_width * 0.30,
        table_width * 0.15,
        table_width * 0.15,
        table_width * 0.20,
        table_width * 0.20,
    ]

    if len(col_widths) != num_cols:
        col_widths = [table_width / num_cols] * num_cols

    table = Table(data, colWidths=col_widths)

    style = TableStyle([
        # =========================
        # HEADER
        # =========================
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#596CFF")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),

        # =========================
        # BODY
        # =========================
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),

        # =========================
        # ALINHAMENTO
        # =========================
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),

        # =========================
        # GRID
        # =========================
        ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor("#596CFF")),
    ])

    table.setStyle(style)

    table.wrapOn(pdf, 0, 0)
    table_height = table._height

    # 🔥 CORREÇÃO (NÃO REMOVER)
    pdf.saveState()

    pdf.scale(1, -1)
    pdf.translate(0, -pdf._pagesize[1])

    table.drawOn(pdf, x, pdf._pagesize[1] - y - table_height)

    pdf.restoreState()

    return table_height

# =========================
# FUNÇÃO DE DESENHAR A TABELA
# =========================

def montar_tabela_publico(json_data):
    table_data = [
        [
            "Grupo",
            "Total",
            "Respondidas",
            "Não Respondidas",
            "Aderência (%)"
        ]
    ]

    for report in json_data.get("reportData", []):
        for group in report.get("public_groups", []):

            group_name = group.get("groupName", "")

            people = group.get("peopleGroup", {})
            total = people.get("totalPeople", 0)
            answered = people.get("answered", 0)
            not_answered = people.get("notAnswered", 0)

            if total > 0:
                adherence = (answered / total) * 100
                adherence = f"{adherence:.2f}%"
            else:
                adherence = "0%"

            styles = getSampleStyleSheet()
            style_normal = styles["Normal"]

            table_data.append([
                Paragraph(str(group_name), style_normal),
                Paragraph(str(total), style_normal),
                Paragraph(str(answered), style_normal),
                Paragraph(str(not_answered), style_normal),
                Paragraph(str(adherence), style_normal),
            ])

    return table_data

# =========================
# FUNÇÃO CALCULO MEDIA GERAL DE ADERENCIA
# =========================

def calc_global_adherence_average(json_data):
    total_people_sum = 0
    total_answered_sum = 0

    for report in json_data.get("reportData", []):
        public_groups = report.get("public_groups", [])
        for group in public_groups:
            people = group.get("peopleGroup", {})
            total = people.get("totalPeople", 0)
            answered = people.get("answered", 0)
            total_people_sum += total
            total_answered_sum += answered

    if total_people_sum == 0:
        raise Exception("Erro: total de pessoas é zero.")

    global_adherence = (total_answered_sum / total_people_sum) * 100
    formated_adherence = f"Média geral da aderência de participação {global_adherence:.1f}%"
    return formated_adherence

# =========================
# FUNÇÃO CALCULO MEDIA GERAL DO DIAGNOSTICO
# =========================

def calc_global_diagnostic_average(json_data):
    total_avarage_sum = 0

    for report in json_data.get("reportData", []):
        public_groups = report.get("public_groups", [])
        quantity_groups = len(public_groups)
        for group in public_groups:
            people = group.get("peopleGroup", {})
            total_avarage_group = people.get("avarageGroup", 0)
            total_avarage_sum += total_avarage_group

    if quantity_groups < 0:
        raise Exception("Erro: total de GRUPOS é MENOR OU IGUAL a zero.")
    
    total_avarage_result = ((total_avarage_sum / quantity_groups) * 100)

    formated_total_avarage_result = f'{total_avarage_result:.1f}%'

    return total_avarage_result, formated_total_avarage_result 

# =========================
# FUNÇÃO CRIA CARD STATUS GERAL DO DIAGNOSTICO
# =========================

def draw_score_card(pdf, x, y, value, value_str):
    rect_width = 130
    rect_height = 80

    # lógica de cor
    if 0 <= value <= 20:
        bg = "#ee3650"
        label = "Muito Ruim"
    elif value <= 40:
        bg = "#f4b184"
        label = "Ruim"
    elif value <= 60:
        bg = "#ffd656"
        label = "Razoável"
    elif value <= 80:
        bg = "#c3dfa5"
        label = "Bom"
    elif value <= 100:
        bg = "#2f6e2d"
        label = "Excelente"
    else:
        bg = "#adadad"
        label = "n/d"

    # fundo
    pdf.setFillColor(colors.HexColor(bg))
    pdf.roundRect(x, y, rect_width, rect_height, 5, fill=1, stroke=0)

    # centro
    cx = x + rect_width / 2
    cy = y + ((rect_height / 2) - 10)

    # círculo
    pdf.setFillColor(colors.white)
    pdf.circle(cx, cy, 20, stroke=0, fill=1)

    # número
    draw_text(pdf, cx, cy - 7, value_str, size=11, weight=700, color=bg, align="center")

    # label
    draw_text(pdf, cx, cy + 25, label, size=11, weight=700, color="#FFFFFF", align="center")

# =========================
# FUNCAO LIMPAR HTML
# =========================

def limpar_html(html_content):
    if not html_content:
        return "<para></para>"

    # =========================
    # 1. Decodifica entidades HTML (&Aacute; → Á)
    # =========================
    html_content = html.unescape(html_content)

    # =========================
    # 2. Remove tags problemáticas
    # =========================
    html_content = re.sub(r'</?(div|span)[^>]*>', '', html_content)

    # =========================
    # 3. Remove atributos (style, class, etc)
    # =========================
    html_content = re.sub(r'<(\w+)[^>]*>', r'<\1>', html_content)

    # =========================
    # 4. Remove lixo do Word
    # =========================
    html_content = re.sub(r'mso-[^:]+:[^;"]+;?', '', html_content)

    # =========================
    # 5. REMOVE PARÁGRAFOS VAZIOS (ESSENCIAL)
    # =========================
    html_content = re.sub(r'<p>\s*</p>', '', html_content)
    html_content = re.sub(r'<p>\s*&nbsp;\s*</p>', '', html_content)

    # =========================
    # 6. Converte <p> → quebra controlada
    # =========================
    html_content = re.sub(r'</p>\s*<p>', '<br/><br/>', html_content)

    html_content = html_content.replace('<p>', '')
    html_content = html_content.replace('</p>', '')

    # =========================
    # 7. Normaliza múltiplas quebras (🔥 AQUI RESOLVE SEU PROBLEMA)
    # =========================
    html_content = re.sub(r'(<br/>\s*){3,}', '<br/><br/>', html_content)

    # =========================
    # 8. Limpa espaços
    # =========================
    html_content = html_content.replace('&nbsp;', ' ')
    html_content = re.sub(r'\s+', ' ', html_content)

    html_content = html_content.strip()

    # =========================
    # 9. GARANTE UM ÚNICO <para>
    # =========================
    return f"<para>{html_content}</para>"

# =========================
# DESENHAR PARAGRAFO
# =========================

def draw_paragraph(pdf, paragraph, x, y, max_width):
    w, h = paragraph.wrap(max_width, 1000)

    pdf.saveState()
    pdf.scale(1, -1)
    paragraph.drawOn(pdf, x, -(y + h))
    pdf.restoreState()

    return h  # útil pra layout dinâmico

# =========================
# FUNCAO BUSCA RECOMENDAÇÃO
# =========================

def get_recommendation_by_score(data_json, score, group_name=None):
    """
    Retorna a recomendação baseada no score.

    :param data_json: JSON completo
    :param score: valor numérico (ex: 12, 2.4, 50.5, 100)
    :param group_name: opcional (name do agrupador, ex: 'agrupador_1')
    :return: dict com recommendation, concept, start, end
    """

    data_recommendation = data_json.get("dataRecommendation", [])

    for group in data_recommendation:
        # 🔹 filtro opcional por agrupador
        if group_name and group.get("name") != group_name:
            continue

        meta = group.get("meta", {})
        rec_list = meta.get("recommendations", [])

        for rec in rec_list:
            start = rec.get("start")
            end = rec.get("end")

            # 🔥 comparação principal
            if start is not None and end is not None:
                if start <= score <= end:
                    return {
                        "recommendation": rec.get("recommendations"),
                        "concept": rec.get("concept"),
                        "start": start,
                        "end": end
                    }

    return None

# =========================
# EXECUÇÃO
# =========================

pdf = canvas.Canvas("Relatorio-Diagnostico.pdf", pagesize=A4)

width, height = A4

# 🔥 AQUI ESTÁ A MUDANÇA GLOBAL
pdf.translate(0, height)
pdf.scale(1, -1)

# =========================
# FUNDO
# =========================

draw_css_gradient(pdf, width, height)
draw_images(pdf, width, height)

# =======================================================================================
# "------------⬇️------ INICIO DO BLOCO PARA CONTEUDO DO RELATORIO ------⬇️------------"

'''
👉 Agora você trabalha como se fosse CSS:

(0,0) = topo esquerdo
X → direita
Y → baixo
'''

draw_logo_image(pdf,"logo-edna-center.png",y=20,width=100,height=48,align="center")
draw_text(pdf,x=20,y=80,text="Diagnóstico de Riscos Psicossociais",size=20,font="Helvetica",weight=700,color="#596CFF",align="left")
draw_text(pdf,x=20,y=110,text="Grupo Agulhas Negras - Agulhas Negras",size=7,font="Helvetica",weight=400,color="#344767",align="left")

rect_width = px_to_pt(302)
rect_height = px_to_pt(18)
radius = rect_height / 2

pdf.setFillColor(colors.HexColor("#596cff"))
pdf.roundRect(20,130,rect_width,rect_height,radius,fill=1,stroke=0)

draw_text(pdf,x=40,y=132,text="Respostas entre 11/03/2026 e 19/03/2026",size=7,font="Helvetica",weight=700,color="#ffffff",align="left")

rect_width_2 = 595.27
rect_height_2 = px_to_pt(36)
pdf.setFillColor(colors.HexColor("#e9ecef"))
pdf.roundRect(0,180,rect_width_2,rect_height_2,0,fill=1,stroke=0)

draw_text(pdf,x=20,y=186,text="Aderencia da participação",size=12,font="Helvetica",weight=700,color="#596CFF",align="left")

table_data = montar_tabela_publico(data_json)

draw_table(
    pdf,
    data=table_data,
    x=20,
    y=220,
    table_width=555
)

draw_text(pdf,x=20,y=340,text=calc_global_adherence_average(data_json),size=16,font="Helvetica",weight=700,color="#596CFF",align="left")

total_global_avarage_diagnostic = calc_global_diagnostic_average(data_json)
total_global_avarage_diagnostic_number = total_global_avarage_diagnostic[0]
total_global_avarage_diagnostic_str = total_global_avarage_diagnostic[1]

draw_score_card(pdf,x=233,y=400,value=total_global_avarage_diagnostic_number,value_str=total_global_avarage_diagnostic_str)
    
draw_text(pdf,x=20,y=520,text="1. ORGANIZAÇÃO DAS DEMANDAS",size=12,font="Helvetica",weight=700,color="#283BCC",align="left")

resultado = get_recommendation_by_score(
    data_json,
    total_global_avarage_diagnostic_number,
    group_name="agrupador_1"
)

# =========================
# TRATAMENTO SEGURO
# =========================

if resultado:
    final_recommendation = resultado["recommendation"]
else:
    final_recommendation = "<p>Sem recomendação disponível</p>"

# =========================
# PARAGRAPH CORRETO
# =========================

html_final = limpar_html(final_recommendation)

styles = getSampleStyleSheet()

p = Paragraph(html_final, styles['Normal'])

h = draw_paragraph(pdf, p, 20, 540, 555)



# "------------⬆️-------- FIM DO BLOCO PARA CONTEUDO DO RELATORIO -------⬆️------------"
# =======================================================================================

pdf.save()