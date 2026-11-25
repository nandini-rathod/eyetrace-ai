import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck(filename="ASD_EyeTracking_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Color Palette
    DARK_NAVY = RGBColor(11, 25, 56)       # Exact title bg from user image
    NAVY_CARD = RGBColor(17, 34, 72)       # Elevated dark card
    CYAN_ACCENT = RGBColor(0, 168, 204)    # Exact vibrant cyan from user image
    LIGHT_CYAN = RGBColor(56, 189, 248)    # Sky cyan
    WHITE = RGBColor(255, 255, 255)
    OFF_WHITE = RGBColor(241, 245, 249)    # Slate 100
    LIGHT_BG = RGBColor(248, 250, 252)     # Slate 50 content background
    CARD_BG = RGBColor(255, 255, 255)      # Pure white card
    CARD_BORDER = RGBColor(226, 232, 240)  # Slate 200 border
    TEXT_DARK = RGBColor(15, 23, 42)       # Slate 900
    TEXT_MUTED = RGBColor(100, 116, 139)   # Slate 500
    TEXT_LIGHT_MUTED = RGBColor(203, 213, 225) # Slate 300
    BLUE_PRIMARY = RGBColor(37, 99, 235)   # Blue 600
    SUCCESS_COLOR = RGBColor(16, 185, 129) # Emerald 500
    ROSE_ALERT = RGBColor(244, 63, 94)     # Rose 500

    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", "static")

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER, corner_radius=None):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()
        return shape

    def add_header(slide, title_text, category="EYE-TRACKING RESEARCH & MACHINE LEARNING"):
        # Header category tracker
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(10.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = BLUE_PRIMARY
        p_cat.font.name = "Arial"

        # Main slide title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.5), Inches(0.65))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_DARK
        p_t.font.name = "Arial"

        # Subtle divider line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(226, 232, 240)
        line.line.fill.background()

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Exact Replica of User's Uploaded Cover Slide)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_NAVY
    bg1.line.fill.background()

    # Title & Subtitle box (Centered vertically & horizontally in upper half)
    tb_title = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(2.2))
    tf1 = tb_title.text_frame
    tf1.word_wrap = True

    p1 = tf1.paragraphs[0]
    p1.text = "Autism Spectrum Disorder (ASD)"
    p1.font.size = Pt(38)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.font.name = "Georgia"
    p1.alignment = PP_ALIGN.CENTER
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "Prediction using Deep Learning"
    p2.font.size = Pt(30)
    p2.font.bold = True
    p2.font.color.rgb = CYAN_ACCENT
    p2.font.name = "Georgia"
    p2.alignment = PP_ALIGN.CENTER
    p2.space_after = Pt(6)

    p3 = tf1.add_paragraph()
    p3.text = "& Feature Reduction"
    p3.font.size = Pt(26)
    p3.font.bold = False
    p3.font.color.rgb = WHITE
    p3.font.name = "Georgia"
    p3.alignment = PP_ALIGN.CENTER

    # Team Members Block
    tb_team = slide1.shapes.add_textbox(Inches(2.5), Inches(4.5), Inches(8.333), Inches(1.4))
    tf_team = tb_team.text_frame
    tf_team.word_wrap = True

    p_tm_header = tf_team.paragraphs[0]
    p_tm_header.text = "Team Members: "
    p_tm_header.font.size = Pt(15)
    p_tm_header.font.bold = True
    p_tm_header.font.color.rgb = CYAN_ACCENT
    p_tm_header.font.name = "Arial"
    p_tm_header.alignment = PP_ALIGN.CENTER

    # Add member details
    members = [
        ("Pranav Priy", "2023UGCS046"),
        ("Tanisha Jain", "2023UGCS122"),
        ("Rathod Nandini", "2023UGCS079")
    ]
    for name, roll in members:
        pm = tf_team.add_paragraph()
        pm.text = f"{name}   {roll}"
        pm.font.size = Pt(14)
        pm.font.color.rgb = WHITE
        pm.font.name = "Arial"
        pm.alignment = PP_ALIGN.CENTER
        pm.space_after = Pt(2)

    # Supervisor Block
    tb_sup = slide1.shapes.add_textbox(Inches(2.5), Inches(6.2), Inches(8.333), Inches(0.8))
    tf_sup = tb_sup.text_frame
    tf_sup.word_wrap = True

    p_sup = tf_sup.paragraphs[0]
    p_sup.text = "Supervisor:   Dr. Nidhi Kushwaha"
    p_sup.font.size = Pt(15)
    p_sup.font.bold = True
    p_sup.font.color.rgb = CYAN_ACCENT
    p_sup.font.name = "Arial"
    p_sup.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: Problem Statement & Clinical Motivation
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Clinical Motivation & The Autism Diagnostic Crisis", category="01. INTRODUCTION & PROBLEM STATEMENT")

    # Left Column: The Problem (Challenges)
    card_w = Inches(5.7)
    add_card(slide2, Inches(0.8), Inches(1.6), card_w, Inches(5.4), bg_color=WHITE, border_color=CARD_BORDER)
    tb_prob = slide2.shapes.add_textbox(Inches(1.0), Inches(1.8), card_w - Inches(0.4), Inches(5.0))
    tf_p = tb_prob.text_frame
    tf_p.word_wrap = True

    p_ph = tf_p.paragraphs[0]
    p_ph.text = "CURRENT DIAGNOSTIC BOTTLENECKS"
    p_ph.font.size = Pt(11)
    p_ph.font.bold = True
    p_ph.font.color.rgb = ROSE_ALERT
    p_ph.space_after = Pt(12)

    challenges = [
        ("Delayed Clinical Diagnosis (Ages 4–5)",
         "Autism Spectrum Disorder (ASD) can be detected as early as 18–24 months, yet average diagnosis occurs at 4–5 years, missing the prime neurodevelopmental therapy window."),
        ("Specialist Scarcity & High Waitlists",
         "Gold-standard assessments (ADOS-2, ADI-R) require extensive clinical sessions by rare pediatric specialists, causing months-long waitlists."),
        ("Subjective & Stressful Evaluations",
         "Questionnaire-based exams rely on parental memory and subjective clinician observations, causing diagnostic variance and high child anxiety.")
    ]
    for ch_title, ch_desc in challenges:
        pt = tf_p.add_paragraph()
        pt.text = "• " + ch_title
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = TEXT_DARK
        pd = tf_p.add_paragraph()
        pd.text = "   " + ch_desc
        pd.font.size = Pt(11)
        pd.font.color.rgb = TEXT_MUTED
        pd.space_after = Pt(10)

    # Right Column: The Proposed Eye-Tracking Solution
    add_card(slide2, Inches(6.8), Inches(1.6), card_w, Inches(5.4), bg_color=LIGHT_BG, border_color=BLUE_PRIMARY)
    tb_sol = slide2.shapes.add_textbox(Inches(7.0), Inches(1.8), card_w - Inches(0.4), Inches(5.0))
    tf_s = tb_sol.text_frame
    tf_s.word_wrap = True

    p_sh = tf_s.paragraphs[0]
    p_sh.text = "OUR OBJECTIVE: DIGITAL EYE-TRACKING BIOMARKER"
    p_sh.font.size = Pt(11)
    p_sh.font.bold = True
    p_sh.font.color.rgb = BLUE_PRIMARY
    p_sh.space_after = Pt(12)

    solutions = [
        ("Objective Visual Attention Tracing",
         "Eye-tracking captures gaze fixations and saccades during social scene viewing. Individuals with ASD exhibit distinct non-social visual exploration patterns."),
        ("Automated Deep Learning & Feature Reduction",
         "Apply transfer learning (MobileNet) and PCA feature reduction to accurately distinguish ASD vs. Non-ASD scanpaths with zero human subjectivity."),
        ("Clinical Transparency & Explainability",
         "Provide visual attribution heatmaps (Occlusion Sensitivity) and kinematic channel ablation to give clinicians explainable evidence, not black-box scores.")
    ]
    for s_title, s_desc in solutions:
        st = tf_s.add_paragraph()
        st.text = "✔ " + s_title
        st.font.size = Pt(13)
        st.font.bold = True
        st.font.color.rgb = TEXT_DARK
        sd = tf_s.add_paragraph()
        sd.text = "   " + s_desc
        sd.font.size = Pt(11)
        sd.font.color.rgb = TEXT_MUTED
        sd.space_after = Pt(10)

    # =========================================================================
    # SLIDE 3: Dataset Description & Preprocessing Pipeline
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Dataset Description & Input Preprocessing", category="02. DATA ENGINEERING")

    # Left Card: Dataset metrics
    add_card(slide3, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.4))
    tb_d = slide3.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.1), Inches(5.0))
    tf_ds = tb_d.text_frame
    tf_ds.word_wrap = True

    p_dh = tf_ds.paragraphs[0]
    p_dh.text = "ETSDS DATASET CHARACTERISTICS"
    p_dh.font.size = Pt(11)
    p_dh.font.bold = True
    p_dh.font.color.rgb = BLUE_PRIMARY
    p_dh.space_after = Pt(8)

    d_info = [
        ("Source Modality", "Eye-tracking scanpaths recorded during visual stimulus presentation."),
        ("Total Raw Samples", "547 scanpath images (219 ASD, 328 Non-ASD neurotypical controls)."),
        ("Data Partitioning", "Stratified 80% Training (437 samples) and 20% Holdout Testing (110 samples)."),
        ("Augmentation Strategy", "Rotation (±15°), horizontal/vertical flips expanding training set to ~1,750 samples to prevent deep learning overfitting.")
    ]
    for dh, dd in d_info:
        pdh = tf_ds.add_paragraph()
        pdh.text = f"{dh}:"
        pdh.font.size = Pt(12)
        pdh.font.bold = True
        pdh.font.color.rgb = TEXT_DARK
        pdd = tf_ds.add_paragraph()
        pdd.text = dd
        pdd.font.size = Pt(10.5)
        pdd.font.color.rgb = TEXT_MUTED
        pdd.space_after = Pt(6)

    # Right Card: Preprocessing Pipeline & Embedded Image
    add_card(slide3, Inches(5.6), Inches(1.6), Inches(6.9), Inches(5.4))
    tb_pr = slide3.shapes.add_textbox(Inches(5.8), Inches(1.8), Inches(6.5), Inches(2.2))
    tf_pr = tb_pr.text_frame
    tf_pr.word_wrap = True

    p_prh = tf_pr.paragraphs[0]
    p_prh.text = "4-STAGE STANDARDIZATION PIPELINE"
    p_prh.font.size = Pt(11)
    p_prh.font.bold = True
    p_prh.font.color.rgb = BLUE_PRIMARY
    p_prh.space_after = Pt(6)

    steps = [
        "1. Spatial Resizing: Bilinear resampling to uniform 224 × 224 resolution for neural network input.",
        "2. Gaussian Denoising: 5 × 5 blur filter (σ=0) to suppress high-frequency hardware acquisition noise.",
        "3. Min-Max Normalization: Gaze intensity scaled to [0, 1] range preserving fixation hotspots.",
        "4. Feature Encoding: Normalization to [-1, 1] matching pre-trained MobileNet feature space."
    ]
    for s in steps:
        ps = tf_pr.add_paragraph()
        ps.text = s
        ps.font.size = Pt(11)
        ps.font.color.rgb = TEXT_DARK
        ps.space_after = Pt(3)

    # Embed preprocessed comparison image
    raw_img_path = os.path.join(static_dir, "02_preprocessing_comparison.png")
    if os.path.exists(raw_img_path):
        slide3.shapes.add_picture(raw_img_path, Inches(5.8), Inches(3.9), width=Inches(6.5))

    # =========================================================================
    # SLIDE 4: Feature Extraction & PCA Dimensionality Reduction
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Feature Extraction (MobileNet) & PCA Dimensionality Reduction", category="03. FEATURE ENGINEERING")

    # Left: MobileNet Feature Extraction
    add_card(slide4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.4))
    tb_m = slide4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(5.0))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True

    p_mh = tf_m.paragraphs[0]
    p_mh.text = "TRANSFER LEARNING VIA MOBILENET"
    p_mh.font.size = Pt(11)
    p_mh.font.bold = True
    p_mh.font.color.rgb = BLUE_PRIMARY
    p_mh.space_after = Pt(8)

    m_points = [
        ("Depthwise Separable Convolutions", "Drastically reduces parameter count while preserving spatial feature hierarchies from scanpaths."),
        ("Global Average Pooling (GAP)", "Condenses spatial convolutional feature maps into a dense 1,024-dimensional continuous feature vector."),
        ("Why MobileNet over ResNet?", "Achieves higher generalization with 6× lower computational overhead, making it ideal for clinical deployment.")
    ]
    for m_head, m_body in m_points:
        pmh = tf_m.add_paragraph()
        pmh.text = "• " + m_head
        pmh.font.size = Pt(12.5)
        pmh.font.bold = True
        pmh.font.color.rgb = TEXT_DARK
        pmd = tf_m.add_paragraph()
        pmd.text = "   " + m_body
        pmd.font.size = Pt(10.5)
        pmd.font.color.rgb = TEXT_MUTED
        pmd.space_after = Pt(8)

    # Right: PCA Dimensionality Reduction
    add_card(slide4, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.4))
    tb_pca = slide4.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(2.2))
    tf_pca = tb_pca.text_frame
    tf_pca.word_wrap = True

    p_pcah = tf_pca.paragraphs[0]
    p_pcah.text = "PCA: 1024-D → 250 COMPONENTS (92.1% VARIANCE)"
    p_pcah.font.size = Pt(11)
    p_pcah.font.bold = True
    p_pcah.font.color.rgb = BLUE_PRIMARY
    p_pcah.space_after = Pt(6)

    pca_facts = [
        "Curse of Dimensionality Elimination: 1,024 features on 547 samples causes severe overfitting without PCA.",
        "Noise Filtering: Removes low-variance noise components while retaining 92.1% cumulative variance.",
        "Performance Leap: Adding PCA boosted downstream classification accuracy from 78.5% to 92.7%."
    ]
    for pf in pca_facts:
        ppf = tf_pca.add_paragraph()
        ppf.text = "✔ " + pf
        ppf.font.size = Pt(10.5)
        ppf.font.color.rgb = TEXT_DARK
        ppf.space_after = Pt(4)

    # Embed PCA Variance plot
    pca_img_path = os.path.join(static_dir, "05_pca_variance.png")
    if os.path.exists(pca_img_path):
        slide4.shapes.add_picture(pca_img_path, Inches(7.0), Inches(4.0), width=Inches(5.3))

    # =========================================================================
    # SLIDE 5: Stacking Ensemble Learning Architecture
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Stacking Ensemble Classification Architecture", category="04. MODEL ARCHITECTURE")

    ens_components = [
        ("BASE MODEL 1", "Support Vector Machine (SVM)", "RBF Kernel (C=10, γ=scale)",
         "Finds optimal non-linear maximum margin hyperplane separating ASD from neurotypical gaze patterns in 250-D PCA space.",
         BLUE_PRIMARY),
        ("BASE MODEL 2", "K-Nearest Neighbors (KNN)", "k = 5 Distance-Weighted",
         "Instance-based non-parametric classifier capturing localized spatial manifold clusters and neighborhood densities.",
         CYAN_ACCENT),
        ("META-LEARNER", "Logistic Regression", "5-Fold Stacking CV",
         "Combines out-of-fold probability predictions of both base classifiers to output final calibrated diagnostic likelihood.",
         SUCCESS_COLOR)
    ]
    card_w3 = Inches(3.64)
    for i, (tag, name, sub, desc, color) in enumerate(ens_components):
        left_pos = Inches(0.8 + i * 4.04)
        add_card(slide5, left_pos, Inches(1.6), card_w3, Inches(4.1))
        tb_c = slide5.shapes.add_textbox(left_pos + Inches(0.2), Inches(1.8), card_w3 - Inches(0.4), Inches(3.7))
        tfc = tb_c.text_frame
        tfc.word_wrap = True

        ptag = tfc.paragraphs[0]
        ptag.text = tag
        ptag.font.size = Pt(11)
        ptag.font.bold = True
        ptag.font.color.rgb = color

        pname = tfc.add_paragraph()
        pname.text = name
        pname.font.size = Pt(16)
        pname.font.bold = True
        pname.font.color.rgb = TEXT_DARK
        pname.space_after = Pt(2)

        psub = tfc.add_paragraph()
        psub.text = sub
        psub.font.size = Pt(11)
        psub.font.color.rgb = BLUE_PRIMARY
        psub.font.bold = True
        psub.space_after = Pt(10)

        pdesc = tfc.add_paragraph()
        pdesc.text = desc
        pdesc.font.size = Pt(11)
        pdesc.font.color.rgb = TEXT_MUTED
        pdesc.space_after = Pt(8)

    # Bottom Pipeline Flow Ribbon
    add_card(slide5, Inches(0.8), Inches(5.9), Inches(11.733), Inches(1.1), bg_color=DARK_NAVY, border_color=None)
    tb_rib = slide5.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.333), Inches(1.0))
    tf_rib = tb_rib.text_frame
    tf_rib.word_wrap = True
    prib = tf_rib.paragraphs[0]
    prib.text = "FULL END-TO-END INFERENCE PIPELINE:"
    prib.font.size = Pt(11)
    prib.font.bold = True
    prib.font.color.rgb = CYAN_ACCENT

    prib2 = tf_rib.add_paragraph()
    prib2.text = "Input Scanpath (224×224)  ➔  MobileNet Feature Extractor (1024-D)  ➔  PCA Reduction (250-D)  ➔  Stacking Ensemble (SVM + KNN ➔ Logistic Regression)  ➔  ASD Probability"
    prib2.font.size = Pt(12)
    prib2.font.bold = True
    prib2.font.color.rgb = WHITE
    prib2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 6: Experimental Results & Benchmarking
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Experimental Results & Benchmark Comparison", category="05. RESULTS & EVALUATION")

    # Left: Results Table Card
    add_card(slide6, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.4))
    tb_tbl = slide6.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(6.4), Inches(5.0))
    tf_tbl = tb_tbl.text_frame
    tf_tbl.word_wrap = True

    ptbl_h = tf_tbl.paragraphs[0]
    ptbl_h.text = "MODEL PERFORMANCE COMPARISON (ETSDS BENCHMARK)"
    ptbl_h.font.size = Pt(11)
    ptbl_h.font.bold = True
    ptbl_h.font.color.rgb = BLUE_PRIMARY
    ptbl_h.space_after = Pt(10)

    perf_data = [
        ("Model Pipeline", "Accuracy", "Precision", "Sensitivity", "Specificity"),
        ("MobileNet + PCA + Stacking", "92.69%", "90.86%", "90.86%", "93.92%"),
        ("MobileNet + PCA + SVM", "92.69%", "90.40%", "91.43%", "93.54%"),
        ("MobileNet + PCA + KNN", "90.41%", "88.89%", "86.86%", "92.78%"),
        ("ResNet50 + Stacking", "90.12%", "89.50%", "88.40%", "91.20%"),
        ("Baseline (No PCA Reduction)", "78.56%", "77.10%", "76.40%", "79.80%"),
        ("Published Paper Benchmark", "98.00%", "98.40%", "98.20%", "97.80%")
    ]
    for row in perf_data:
        p_row = tf_tbl.add_paragraph()
        p_row.text = f"{row[0]:<28} | {row[1]:<9} | {row[2]:<10} | {row[3]:<11} | {row[4]}"
        p_row.font.size = Pt(11)
        p_row.font.name = "Courier New"
        if row[0] == "Model Pipeline":
            p_row.font.bold = True
            p_row.font.color.rgb = TEXT_DARK
        elif "MobileNet + PCA + Stacking" in row[0]:
            p_row.font.bold = True
            p_row.font.color.rgb = BLUE_PRIMARY
        elif "Paper" in row[0]:
            p_row.font.italic = True
            p_row.font.color.rgb = TEXT_MUTED
        else:
            p_row.font.color.rgb = TEXT_MUTED
        p_row.space_after = Pt(6)

    # Key takeaways
    p_take = tf_tbl.add_paragraph()
    p_take.text = "\nKey Takeaway: The Stacking Ensemble achieves a superior 93.92% Specificity, effectively minimizing false-positive ASD referrals while retaining 90.86% clinical sensitivity."
    p_take.font.size = Pt(10.5)
    p_take.font.color.rgb = SUCCESS_COLOR
    p_take.font.bold = True

    # Right: Embedded Confusion Matrix / Model comparison plot
    add_card(slide6, Inches(7.8), Inches(1.6), Inches(4.7), Inches(5.4))
    tb_plt = slide6.shapes.add_textbox(Inches(8.0), Inches(1.8), Inches(4.3), Inches(0.4))
    tf_plt = tb_plt.text_frame
    p_plth = tf_plt.paragraphs[0]
    p_plth.text = "CONFUSION MATRIX & ERROR DISTRIBUTION"
    p_plth.font.size = Pt(11)
    p_plth.font.bold = True
    p_plth.font.color.rgb = BLUE_PRIMARY

    cm_path = os.path.join(static_dir, "06_confusion_mobilenet_+_stacking_ensemble.png")
    if os.path.exists(cm_path):
        slide6.shapes.add_picture(cm_path, Inches(8.0), Inches(2.4), width=Inches(4.3))

    # =========================================================================
    # SLIDE 7: Explainable AI (XAI) Framework
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Explainable AI (XAI): Transparent Clinical Decision Support", category="06. EXPLAINABILITY & TRUST")

    xai_cols = [
        ("XAI METHOD 1", "Occlusion Sensitivity Mapping", "Spatial Heatmap Attribution",
         "A neutral gray patch slides across the image to measure changes in ASD probability. Image regions whose occlusion causes significant prediction drops are highlighted in warm colors (red/yellow).",
         "Clinicians can visually verify whether the model is focusing on legitimate gaze path anomalies rather than background image artifacts."),
        ("XAI METHOD 2", "Kinematic Channel Ablation", "Velocity, Acceleration & Jerk",
         "The eye-tracking RGB scanpath encodes physical kinematics: Red (Gaze Velocity), Green (Acceleration), Blue (Jerk).",
         "By selectively zeroing each channel, the system measures the exact drop (Δ%) in model confidence, revealing the kinematic drivers of the diagnosis.")
    ]
    col_w2 = Inches(5.7)
    for i, (tag, title, sub, desc1, desc2) in enumerate(xai_cols):
        left_p = Inches(0.8 + i * 6.0)
        add_card(slide7, left_p, Inches(1.6), col_w2, Inches(5.4))
        tb_x = slide7.shapes.add_textbox(left_p + Inches(0.2), Inches(1.8), col_w2 - Inches(0.4), Inches(5.0))
        tfx = tb_x.text_frame
        tfx.word_wrap = True

        ptag = tfx.paragraphs[0]
        ptag.text = tag
        ptag.font.size = Pt(11)
        ptag.font.bold = True
        ptag.font.color.rgb = BLUE_PRIMARY

        ptitle = tfx.add_paragraph()
        ptitle.text = title
        ptitle.font.size = Pt(16)
        ptitle.font.bold = True
        ptitle.font.color.rgb = TEXT_DARK

        psub = tfx.add_paragraph()
        psub.text = sub
        psub.font.size = Pt(12)
        psub.font.bold = True
        psub.font.color.rgb = CYAN_ACCENT
        psub.space_after = Pt(12)

        pd1 = tfx.add_paragraph()
        pd1.text = "• " + desc1
        pd1.font.size = Pt(11.5)
        pd1.font.color.rgb = TEXT_DARK
        pd1.space_after = Pt(10)

        pd2 = tfx.add_paragraph()
        pd2.text = "• " + desc2
        pd2.font.size = Pt(11.5)
        pd2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 8: The EyeTrace AI Web Platform Architecture
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "The EyeTrace AI Full-Stack Web Platform", category="07. SYSTEM IMPLEMENTATION")

    add_card(slide8, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.4))
    tb_fe = slide8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(5.0))
    tf_fe = tb_fe.text_frame
    tf_fe.word_wrap = True

    p_feh = tf_fe.paragraphs[0]
    p_feh.text = "FRONTEND CLIENT (REACT 19 + VITE + TAILWIND)"
    p_feh.font.size = Pt(11)
    p_feh.font.bold = True
    p_feh.font.color.rgb = BLUE_PRIMARY
    p_feh.space_after = Pt(8)

    fe_features = [
        ("Instant Scanpath Upload & Validation", "Drag-and-drop zone with instant client-side thumbnail rendering and resolution checks."),
        ("Animated Step-by-Step Pipeline Progress", "Displays real-time inference progress from preprocessing to feature extraction and classification."),
        ("Interactive Diagnostic Dashboard", "Displays high-contrast risk classification, calibrated probability meter, and interactive kinematic breakdown."),
        ("Medical Accessibility & Dark Mode", "High-contrast clinical UI designed for laboratory environments and desktop/tablet use.")
    ]
    for fh, fd in fe_features:
        pfh = tf_fe.add_paragraph()
        pfh.text = "• " + fh
        pfh.font.size = Pt(12)
        pfh.font.bold = True
        pfh.font.color.rgb = TEXT_DARK
        pfd = tf_fe.add_paragraph()
        pfd.text = "   " + fd
        pfd.font.size = Pt(10.5)
        pfd.font.color.rgb = TEXT_MUTED
        pfd.space_after = Pt(6)

    # Right: Backend Server Architecture
    add_card(slide8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.4))
    tb_be = slide8.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(5.0))
    tf_be = tb_be.text_frame
    tf_be.word_wrap = True

    p_beh = tf_be.paragraphs[0]
    p_beh.text = "BACKEND SERVER (FASTAPI + DOCKER + ML ENGINE)"
    p_beh.font.size = Pt(11)
    p_beh.font.bold = True
    p_beh.font.color.rgb = BLUE_PRIMARY
    p_beh.space_after = Pt(8)

    be_features = [
        ("FastAPI Asynchronous REST API", "High-throughput asynchronous endpoints (/api/v1/predict, /api/health) running on Uvicorn."),
        ("Sub-Second Inference Speed", "Optimized MobileNet forward passes and PCA transformations complete in <400 ms."),
        ("Micro-Batch Memory Optimization", "Vectorized 16-patch explainability algorithm designed to run within strict 512 MB memory footprints."),
        ("Multi-Stage Containerization", "Docker multi-stage build uniting React compilation and Python inference inside one deployable container.")
    ]
    for bh, bd in be_features:
        pbh = tf_be.add_paragraph()
        pbh.text = "✔ " + bh
        pbh.font.size = Pt(12)
        pbh.font.bold = True
        pbh.font.color.rgb = TEXT_DARK
        pbd = tf_be.add_paragraph()
        pbd.text = "   " + bd
        pbd.font.size = Pt(10.5)
        pbd.font.color.rgb = TEXT_MUTED
        pbd.space_after = Pt(6)

    # =========================================================================
    # SLIDE 9: Clinical Safety Protocol & Workflow Integration
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Clinical Safety Protocol & Healthcare Integration", category="08. ETHICS & CLINICAL WORKFLOW")

    safety_cards = [
        ("DECISION THRESHOLDS", "Risk Stratification",
         ["Probability > 75%: High confidence ASD gaze marker; prioritize for expedited specialist evaluation.",
          "Probability 50–75%: Moderate risk pattern; repeat scanpath or administer secondary screener.",
          "Probability < 50%: Neurotypical visual exploration pattern indicated."]),
        ("CLINICAL BOUNDARIES", "Academic & Screening Scope",
         ["Strict Decision-Support Role: The platform explicitly acts as an objective screening assistant, NOT an autonomous diagnostic tool.",
          "Clinical Multidisciplinary Requirement: Final diagnosis strictly requires formal clinical evaluation (ADOS-2, pediatric developmental assessment).",
          "Ethical Compliance: All patient images processed in-memory with zero cloud storage of identifying biometric data."]),
        ("FAULT TOLERANCE", "System Reliability & Fail-Safe",
         ["Real-Time Model Health Checks: GET /api/health continuously verifies integrity of PCA, StackingClassifier, and MobileNet weights.",
          "Graceful Degradation: If visual heatmap generation encounters timeout limits, classification and ablation scores still deliver without crashing.",
          "Zero Cloud Dependency: Full standalone local offline execution available for remote hospitals."])
    ]
    for i, (stag, stitle, sposts) in enumerate(safety_cards):
        sp_x = Inches(0.8 + i * 4.04)
        add_card(slide9, sp_x, Inches(1.6), card_w3, Inches(5.4))
        tb_s = slide9.shapes.add_textbox(sp_x + Inches(0.2), Inches(1.8), card_w3 - Inches(0.4), Inches(5.0))
        tfs = tb_s.text_frame
        tfs.word_wrap = True

        pst = tfs.paragraphs[0]
        pst.text = stag
        pst.font.size = Pt(11)
        pst.font.bold = True
        pst.font.color.rgb = BLUE_PRIMARY

        psth = tfs.add_paragraph()
        psth.text = stitle
        psth.font.size = Pt(15)
        psth.font.bold = True
        psth.font.color.rgb = TEXT_DARK
        psth.space_after = Pt(10)

        for pt in sposts:
            ppt = tfs.add_paragraph()
            ppt.text = "• " + pt
            ppt.font.size = Pt(10.5)
            ppt.font.color.rgb = TEXT_MUTED
            ppt.space_after = Pt(8)

    # =========================================================================
    # SLIDE 10: Conclusion & Future Roadmap
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    bg10 = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg10.fill.solid()
    bg10.fill.fore_color.rgb = DARK_NAVY
    bg10.line.fill.background()

    # Left Card: Summary of Achievements
    add_card(slide10, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3), bg_color=NAVY_CARD, border_color=CYAN_ACCENT)
    tb_ach = slide10.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.9))
    tf_ach = tb_ach.text_frame
    tf_ach.word_wrap = True

    p_achh = tf_ach.paragraphs[0]
    p_achh.text = "PROJECT ACHIEVEMENTS & CONTRIBUTIONS"
    p_achh.font.size = Pt(12)
    p_achh.font.bold = True
    p_achh.font.color.rgb = CYAN_ACCENT
    p_achh.space_after = Pt(10)

    recap = [
        ("High Diagnostic Accuracy (92.69%)",
         "Successfully proved that MobileNet transfer learning combined with PCA dimensionality reduction and Stacking Ensemble reliably classifies ASD scanpaths."),
        ("Multi-Modal Explainability (XAI)",
         "Implemented spatial Occlusion Sensitivity mapping and kinematic channel ablation to provide transparent justification for clinical trust."),
        ("Working Full-Stack Platform",
         "Engineered an end-to-end web system (React 19 + FastAPI) containerized with Docker, bridging the gap between theoretical research and practical clinical triage.")
    ]
    for rh, rd in recap:
        prh = tf_ach.add_paragraph()
        prh.text = "✔ " + rh
        prh.font.size = Pt(13)
        prh.font.bold = True
        prh.font.color.rgb = WHITE
        prd = tf_ach.add_paragraph()
        prd.text = "   " + rd
        prd.font.size = Pt(11)
        prd.font.color.rgb = TEXT_LIGHT_MUTED
        prd.space_after = Pt(8)

    # Right Card: Future Scope
    add_card(slide10, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3), bg_color=NAVY_CARD, border_color=LIGHT_CYAN)
    tb_fut = slide10.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(4.9))
    tf_fut = tb_fut.text_frame
    tf_fut.word_wrap = True

    p_futh = tf_fut.paragraphs[0]
    p_futh.text = "FUTURE RESEARCH ROADMAP"
    p_futh.font.size = Pt(12)
    p_futh.font.bold = True
    p_futh.font.color.rgb = LIGHT_CYAN
    p_futh.space_after = Pt(10)

    future = [
        ("Webcam-Based Real-Time Gaze Tracking",
         "Eliminate dedicated eye-tracking hardware by integrating browser-based computer vision gaze estimation (WebGazer / MediaPipe)."),
        ("Vision Transformers (ViT) & Attention Models",
         "Benchmark self-attention mechanisms to learn long-range temporal dependencies directly across scanpath saccadic sequences."),
        ("Multimodal Fusion with EEG Signals",
         "Integrate synchronized EEG brainwave signals alongside eye tracking for comprehensive multi-sensor autism biomarker screening.")
    ]
    for fh, fd in future:
        pfh = tf_fut.add_paragraph()
        pfh.text = "➔ " + fh
        pfh.font.size = Pt(13)
        pfh.font.bold = True
        pfh.font.color.rgb = WHITE
        pfd = tf_fut.add_paragraph()
        pfd.text = "   " + fd
        pfd.font.size = Pt(11)
        pfd.font.color.rgb = TEXT_LIGHT_MUTED
        pfd.space_after = Pt(8)

    prs.save(filename)
    print(f"Professional 10-slide presentation successfully generated at: {filename}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "ASD_EyeTracking_Presentation.pptx"
    create_deck(out_file)
