import { BookOpen, Eye, Layers, Brain, BarChart3, AlertTriangle, ChevronRight } from 'lucide-react';

function Section({ icon, title, children }) {
  return (
    <section className="mb-10">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-9 h-9 rounded-xl bg-cyan-500/15 border border-cyan-500/25 flex items-center justify-center text-cyan-400 flex-shrink-0">
          {icon}
        </div>
        <h2 className="text-xl font-bold text-white">{title}</h2>
      </div>
      <div className="ml-12 text-slate-400 text-sm leading-relaxed space-y-3">
        {children}
      </div>
    </section>
  );
}

function PipelineStep({ n, title, detail }) {
  return (
    <div className="flex items-start gap-4 py-3 border-b border-navy-700 last:border-0">
      <div className="w-8 h-8 rounded-full bg-cyan-500 text-navy-900 font-bold text-sm flex items-center justify-center flex-shrink-0">
        {n}
      </div>
      <div>
        <div className="text-white font-medium">{title}</div>
        <div className="text-slate-400 text-xs mt-0.5">{detail}</div>
      </div>
    </div>
  );
}

export default function ResearchPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="mb-10">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/15 border border-cyan-500/25 flex items-center justify-center text-cyan-400">
            <BookOpen size={20} />
          </div>
          <h1 className="text-3xl font-bold text-white">Research & Methodology</h1>
        </div>
        <p className="text-slate-400 text-sm ml-13 pl-1">
          A technical overview of the EyeTrace AI pipeline, dataset, and explainability approach.
        </p>
      </div>

      <Section icon={<Eye size={18} />} title="Project Objective">
        <p>
          EyeTrace AI is an academic research demonstration that applies machine learning to
          eye-tracking scanpath images for ASD (Autism Spectrum Disorder) classification.
          The goal is to explore whether visual scanpath kinematic features, encoded as RGB images,
          can distinguish ASD and Non-ASD gaze patterns using a convolutional feature extractor
          combined with classical machine learning.
        </p>
        <p>
          This is not a clinical diagnostic system. It is a research prototype that demonstrates
          a full machine learning pipeline from raw scanpath images to interpretable classification
          with explainability analysis.
        </p>
      </Section>

      <Section icon={<Eye size={18} />} title="Eye-Tracking Scanpath Representation">
        <p>
          Eye-tracking data records where and how a participant's gaze moves over time.
          A scanpath is the temporal sequence of fixations and saccades recorded during a visual task.
        </p>
        <p>
          In this project, scanpaths are encoded as RGB images where the three color channels
          represent different kinematic properties of gaze movement:
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-4">
          {[
            { label: 'Red Channel', sub: 'Velocity', desc: 'Speed of gaze movement. Faster saccades = higher red intensity.', color: 'border-red-500/40 bg-red-500/10 text-red-400' },
            { label: 'Green Channel', sub: 'Acceleration', desc: 'Rate of change of velocity. High acceleration indicates rapid gaze shifts.', color: 'border-emerald-500/40 bg-emerald-500/10 text-emerald-400' },
            { label: 'Blue Channel', sub: 'Jerk', desc: 'Rate of change of acceleration. High jerk indicates erratic gaze transitions.', color: 'border-blue-500/40 bg-blue-500/10 text-blue-400' },
          ].map(ch => (
            <div key={ch.label} className={`rounded-xl border p-4 ${ch.color.split(' ').slice(0,2).join(' ')}`}>
              <div className={`font-bold text-sm mb-0.5 ${ch.color.split(' ')[2]}`}>{ch.label}</div>
              <div className="text-white font-semibold text-sm mb-2">{ch.sub}</div>
              <div className="text-slate-400 text-xs">{ch.desc}</div>
            </div>
          ))}
        </div>
        <p className="mt-3">
          This encoding allows convolutional networks to process spatial and kinematic information
          simultaneously using standard image classification architectures.
        </p>
      </Section>

      <Section icon={<Layers size={18} />} title="Model Pipeline">
        <p>The classification pipeline consists of four stages:</p>
        <div className="mt-3 card">
          <PipelineStep n={1} title="Image Preprocessing" detail="RGB load → resize to 224×224 → Gaussian blur (5×5 kernel, σ=0) → MobileNet preprocess_input (scales to [-1, 1])" />
          <PipelineStep n={2} title="MobileNet Feature Extraction" detail="MobileNet (ImageNet pretrained, include_top=False, pooling='avg') extracts a 1024-dimensional feature vector via GlobalAveragePooling2D." />
          <PipelineStep n={3} title="PCA Dimensionality Reduction" detail="Fitted PCA (n_components=250, random_state=42) reduces features to 250 dimensions, capturing 92.1% of explained variance. PCA is loaded from pca_250.pkl — not refit at inference time." />
          <PipelineStep n={4} title="Stacking Classifier" detail="StackingClassifier with SVM + KNN base estimators and Logistic Regression meta-learner. Loaded from stacking_clf.pkl. Outputs class label (Autistic / Non_Autistic) and probabilities." />
        </div>
      </Section>

      <Section icon={<BarChart3 size={18} />} title="Explainability Methodology">
        <p>
          Grad-CAM is not applicable to this pipeline because the final classifier is a
          scikit-learn StackingClassifier, which is not differentiable with respect to the input image.
          Two model-agnostic methods are used instead:
        </p>
        <div className="space-y-4 mt-3">
          <div className="card">
            <div className="text-white font-semibold mb-2">1. Occlusion Sensitivity</div>
            <p>
              A 32×32 gray patch is systematically slid across the image (stride 16). For each
              patch position, the full inference pipeline is re-run and the ASD probability is
              recorded. The heatmap shows regions where occlusion causes the largest drop in
              ASD probability — i.e., regions most influential to the prediction. This is
              a valid model attribution technique for any pipeline.
            </p>
          </div>
          <div className="card">
            <div className="text-white font-semibold mb-2">2. Channel Ablation</div>
            <p>
              Each RGB channel (Velocity, Acceleration, Jerk) is independently zeroed out and
              inference is re-run. The delta in ASD probability measures how much each kinematic
              feature contributed to the final classification. A large positive delta for a channel
              indicates it strongly supported the prediction.
            </p>
          </div>
        </div>
        <div className="mt-4 bg-amber-500/10 border border-amber-500/20 rounded-xl p-4 flex gap-3">
          <AlertTriangle size={16} className="text-amber-400 flex-shrink-0 mt-0.5" />
          <div>
            <div className="text-amber-400 font-semibold text-sm mb-1">Attribution ≠ Clinical Evidence</div>
            <div className="text-xs text-slate-300">
              Explainability maps show which image features influenced the model's decision,
              not which gaze behaviors are clinically associated with ASD. Do not interpret
              heatmaps as clinical findings or behavioral evidence.
            </div>
          </div>
        </div>
      </Section>

      <Section icon={<Brain size={18} />} title="Dataset & Model Training">
        <p>
          The model was trained on a labeled dataset of RGB-encoded eye-tracking scanpath images:
        </p>
        <ul className="list-disc list-inside space-y-1 mt-2">
          <li><strong className="text-slate-200">ASD class:</strong> 219 images labeled "Autistic"</li>
          <li><strong className="text-slate-200">Non-ASD class:</strong> 328 images labeled "Non_Autistic"</li>
          <li><strong className="text-slate-200">Total:</strong> 547 images</li>
          <li><strong className="text-slate-200">PCA explained variance:</strong> 92.1% (250 components, paper uses 250; 95% variance requires 251)</li>
          <li><strong className="text-slate-200">Framework:</strong> TensorFlow/Keras (MobileNet), scikit-learn (PCA, StackingClassifier)</li>
          <li><strong className="text-slate-200">Random seed:</strong> 42</li>
        </ul>
      </Section>

      <Section icon={<AlertTriangle size={18} />} title="Limitations & Disclaimer">
        <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-5">
          <ul className="space-y-2">
            {[
              'This is a research prototype, not a clinically validated diagnostic tool.',
              'The dataset is small (547 images) and may not generalize across different eye-tracking setups, populations, or tasks.',
              'The model has not been evaluated on external datasets or through clinical trials.',
              'ASD is a spectrum condition. Eye-tracking patterns vary widely across individuals.',
              'Model predictions are influenced by scanpath encoding quality, image artifacts, and the specific visual task used during data collection.',
              'No demographic, clinical, or behavioral context is considered by the model.',
              'ASD diagnosis requires comprehensive multidisciplinary clinical evaluation.',
            ].map((item, i) => (
              <li key={i} className="flex gap-2 text-xs text-slate-300">
                <ChevronRight size={14} className="text-amber-400 flex-shrink-0 mt-0.5" />
                {item}
              </li>
            ))}
          </ul>
        </div>
      </Section>
    </div>
  );
}
