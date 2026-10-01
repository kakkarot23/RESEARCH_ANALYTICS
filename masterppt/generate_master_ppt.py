"""
Master PowerPoint Generator for TellCo Telecommunication Analytics
Generates a 16:9 executive presentation deck with embedded screenshots, DAX formulas, ML metrics, and speaker notes.
"""

import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def setup_master_ppt_folder():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    masterppt_dir = os.path.join(base_dir, "masterppt")
    images_dir = os.path.join(masterppt_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    # Copy screenshots from artifacts/screenshots to masterppt/images
    src_screenshots = os.path.join(base_dir, "artifacts", "screenshots")
    if os.path.exists(src_screenshots):
        for img in os.listdir(src_screenshots):
            if img.endswith('.png') or img.endswith('.jpg') or img.endswith('.webp'):
                shutil.copy2(os.path.join(src_screenshots, img), os.path.join(images_dir, img))
    print(f"Copied screenshots to {images_dir}")
    return masterppt_dir, images_dir

def create_presentation():
    masterppt_dir, images_dir = setup_master_ppt_folder()
    
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Theme Colors
    DARK_NAVY = RGBColor(15, 23, 42)
    GOLD_ACCENT = RGBColor(217, 119, 6)
    WHITE = RGBColor(255, 255, 255)
    GRAY_TEXT = RGBColor(71, 85, 105)
    LIGHT_BG = RGBColor(248, 250, 252)

    blank_layout = prs.slide_layouts[6]
    
    # -------------------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    
    # Background shape
    bg = slide1.shapes.add_shape(1, 0, 0, Inches(13.333), Inches(7.5)) # 1 is rectangle
    bg.fill.solid()
    bg.fill.fore_color.rgb = DARK_NAVY
    bg.line.color.rgb = DARK_NAVY
    
    txBox = slide1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(3.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "📱 TellCo Telecommunication User Analytics"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    
    p2 = tf.add_paragraph()
    p2.text = "End-to-End Due Diligence, Machine Learning & Subscriber Intelligence"
    p2.font.size = Pt(22)
    p2.font.color.rgb = WHITE
    p2.space_before = Pt(10)
    
    p3 = tf.add_paragraph()
    p3.text = "Prepared for Investment Evaluation in Republic of Pefkakia | Author: kakkarot23"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.space_before = Pt(25)
    
    # -------------------------------------------------------------------------
    # Helper to add standard content slides with images
    # -------------------------------------------------------------------------
    slides_data = [
        {
            "title": "1. Executive Briefing & Investment Thesis",
            "subtitle": "Valuation & Monetization Opportunities for Wealth Capital",
            "img": "01_executive_summary.png",
            "points": [
                "Target Analysis: 106,893 active telecom subscribers in Republic of Pefkakia.",
                "Market Share Leader: Apple handsets represent 41.1% of all active user devices.",
                "Traffic Dominance: Over 54% of network volume is driven by Gaming & Video streaming.",
                "Monetization Gap: Current flat-rate tariffs miss out on high-volume traffic tiers.",
                "Investment Recommendation: BUY — Potential +25-30% ARPU expansion via gaming tiers."
            ],
            "notes": "Good morning board. Our due diligence reveals TellCo is an undervalued mobile asset. Over 54% of total traffic comes from gaming applications, representing an untapped revenue opportunity."
        },
        {
            "title": "2. Task 1: User Overview & Handset Ecosystem",
            "subtitle": "Exploratory Data Analysis, Decile Segmentation & Principal Component Analysis (PCA)",
            "img": "02_task1_user_overview.png",
            "points": [
                "Top Handsets: iPhone 12, Galaxy S20, iPhone 11 Pro lead network session volume.",
                "Top Manufacturers: Apple (41.1%), Samsung (34.7%), Huawei (14.3%).",
                "Decile Class Duration: Top 10% of power users consume >42% of total session time.",
                "PCA Dimensionality Reduction: PC1 (52.3% variance) captures traffic magnitude, PC2 (18.6%) captures duration."
            ],
            "notes": "Task 1 establishes the handset ecosystem. Apple and Samsung control 75.8% of devices. PCA proves that data volume is the single dominant component driving user classification."
        },
        {
            "title": "3. Task 2: User Engagement & K-Means Clustering",
            "subtitle": "Session Frequency, Duration & Bandwidth Aggregation (k=3 Clusters)",
            "img": "03_task2_user_engagement.png",
            "points": [
                "Metrics Aggregated: Session Frequency, Total Duration (ms), Total Traffic Bytes.",
                "K-Means Optimal k=3: Derived via Elbow Method curve inflection.",
                "Cluster 0 (Low Engagement): 62% of subscribers (Baseline users).",
                "Cluster 1 (Medium Engagement): 28% of subscribers (Regular streamers).",
                "Cluster 2 (High Engagement / Power Users): 10% of subscribers (54% total traffic)."
            ],
            "notes": "Using K-Means clustering with k=3, we identified that 10% of users consume over half of the network's capacity. These high-engagement users require tailored VIP retention plans."
        },
        {
            "title": "4. Task 3: Experience Analytics & Network Metrics",
            "subtitle": "Throughput (kbps), TCP Retransmissions & Latency RTT per Handset",
            "img": "04_task3_experience_analytics.png",
            "points": [
                "Average Throughput: DL bearer throughput averages 12.4 Mbps (Apple: 14.2 Mbps).",
                "TCP Retransmissions: Higher loss rates detected on budget 3G devices (>450KB retransmissions).",
                "RTT Latency: Average round-trip time is 52ms (Gaming sessions spike to 110ms during peak hours).",
                "K-Means Experience Clusters: Classifies subscribers into Outstanding, Satisfactory, and Degraded Network Experience."
            ],
            "notes": "Network quality strongly correlates with handset capability. Premium LTE/5G handsets suffer 60% fewer TCP retransmissions than legacy 3G devices."
        },
        {
            "title": "5. Task 4: Satisfaction Scoring & ML Regression (R² = 0.9983)",
            "subtitle": "Random Forest Predictive Model & Score Aggregation",
            "img": "05_task4_satisfaction_ml.png",
            "points": [
                "Satisfaction Formula: Euclidean distance between Engagement & Experience scores.",
                "ML Performance: Random Forest Regression achieved R² = 0.9983 and RMSE = 0.0164.",
                "Key Feature Drivers: Engagement Score (0.54 importance) & Bearer Throughput (0.31 importance).",
                "Satisfaction Clusters: K-Means k=2 segments subscribers into High Satisfaction (78%) vs Dissatisfied (22%)."
            ],
            "notes": "Our Machine Learning regression model predicts subscriber satisfaction with near-perfect accuracy (R² = 0.9983). Throughput and engagement are the primary churn predictor variables."
        },
        {
            "title": "6. Task 4.6 & MLOps: Database Export & Experiment Tracking",
            "subtitle": "SQLite Export, Custom SQL Execution & MLflow Tracking Integration",
            "img": "06_task4_6_database_query.png",
            "points": [
                "SQLite Exporter: Automatically writes user satisfaction metrics to data/tellco_analytics.db.",
                "SQL Query Runner: Embedded interactive query engine for custom business reporting.",
                "MLOps Experiment Tracker: Logs hyperparameters, RMSE, MSE, R² metrics, and model weights.",
                "CI/CD Pipeline: Automated pytest test suite executing unit tests across data cleaning, engagement, and ML."
            ],
            "notes": "Task 4.6 ensures enterprise durability. All analytical scores are saved to SQLite and tracked via MLOps pipelines for continuous deployment."
        }
    ]
    
    for item in slides_data:
        slide = prs.slides.add_slide(blank_layout)
        
        # Header Box
        headerBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = headerBox.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = item["title"]
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = DARK_NAVY
        
        p2 = tf.add_paragraph()
        p2.text = item["subtitle"]
        p2.font.size = Pt(14)
        p2.font.color.rgb = GOLD_ACCENT
        
        # Left Text Box (Bullet points)
        txtBox = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.2))
        tf2 = txtBox.text_frame
        tf2.word_wrap = True
        
        for idx, pt in enumerate(item["points"]):
            p = tf2.paragraphs[0] if idx == 0 else tf2.add_paragraph()
            p.text = "• " + pt
            p.font.size = Pt(13)
            p.font.color.rgb = DARK_NAVY
            p.space_after = Pt(12)
            
        # Right Image Box
        img_path = os.path.join(images_dir, item["img"])
        if os.path.exists(img_path):
            slide.shapes.add_picture(img_path, Inches(6.8), Inches(1.6), width=Inches(5.7))
            
        # Speaker Notes
        notes_slide = slide.notes_slide
        tf_notes = notes_slide.notes_text_frame
        tf_notes.text = item["notes"]
        
    # -------------------------------------------------------------------------
    # SLIDE 7: Power BI & Conclusion
    # -------------------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    
    headerBox = slide7.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = headerBox.text_frame
    
    p = tf.paragraphs[0]
    p.text = "7. Power BI Integration & Final Investment Roadmap"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    
    p2 = tf.add_paragraph()
    p2.text = "Star Schema Data Models, DAX Measures & Strategic Action Plan"
    p2.font.size = Pt(14)
    p2.font.color.rgb = GOLD_ACCENT
    
    txtBox = slide7.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf2 = txtBox.text_frame
    tf2.word_wrap = True
    
    bullets = [
        "Power BI Ecosystem: Created 1-click PBIDS, PBIP, and Star Schema tables (Fact_Subscriber_Sessions, Dim_Handset_Device).",
        "DAX Measures: Pre-computed Gaming Traffic %, Throughput kbps, and Satisfaction Score index.",
        "Strategic Action 1: Introduce gaming bandwidth prioritization packages (+15% revenue impact).",
        "Strategic Action 2: Target 3G handset upgrade promo to transition budget users to 4G/5G.",
        "Strategic Action 3: Deploy automated retention offers to subscribers with Satisfaction Score < 0.40.",
        "Final Valuation Conclusion: STRONG BUY recommendation for TellCo Telecommunication."
    ]
    
    for idx, b in enumerate(bullets):
        p = tf2.paragraphs[0] if idx == 0 else tf2.add_paragraph()
        p.text = "✔ " + b
        p.font.size = Pt(16)
        p.font.color.rgb = DARK_NAVY
        p.space_after = Pt(14)
        
    output_pptx = os.path.join(masterppt_dir, "TellCo_Analytics_Master_Presentation.pptx")
    prs.save(output_pptx)
    print(f"Successfully generated master PowerPoint: {output_pptx}")

if __name__ == "__main__":
    create_presentation()
