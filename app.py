import streamlit as st
from seo_analyzer import analyze_website
from ai_suggestions import generate_suggestions, generate_title_ideas, generate_meta_ideas
from report_generator import generate_csv_report, generate_pdf_report

st.set_page_config(page_title="SEO Tool V2", layout="wide")

st.title("🚀 Advanced SEO Analyzer Tool")
st.write("Analyze any website SEO instantly in Chrome")

url = st.text_input("Enter Website URL")

if st.button("Analyze SEO"):
    if url:
        data = analyze_website(url)

        if "error" in data:
            st.error(data["error"])
        else:
            st.success("Analysis Complete")

            # SEO Score
            st.subheader("📊 SEO Score")
            st.metric("Score", f"{data['seo_score']}/100")

            # Basic Info
            col1, col2, col3 = st.columns(3)

            col1.metric("Title", data.get("title", ""))
            col2.metric("Meta Description", data.get("meta_description", ""))
            col3.metric("Word Count", data.get("word_count", 0))

            # Headings
            st.subheader("📌 Headings")
            st.write(f"H1: {data['h1_count']}")
            st.write(f"H2: {data['h2_count']}")
            st.write(f"H3: {data['h3_count']}")

            # Links
            st.subheader("🔗 Links Analysis")
            st.write(f"Total Links: {data['total_links']}")
            st.write(f"Internal Links: {data['internal_links']}")
            st.write(f"External Links: {data['external_links']}")
            st.write(f"Broken Links: {data['broken_links']}")

            # Images
            st.subheader("🖼 Images")
            st.write(f"Total Images: {data['total_images']}")
            st.write(f"Missing ALT Text: {data['missing_alt']}")

            # SEO Suggestions
            st.subheader("💡 SEO Suggestions")
            suggestions = generate_suggestions(data)
            for s in suggestions:
                st.write("-", s)

            # AI Ideas
            st.subheader("✨ SEO Title Ideas")
            for t in generate_title_ideas(url):
                st.write("-", t)

            st.subheader("✨ Meta Description Ideas")
            for m in generate_meta_ideas(url):
                st.write("-", m)

            # Reports
            st.subheader("📥 Download Report")

            csv_file = generate_csv_report(data)
            pdf_file = generate_pdf_report(data)

            with open(csv_file, "rb") as f:
                st.download_button("Download CSV", f, file_name="seo_report.csv")

            with open(pdf_file, "rb") as f:
                st.download_button("Download PDF", f, file_name="seo_report.pdf")
    else:
        st.warning("Please enter a URL")
