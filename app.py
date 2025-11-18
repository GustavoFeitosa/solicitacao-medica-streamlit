import streamlit as st
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
import io

# ===========================
# LISTA DE EXAMES LABORATORIAIS
# ===========================
exames_lab = [
    "Hemograma Completo",
    "Sódio, Potássio, Uréia, Creatinina, Ácido úrico",
    "15 OH Vitamina D3",
    "Cálcio iônico",
    "Colesterol total e frações",
    "Glicemia, Hb-glicada",
    "AST, ALT, CPK",
    "Ferritina",
    "NT-próBNP",
    "TSH, T4-livre",
    "Sumário de Urina",
    "Relação albumina/creatinina em amostra isolada de urina",
    "Lp(a)",
    "VHS",
    "PCR de alta sensibilidade"
]

# ===========================
# EXAMES DE IMAGEM
# ===========================
exames_imagem = [
    "Teste Ergométrico",
    "RX de tórax em PA e Perfil",
    "Ultrassom de Abdome Total",
    "Ecocardiograma Bidimensional com Doppler Colorido",
    "ECG de repouso",
    "Holter de 24 horas",
    "MAPA de 24 horas",
    "Cintilografia do miocárdio sob repouso e estresse físico",
    "Cintilografia do miocárdio sob repouso e estresse farmacológico",
    "AngioTC de coronárias",
    "TC de tórax para escore de cálcio coronariano",
    "Doppler arterial de membros inferiores",
    "Doppler venoso de membros inferiores",
    "US com Doppler de carótidas e vertebrais",
    "US de tireoide",
    "Endoscopia Digestiva Alta",
    "Colonoscopia"
]

# ===========================
# FUNÇÃO PARA CRIAR RECEITUÁRIO
# ===========================
def criar_receituario(paciente, cid, justificativa, lista_exames, titulo):

    doc = Document()

    # Cabeçalho
    h = doc.add_paragraph("CONSULTÓRIO CARDIOLÓGICO")
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h.runs[0].bold = True
    h.runs[0].font.size = Pt(14)

    n = doc.add_paragraph("Dr. Gustavo Feitosa – Cardiologista")
    n.alignment = WD_ALIGN_PARAGRAPH.CENTER
    n.runs[0].font.size = Pt(12)

    doc.add_paragraph("")

    # Título
    t = doc.add_paragraph(titulo)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t.runs[0].bold = True
    t.runs[0].font.size = Pt(14)

    doc.add_paragraph("")

    # Paciente
    p = doc.add_paragraph(f"Para Sr(a). {paciente}")
    p.runs[0].font.size = Pt(12)

    doc.add_paragraph("Solicito:\n").runs[0].font.size = Pt(12)

    # Lista de exames
    for ex in lista_exames:
        linha = doc.add_paragraph(f"• {ex}")
        linha.runs[0].font.size = Pt(12)

    # JUSTIFICATIVA – duas linhas acima do CID
    if justificativa.strip():
        doc.add_paragraph("\n")
        j = doc.add_paragraph(f"Justificativa: {justificativa}")
        j.runs[0].font.size = Pt(12)

    # CID – duas linhas acima da data
    doc.add_paragraph("\n")
    cid_par = doc.add_paragraph(f"CID 10: {cid}")
    cid_par.runs[0].font.size = Pt(12)

    # Data
    data = datetime.now().strftime("%d/%m/%Y")
    d = doc.add_paragraph(f"\nSalvador/BA, {data}")
    d.runs[0].font.size = Pt(12)

    # Assinatura
    assinatura = doc.add_paragraph("\n_______________________________")
    assinatura.runs[0].font.size = Pt(12)

    info = doc.add_paragraph(
        "Dr. Gustavo Feitosa – Cardiologista\nCRM/BA 21730 – RQE 21919"
    )
    info.runs[0].font.size = Pt(11)

    end1 = doc.add_paragraph(
        "Centro Médico Aliança, sala 211 – Av. Juracy Magalhães Júnior, 2096 – Salvador – BA"
    )
    end1.runs[0].font.size = Pt(10)

    end2 = doc.add_paragraph(
        "Centro Médico Cárdio Pulmonar, sala 501 – Rua Ponciano Oliveira, 157 – Salvador – BA"
    )
    end2.runs[0].font.size = Pt(10)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ===========================
# INTERFACE STREAMLIT
# ===========================
st.title("📄 Gerador de Solicitações Médicas – Dr. Gustavo Feitosa")

st.markdown("### Preencha os dados abaixo:")

paciente = st.text_input("Nome completo do paciente")
cid = st.text_input("CID (ex: I-10, I-25.1)")
justificativa = st.text_area("Justificativa (opcional)")

st.markdown("### 🧪 Selecione os exames laboratoriais")
selecionados_lab = st.multiselect("Exames laboratoriais", exames_lab)

st.markdown("### 🩻 Selecione os exames de imagem / complementares")
selecionados_img = st.multiselect("Exames de imagem / complementares", exames_imagem)

if st.button("Gerar Solicitações"):
    if paciente.strip() == "" or cid.strip() == "":
        st.error("Preencha nome e CID.")
    else:
        # Arquivo de laboratório
        if selecionados_lab:
            doc_lab = criar_receituario(
                paciente, cid, justificativa, selecionados_lab,
                "SOLICITAÇÃO DE EXAMES LABORATORIAIS"
            )
            st.download_button(
                label="📥 Baixar Solicitação Laboratorial",
                data=doc_lab,
                file_name="solicitacao_laboratorial.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        # Arquivos individuais de imagem
        for exame in selecionados_img:
            doc_img = criar_receituario(
                paciente, cid, justificativa, [exame],
                "SOLICITAÇÃO DE EXAME COMPLEMENTAR"
            )
            filename = exame.replace(" ", "_").replace("/", "_").lower() + ".docx"
            st.download_button(
                label=f"📥 Solicitação – {exame}",
                data=doc_img,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        st.success("Solicitações geradas com sucesso!")
