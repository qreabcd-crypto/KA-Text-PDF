import streamlit as st
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Page Setup
st.set_page_config(page_title="PDF Creator & Editor", page_icon="💖", layout="centered")

st.title("💖 లవ్ లెటర్ & డాక్యుమెంట్ PDF ఎడిటర్")
st.write("మీ టెక్స్ట్ ఎడిట్ చేసుకోవడానికి మరియు సురక్షితమైన డిలీట్ ఆప్షన్‌తో కూడిన PDF మేకర్.")

# Session State
if "pdf_items" not in st.session_state:
    st.session_state.pdf_items = []

# Background Theme Selector
theme_choice = st.selectbox(
    "🎨 PDF బ్యాక్‌గ్రౌండ్ కలర్ థీమ్ ఎంచుకోండి:",
    ["సాఫ్ట్ పింక్ (Soft Pink - Love Theme)", "క్రీమ్ / పీచ్ (Cream & Peach)", "లైట్ ల్యావెండర్ (Light Lavender)"]
)

theme_colors = {
    "సాఫ్ట్ పింక్ (Soft Pink - Love Theme)": {"bg": "#FCE4EC", "border": "#880E4F", "title": "#C2185B", "body": "#3E2723"},
    "క్రీమ్ / పీచ్ (Cream & Peach)": {"bg": "#FFF3E0", "border": "#E65100", "title": "#D84315", "body": "#212121"},
    "లైట్ ల్యావెండర్ (Light Lavender)": {"bg": "#F3E5F5", "border": "#8E24AA", "title": "#4A148C", "body": "#1A237E"}
}

current_theme = theme_colors[theme_choice]

# Input Section
st.markdown("---")
st.subheader("✍️ కొత్త కంటెంట్ యాడ్ చేయండి")
title_input = st.text_input("📌 హెడ్‌లైన్ / టైటిల్:", placeholder="ఉదా: 1. నా ప్రియమైన ప్రేమకి (To My Dearest Love)")
matter_input = st.text_area("📝 మ్యాటర్ / టెక్స్ట్:", placeholder="మీ టెక్స్ట్ ఇక్కడ రాయండి...", height=130)

col1, col2 = st.columns(2)
with col1:
    if st.button("➕ లిస్ట్‌కి యాడ్ చేయండి", type="primary"):
        if title_input.strip() or matter_input.strip():
            st.session_state.pdf_items.append({
                "title": title_input if title_input else "Untitled",
                "matter": matter_input if matter_input else ""
            })
            st.success("✅ విజయవంతంగా యాడ్ అయింది!")
        else:
            st.warning("⚠️ దయచేసి టైటిల్ లేదా మ్యాటర్ రాయండి.")

with col2:
    if st.button("🗑️ అన్నీ క్లియర్ చేయండి"):
        st.session_state.pdf_items = []
        st.rerun()

