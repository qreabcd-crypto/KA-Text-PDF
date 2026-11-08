import streamlit as st
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Streamlit Page Setup
st.set_page_config(page_title="Text to PDF Converter 🎨", page_icon="✨", layout="centered")

st.title("✨ 🎨 కలర్‌ఫుల్ Text to PDF కన్వర్టర్ 📄")
st.write("మీ టెక్స్ట్‌ని అందమైన హెడ్‌లైన్స్‌తో, ఎమోజీలతో, కలర్‌ఫుల్ బ్యాక్‌గ్రౌండ్‌తో PDF గా మార్చుకోండి!")

# Session State Setup
if "pdf_items" not in st.session_state:
    st.session_state.pdf_items = []

# Input Form
with st.container():
    headline = st.text_input("📌 హెడ్‌లైన్ / శీర్షిక:", placeholder="ఉదా: 🌟 Chapter 1: నా ప్రయాణం")
    text_content = st.text_area("📝 టెక్స్ట్ లేదా కంటెంట్:", placeholder="మీ కథ లేదా వివరాలు ఇక్కడ రాయండి...", height=150)

col1, col2 = st.columns(2)

with col1:
    if st.button("➕ PDF కి యాడ్ చేయండి", type="primary"):
        if headline.strip() or text_content.strip():
            st.session_state.pdf_items.append({
                "title": headline if headline else "Untitled Section",
                "body": text_content if text_content else ""
            })
            st.success("✅ సక్సెస్‌గా యాడ్ అయింది! ఇంకోటి కూడా రాయవచ్చు.")
        else:
            st.warning("⚠️ దయచేసి శీర్షిక లేదా టెక్స్ట్ నమోదు చేయండి.")

with col2:
    if st.button("🗑️ అన్నీ క్లియర్ చేయండి"):
        st.session_state.pdf_items = []
        st.rerun()

# Preview & Download Section
if st.session_state.pdf_items:
    st.markdown("---")
    st.subheader("📋 ప్రస్తుత PDF లోకి యాడ్ అయిన కంటెంట్:")
    
    for idx, item in enumerate(st.session_state.pdf_items):
        st.markdown(f"**{idx+1}. {item['title']}**")
        st.caption(item['body'][:120] + ("..." if len(item['body']) > 120 else ""))

    # Enhanced ReportLab Generator
    def create_colorful_pdf(items):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )
        story = []
        styles = getSampleStyleSheet()

        # Styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=colors.HexColor("#4A148C"), # Deep Purple
            spaceAfter=10,
            spaceBefore=14
        )

        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            textColor=colors.HexColor("#1A237E"), # Navy Dark
            leading=16,
            spaceAfter=12
        )

        # Colorful Background & Page Numbering
        def draw_decorations(canvas_obj, doc_obj):
            canvas_obj.saveState()
            
            # Pastel Colorful Background Gradient/Fill
            canvas_obj.setFillColor(colors.HexColor("#F3E5F5")) # Soft Lavender Pink Background
            canvas_obj.rect(0, 0, doc_obj.pagesize[0], doc_obj.pagesize[1], fill=1, stroke=0)
            
            # Double Border Design
            canvas_obj.setStrokeColor(colors.HexColor("#8E24AA"))
            canvas_obj.setLineWidth(2.5)
            canvas_obj.rect(15, 15, doc_obj.pagesize[0] - 30, doc_obj.pagesize[1] - 30)
            
            canvas_obj.setStrokeColor(colors.HexColor("#BA68C8"))
            canvas_obj.setLineWidth(1)
            canvas_obj.rect(20, 20, doc_obj.pagesize[0] - 40, doc_obj.pagesize[1] - 40)

            # Bottom Footer Page Numbering
            canvas_obj.setFont("Helvetica-Bold", 9)
            canvas_obj.setFillColor(colors.HexColor("#6A1B9A"))
            page_num = canvas_obj.getPageNumber()
            canvas_obj.drawRightString(doc_obj.pagesize[0] - 30, 25, f"Page {page_num}")
            
            canvas_obj.restoreState()

        for item in items:
            story.append(Paragraph(item['title'], title_style))
            formatted_text = item['body'].replace('\n', '<br/>')
            story.append(Paragraph(formatted_text, body_style))
            story.append(Spacer(1, 10))

        doc.build(story, onFirstPage=draw_decorations, onLaterPages=draw_decorations)
        buffer.seek(0)
        return buffer

    st.markdown("---")
    pdf_data = create_colorful_pdf(st.session_state.pdf_items)
    
    st.download_button(
        label="📥 అందమైన PDF ని డౌన్‌లోడ్ చేసుకోండి (Download PDF)",
        data=pdf_data,
        file_name="colorful_text_document.pdf",
        mime="application/pdf",
        type="primary"
    )
    
