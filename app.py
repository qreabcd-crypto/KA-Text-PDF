import streamlit as st
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Streamlit Page Setup
st.set_page_config(page_title="Text to PDF Converter", page_icon="📄", layout="centered")

st.title("📄 కలర్‌ఫుల్ Text to PDF కన్వర్టర్")
st.write("మీ టెక్స్ట్‌ని హెడ్‌లైన్స్‌తో, కలర్‌ఫుల్ బ్యాక్‌గ్రౌండ్‌తో అందమైన PDFగా మార్చుకోండి.")

# Session state లో కంటెంట్‌ని సేవ్ చేయడానికి
if "pdf_items" not in st.session_state:
    st.session_state.pdf_items = []

# యూజర్ ఇన్పుట్ ఫీల్డ్స్
headline = st.text_input("హెడ్‌లైన్ / శీర్షిక:", placeholder="ఉదా: అధ్యాయం 1 / Chapter 1")
text_content = st.text_area("టెక్స్ట్ లేదా కంటెంట్:", placeholder="మీ సమాచారం ఇక్కడ రాయండి...", height=150)

col1, col2 = st.columns(2)

with col1:
    if st.button("➕ PDF కి యాడ్ చేయండి", type="primary"):
        if headline.strip() or text_content.strip():
            st.session_state.pdf_items.append({
                "title": headline if headline else "Untitled",
                "body": text_content if text_content else ""
            })
            st.success("యాడ్ అయింది! కావాలంటే ఇంకో సెక్షన్ కూడా రాయవచ్చు.")
        else:
            st.warning("దయచేసి హెడ్‌లైన్ లేదా టెక్స్ట్ నమోదు చేయండి.")

with col2:
    if st.button("🗑️ అన్నీ క్లియర్ చేయండి"):
        st.session_state.pdf_items = []
        st.rerun()

# యాడ్ చేసిన సెక్షన్ల ప్రివ్యూ
if st.session_state.pdf_items:
    st.markdown("---")
    st.subheader("📋 ప్రస్తుత PDF లోకి యాడ్ అయిన కంటెంట్:")
    for idx, item in enumerate(st.session_state.pdf_items):
        st.markdown(f"**{idx+1}. {item['title']}**")
        st.caption(item['body'][:100] + ("..." if len(item['body']) > 100 else ""))

    # ReportLab PDF జనరేటర్ ఫంక్షన్
    def create_colorful_pdf(items):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        story = []
        styles = getSampleStyleSheet()

        # కస్టమ్ హెడ్‌లైన్ & బాడీ స్టైల్స్
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=colors.HexColor("#1A237E"),
            spaceAfter=8,
            spaceBefore=12
        )

        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            textColor=colors.HexColor("#2C3E50"),
            leading=16,
            spaceAfter=12
        )

        # బ్యాక్‌గ్రౌండ్ మరియు బోర్డర్ డిజైన్
        def draw_background(canvas, doc_obj):
            canvas.saveState()
            # లైట్ క్రీమ్ / ఆకర్షణీయమైన బ్యాక్‌గ్రౌండ్ కలర్
            canvas.setFillColor(colors.HexColor("#FFF8E7"))
            canvas.rect(0, 0, doc_obj.pagesize[0], doc_obj.pagesize[1], fill=1, stroke=0)
            
            # స్టైలిష్ మార్జిన్ బోర్డర్
            canvas.setStrokeColor(colors.HexColor("#8E24AA"))
            canvas.setLineWidth(2)
            canvas.rect(18, 18, doc_obj.pagesize[0] - 36, doc_obj.pagesize[1] - 36)
            canvas.restoreState()

        for item in items:
            story.append(Paragraph(item['title'], title_style))
            # న్యూలైన్స్ ని HTML break గా మార్చడం
            formatted_text = item['body'].replace('\n', '<br/>')
            story.append(Paragraph(formatted_text, body_style))
            story.append(Spacer(1, 10))

        doc.build(story, onFirstPage=draw_background, onLaterPages=draw_background)
        buffer.seek(0)
        return buffer

    st.markdown("---")
    pdf_data = create_colorful_pdf(st.session_state.pdf_items)
    
    # PDF డౌన్‌లోడ్ బటన్
    st.download_button(
        label="📥 PDF ఫైల్‌ని డౌన్‌లోడ్ చేసుకోండి",
        data=pdf_data,
        file_name="colorful_text_document.pdf",
        mime="application/pdf",
        type="primary"
    )
    