# Displaying items with Safe Delete & Edit options
if st.session_state.pdf_items:
    st.markdown("---")
    st.subheader("📋 ప్రస్తుత డాక్యుమెంట్ లిస్ట్ (ఎడిట్ / సేఫ్ డిలీట్):")
    
    for i, item in enumerate(st.session_state.pdf_items):
        with st.expander(f"సెక్షన్ {i+1}: {item['title']}"):
            new_title = st.text_input(f"టైటిల్ మార్చుకోండి {i}", value=item['title'], key=f"title_{i}")
            new_matter = st.text_area(f"మ్యాటర్ మార్చుకోండి {i}", value=item['matter'], key=f"matter_{i}")
            
            # Update Button
            if st.button("💾 వివరాలు అప్‌డేట్ చేయి", key=f"upd_{i}"):
                st.session_state.pdf_items[i] = {"title": new_title, "matter": new_matter}
                st.success("అప్‌డేట్ అయింది!")
                st.rerun()

            st.markdown("---")
            # Safe Delete Mechanism (Delete ఆప్షన్‌లోకి వెళ్తే తప్ప పోదు)
            if f"confirm_del_{i}" not in st.session_state:
                st.session_state[f"confirm_del_{i}"] = False

            if not st.session_state[f"confirm_del_{i}"]:
                if st.button("🗑️ డిలీట్ చేయి (Delete)", key=f"init_del_{i}"):
                    st.session_state[f"confirm_del_{i}"] = True
                    st.rerun()
            else:
                st.warning("⚠️ మీరు దీన్ని నిజంగా డిలీట్ చేయాలనుకుంటున్నారా?")
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("✔ అవును, పర్మినెంట్ డిలీట్", key=f"yes_del_{i}"):
                        st.session_state.pdf_items.pop(i)
                        del st.session_state[f"confirm_del_{i}"]
                        st.success("విజయవంతంగా తొలగించబడింది!")
                        st.rerun()
                with col_no:
                    if st.button("✖ వద్దు (Cancel)", key=f"no_del_{i}"):
                        st.session_state[f"confirm_del_{i}"] = False
                        st.rerun()

    # PDF Generation Function
    def generate_final_pdf(items, theme):
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

        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=15,
            textColor=colors.HexColor(theme["title"]),
            spaceAfter=6,
            spaceBefore=10
        )

        matter_style = ParagraphStyle(
            'CustomMatter',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            textColor=colors.HexColor(theme["body"]),
            leading=16,
            spaceAfter=12
        )

        def draw_page_decorations(canvas_obj, doc_obj):
            canvas_obj.saveState()
            canvas_obj.setFillColor(colors.HexColor(theme["bg"]))
            canvas_obj.rect(0, 0, doc_obj.pagesize[0], doc_obj.pagesize[1], fill=1, stroke=0)
            
            canvas_obj.setStrokeColor(colors.HexColor(theme["border"]))
            canvas_obj.setLineWidth(2)
            canvas_obj.rect(20, 20, doc_obj.pagesize[0] - 40, doc_obj.pagesize[1] - 40)
            
            canvas_obj.setLineWidth(0.8)
            canvas_obj.rect(25, 25, doc_obj.pagesize[0] - 50, doc_obj.pagesize[1] - 50)

            canvas_obj.setFont("Helvetica-Bold", 9)
            canvas_obj.setFillColor(colors.HexColor(theme["border"]))
            page_num = canvas_obj.getPageNumber()
            canvas_obj.drawRightString(doc_obj.pagesize[0] - 35, 30, f"Page {page_num}")
            
            canvas_obj.restoreState()

        # Top Header title
        top_heading = Paragraph("<b>ప్రేమలేఖ ♥</b><br/><font size=9 color='#666666'>నా హృదయపూర్వకమైన అనురాగంతో...</font>", title_style)
        story.append(top_heading)
        story.append(Spacer(1, 10))

        for item in items:
            story.append(Paragraph(item['title'], title_style))
            formatted_matter = item['matter'].replace('\n', '<br/>')
            story.append(Paragraph(formatted_matter, matter_style))
            story.append(Spacer(1, 5))

        # Bottom Signature
        footer_style = ParagraphStyle(
            'FooterSig',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=colors.HexColor(theme["title"]),
            alignment=2
        )
        story.append(Spacer(1, 15))
        story.append(Paragraph("సదా నీ ప్రేమతో... ♥<br/><b>శివాజీ</b>", footer_style))

        doc.build(story, onFirstPage=draw_page_decorations, onLaterPages=draw_page_decorations)
        buffer.seek(0)
        return buffer

    st.markdown("---")
    pdf_data = generate_final_pdf(st.session_state.pdf_items, current_theme)
    
    st.download_button(
        label="📥 మీ అందమైన PDF ని డౌన్‌లోడ్ చేసుకోండి",
        data=pdf_data,
        file_name="love_letter_document.pdf",
        mime="application/pdf",
        type="primary"
    )
    
