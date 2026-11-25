import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
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

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
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
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(10.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = BLUE_PRIMARY
        p_cat.font.name = "Arial"

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.5), Inches(0.65))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_DARK
        p_t.font.name = "Arial"

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
    p3.font.color.rgb = WHITE
    p3.font.name = "Georgia"
    p3.alignment = PP_ALIGN.CENTER

    tb_team = slide1.shapes.add_textbox(Inches(2.5), Inches(4.5), Inches(8.333), Inches(1.4))
    tf_team = tb_team.text_frame
    tf_team.word_wrap = True

    p_tm_header = tf_team.paragraphs[0]
    p_tm_header.text = "Team Members: "
    p_tm_header.font.size = Pt(15)
    p_tm_header.font.bold = True
    p_tm_header.font.color.rgb = CYAN_ACCENT
    p_tm_header.alignment = PP_ALIGN.CENTER

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
        pm.alignment = PP_ALIGN.CENTER
        pm.space_after = Pt(2)

    tb_sup = slide1.shapes.add_textbox(Inches(2.5), Inches(6.2), Inches(8.333), Inches(0.8))
    tf_sup = tb_sup.text_frame
    tf_sup.word_wrap = True

    p_sup = tf_sup.paragraphs[0]
    p_sup.text = "Supervisor:   Dr. Nidhi Kushwaha"
    p_sup.font.size = Pt(15)
    p_sup.font.bold = True
    p_sup.font.color.rgb = CYAN_ACCENT
    p_sup.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: Problem Statement & Clinical Motivation
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Clinical Motivation & The Autism Diagnostic Crisis", category="01. INTRODUCTION & PROBLEM STATEMENT")

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

    raw_img_path = os.path.join(static_dir, "02_preprocessing_comparison.png")
    if os.path.exists(raw_img_path):
        slide3.shapes.add_picture(raw_img_path, Inches(5.8), Inches(3.9), width=Inches(6.5))

    # =========================================================================
    # SLIDE 4: Feature Extraction & PCA Dimensionality Reduction
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Feature Extraction (MobileNet) & PCA Dimensionality Reduction", category="03. FEATURE ENGINEERING")

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

    p_take = tf_tbl.add_paragraph()
    p_take.text = "\nKey Takeaway: The Stacking Ensemble achieves a superior 93.92% Specificity, effectively minimizing false-positive ASD referrals while retaining 90.86% clinical sensitivity."
    p_take.font.size = Pt(10.5)
    p_take.font.color.rgb = SUCCESS_COLOR
    p_take.font.bold = True

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
    # SLIDE 7: LIVE IMPLEMENTATION (Real Working Results from App Screenshot)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Live Platform Implementation: Diagnostic Classification", category="06. REAL WORKING SYSTEM")

    # Left: Explanation of Real Test Run
    add_card(slide7, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.4))
    tb_lr = slide7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.4), Inches(5.0))
    tf_lr = tb_lr.text_frame
    tf_lr.word_wrap = True

    p_lrh = tf_lr.paragraphs[0]
    p_lrh.text = "PATIENT SCANPATH INTAKE & PREDICTION"
    p_lrh.font.size = Pt(11)
    p_lrh.font.bold = True
    p_lrh.font.color.rgb = BLUE_PRIMARY
    p_lrh.space_after = Pt(8)

    lr_points = [
        ("Live Test Sample", "Evaluated scanpath test file TS010_19.png with unique tracking ID 0224b2a8."),
        ("High-Confidence ASD Detection", "Stacking Meta-Learner output an ASD Probability of 98.5% with high certainty (Non-ASD Probability: 1.5%)."),
        ("Synchronous Pipeline Execution", "Processed the input image through 224×224 scaling, Gaussian blur, MobileNet 1024-D feature extraction, and PCA 250 components in <400 ms."),
        ("Doctor-Facing Feedback", "Clear colored status indicators and progress bars prevent misinterpretation of probabilistic scores.")
    ]
    for lh, ld in lr_points:
        plh = tf_lr.add_paragraph()
        plh.text = "• " + lh
        plh.font.size = Pt(12)
        plh.font.bold = True
        plh.font.color.rgb = TEXT_DARK
        pld = tf_lr.add_paragraph()
        pld.text = "   " + ld
        pld.font.size = Pt(10.5)
        pld.font.color.rgb = TEXT_MUTED
        pld.space_after = Pt(6)

    # Right: Embedded Real UI Screenshot
    add_card(slide7, Inches(5.8), Inches(1.6), Inches(6.7), Inches(5.4), bg_color=DARK_NAVY, border_color=CYAN_ACCENT)
    tb_uicap = slide7.shapes.add_textbox(Inches(6.0), Inches(1.75), Inches(6.3), Inches(0.4))
    tf_uicap = tb_uicap.text_frame
    p_uic = tf_uicap.paragraphs[0]
    p_uic.text = "ACTUAL SYSTEM SCREENSHOT (RUNNING AT LOCALHOST:5173)"
    p_uic.font.size = Pt(10.5)
    p_uic.font.bold = True
    p_uic.font.color.rgb = CYAN_ACCENT

    live_screen1 = os.path.join(static_dir, "crop_classification.png")
    if os.path.exists(live_screen1):
        slide7.shapes.add_picture(live_screen1, Inches(6.0), Inches(2.2), width=Inches(6.3))

    # =========================================================================
    # SLIDE 8: Explainable AI in Action (Real Heatmap + Channel Ablation)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Explainable AI in Action: Heatmap & Channel Ablation", category="07. EXPLAINABILITY RESULTS")

    # Left: Heatmap
    add_card(slide8, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.4), bg_color=DARK_NAVY, border_color=CYAN_ACCENT)
    tb_hm = slide8.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(5.3), Inches(0.5))
    tf_hm = tb_hm.text_frame
    p_hm = tf_hm.paragraphs[0]
    p_hm.text = "OCCLUSION SENSITIVITY HEATMAP (REAL OUTPUT)"
    p_hm.font.size = Pt(11)
    p_hm.font.bold = True
    p_hm.font.color.rgb = CYAN_ACCENT

    live_hm = os.path.join(static_dir, "crop_heatmap.png")
    if os.path.exists(live_hm):
        slide8.shapes.add_picture(live_hm, Inches(1.0), Inches(2.3), width=Inches(5.3))

    tb_hmtxt = slide8.shapes.add_textbox(Inches(1.0), Inches(5.5), Inches(5.3), Inches(1.3))
    tf_ht = tb_hmtxt.text_frame
    tf_ht.word_wrap = True
    p_ht1 = tf_ht.paragraphs[0]
    p_ht1.text = "• Warm (red/yellow) center reveals the primary focal gaze cluster that heavily drove the ASD classification."
    p_ht1.font.size = Pt(10.5)
    p_ht1.font.color.rgb = WHITE

    # Right: Channel Ablation
    add_card(slide8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.4), bg_color=DARK_NAVY, border_color=LIGHT_CYAN)
    tb_ab = slide8.shapes.add_textbox(Inches(7.0), Inches(1.75), Inches(5.3), Inches(0.5))
    tf_ab = tb_ab.text_frame
    p_ab = tf_ab.paragraphs[0]
    p_ab.text = "CHANNEL ABLATION ANALYSIS (REAL OUTPUT)"
    p_ab.font.size = Pt(11)
    p_ab.font.bold = True
    p_ab.font.color.rgb = LIGHT_CYAN

    live_ab = os.path.join(static_dir, "crop_ablation.png")
    if os.path.exists(live_ab):
        slide8.shapes.add_picture(live_ab, Inches(7.0), Inches(2.3), width=Inches(5.3))

    tb_abtxt = slide8.shapes.add_textbox(Inches(7.0), Inches(5.5), Inches(5.3), Inches(1.3))
    tf_abt = tb_abtxt.text_frame
    tf_abt.word_wrap = True
    p_abt1 = tf_abt.paragraphs[0]
    p_abt1.text = "• Individually zeros Velocity, Acceleration, and Jerk channels to measure exact diagnostic importance (Δ%)."
    p_abt1.font.size = Pt(10.5)
    p_abt1.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 9: RGB Kinematic Channels & Clinical Safety Protocol
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "RGB Kinematic Channels & Clinical Safety Protocol", category="08. KINEMATICS & SAFETY")

    # Top: Embedded Kinematic Channels
    add_card(slide9, Inches(0.8), Inches(1.6), Inches(11.733), Inches(3.2), bg_color=DARK_NAVY, border_color=CYAN_ACCENT)
    tb_rgb_title = slide9.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.333), Inches(0.4))
    tf_rt = tb_rgb_title.text_frame
    p_rt = tf_rt.paragraphs[0]
    p_rt.text = "RGB SCANPATH KINEMATIC DECOMPOSITION: VELOCITY (RED) • ACCELERATION (GREEN) • JERK (BLUE)"
    p_rt.font.size = Pt(11)
    p_rt.font.bold = True
    p_rt.font.color.rgb = CYAN_ACCENT

    live_rgb = os.path.join(static_dir, "crop_rgb_channels.png")
    if os.path.exists(live_rgb):
        slide9.shapes.add_picture(live_rgb, Inches(2.5), Inches(2.1), width=Inches(8.333))

    # Bottom 3 Safety Cards
    bot_w = Inches(3.75)
    bot_cards = [
        ("DECISION THRESHOLDS", "Risk Stratification",
         ">75% High ASD Risk (flag for ADOS-2); 50-75% Moderate Risk (secondary test recommended); <50% Neurotypical."),
        ("CLINICAL BOUNDARIES", "Academic & Screening Role",
         "Acts strictly as an assistive screening aid, not an autonomous doctor replacement. Final diagnosis requires multidisciplinary assessment."),
        ("DATA PRIVACY", "Zero Persistent Biometric Storage",
         "All scanpaths processed in-memory during inference with immediate memory clearance to protect pediatric patient privacy.")
    ]
    for i, (btag, btitle, bdesc) in enumerate(bot_cards):
        bx = Inches(0.8 + i * 3.99)
        add_card(slide9, bx, Inches(4.95), bot_w, Inches(2.05))
        tb_b = slide9.shapes.add_textbox(bx + Inches(0.15), Inches(5.05), bot_w - Inches(0.3), Inches(1.85))
        tf_bc = tb_b.text_frame
        tf_bc.word_wrap = True

        pbt = tf_bc.paragraphs[0]
        pbt.text = btag
        pbt.font.size = Pt(10)
        pbt.font.bold = True
        pbt.font.color.rgb = BLUE_PRIMARY

        pbth = tf_bc.add_paragraph()
        pbth.text = btitle
        pbth.font.size = Pt(12)
        pbth.font.bold = True
        pbth.font.color.rgb = TEXT_DARK
        pbth.space_after = Pt(3)

        pbd = tf_bc.add_paragraph()
        pbd.text = bdesc
        pbd.font.size = Pt(10)
        pbd.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 10: Conclusion & Future Roadmap
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    bg10 = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg10.fill.solid()
    bg10.fill.fore_color.rgb = DARK_NAVY
    bg10.line.fill.background()

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
    print(f"Presentation successfully updated with embedded screenshots at: {filename}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "ASD_EyeTracking_Presentation.pptx"
    create_deck(out_file)
