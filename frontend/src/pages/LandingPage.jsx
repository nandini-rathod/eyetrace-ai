import { Link } from 'react-router-dom';
import {
  Brain, FlaskConical, Eye, ChevronRight, Layers, Cpu,
  ScanLine, BarChart3, Shield, BookOpen, AlertTriangle,
} from 'lucide-react';

const steps = [
  { icon: <ScanLine size={22} />, title: 'Upload Scanpath', desc: 'Upload an RGB-encoded eye-tracking scanpath image (PNG/JPG).' },
  { icon: <Cpu size={22} />, title: 'MobileNet Extraction', desc: 'MobileNet (ImageNet pretrained) extracts 1024-dimensional visual features.' },
  { icon: <Layers size={22} />, title: 'PCA Reduction', desc: 'PCA reduces features to 250 components, capturing 92.1% of variance.' },
  { icon: <Brain size={22} />, title: 'Stacking Classifier', desc: 'SVM + KNN base learners with Logistic Regression meta-learner predict ASD vs Non-ASD.' },
  { icon: <BarChart3 size={22} />, title: 'Explainability', desc: 'Occlusion sensitivity and channel ablation reveal which regions and channels influenced the prediction.' },
];

const channels = [
  { label: 'Red Channel', sub: 'Velocity', color: 'bg-red-500/15 border-red-500/30 text-red-400', desc: 'Encodes the speed of gaze movement at each scanpath point.' },
  { label: 'Green Channel', sub: 'Acceleration', color: 'bg-emerald-500/15 border-emerald-500/30 text-emerald-400', desc: 'Encodes the rate of change of gaze velocity — acceleration.' },
  { label: 'Blue Channel', sub: 'Jerk', color: 'bg-blue-500/15 border-blue-500/30 text-blue-400', desc: 'Encodes the rate of change of acceleration — jerk or jerkiness.' },
];

const features = [
  { icon: <Brain size={20} />, title: 'Real ML Inference', desc: 'Locally running trained model — no external AI APIs.' },
  { icon: <Eye size={20} />, title: 'Explainable AI', desc: 'Occlusion sensitivity maps and channel ablation analysis.' },
  { icon: <Shield size={20} />, title: 'Research Transparent', desc: 'Clear disclaimers and honest model limitations presented.' },
  { icon: <BookOpen size={20} />, title: 'Scientific Context', desc: 'Full pipeline documentation and methodology explanation.' },
];

export default function LandingPage() {
  return (
    <div className="text-white">
      {/* Hero */}
      <section className="relative overflow-hidden py-24 px-4">
        {/* Background glow */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-20 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-cyan-500/8 rounded-full blur-3xl" />
        </div>

        <div className="max-w-5xl mx-auto text-center relative">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-sm font-medium mb-6">
            <Brain size={14} />
            Academic Research Project — Not for Clinical Use
          </div>

          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold mb-6 leading-tight tracking-tight">
            EyeTrace{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
              AI
            </span>
          </h1>

          <p className="text-xl text-slate-300 max-w-2xl mx-auto mb-4 leading-relaxed">
            Explainable ASD eye-tracking scanpath classification powered by{' '}
            <strong className="text-white">MobileNet + PCA + Stacking Classifier</strong>
            , running entirely on your local machine.
          </p>
          <p className="text-slate-400 max-w-xl mx-auto mb-10 text-sm">
            Upload an RGB-encoded scanpath image and receive a classification with scientifically
            valid explainability analysis — no external AI APIs, no cloud services.
          </p>

          <div className="flex flex-wrap gap-4 justify-center">
            <Link to="/analysis" className="btn-primary text-base px-8 py-3.5">
              <FlaskConical size={18} />
              Analyze Scanpath
              <ChevronRight size={16} />
            </Link>
            <Link to="/research" className="btn-secondary text-base px-8 py-3.5">
              <BookOpen size={18} />
              Learn About the Research
            </Link>
          </div>
        </div>
      </section>

      {/* RGB Channels */}
      <section className="py-16 px-4 bg-navy-800/40">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-10">
            <h2 className="text-3xl font-bold mb-3">RGB-Encoded Scanpath Images</h2>
            <p className="text-slate-400 max-w-xl mx-auto">
              The input images encode three kinematic features of eye-tracking scanpaths
              into the RGB color channels, enabling convolutional networks to extract spatial
              and temporal patterns simultaneously.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {channels.map((ch) => (
              <div key={ch.label} className={`card border ${ch.color}`}>
                <div className={`font-bold text-lg mb-0.5 ${ch.color.split(' ').find(c => c.startsWith('text-'))}`}>
                  {ch.label}
                </div>
                <div className="text-white font-semibold mb-3">{ch.sub}</div>
                <p className="text-slate-400 text-sm">{ch.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-10">
            <h2 className="text-3xl font-bold mb-3">How It Works</h2>
            <p className="text-slate-400">The complete inference pipeline — from image upload to explainability.</p>
          </div>
          <div className="relative">
            {/* Vertical connector line */}
            <div className="absolute left-8 top-10 bottom-10 w-px bg-gradient-to-b from-cyan-500/60 via-cyan-500/20 to-transparent hidden sm:block" />
            <div className="space-y-5">
              {steps.map((step, i) => (
                <div key={i} className="flex items-start gap-5">
                  <div className="relative flex-shrink-0">
                    <div className="w-16 h-16 rounded-2xl bg-navy-700 border border-cyan-500/30 flex items-center justify-center text-cyan-400 shadow-lg shadow-cyan-500/10">
                      {step.icon}
                    </div>
                    <span className="absolute -top-2 -right-2 w-5 h-5 rounded-full bg-cyan-500 text-navy-900 text-xs font-bold flex items-center justify-center">
                      {i + 1}
                    </span>
                  </div>
                  <div className="flex-1 pt-3">
                    <h3 className="text-white font-semibold text-lg mb-1">{step.title}</h3>
                    <p className="text-slate-400 text-sm">{step.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 px-4 bg-navy-800/40">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-10">Platform Features</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {features.map((f) => (
              <div key={f.title} className="card flex gap-4 items-start">
                <div className="w-10 h-10 rounded-xl bg-cyan-500/15 border border-cyan-500/25 flex items-center justify-center text-cyan-400 flex-shrink-0">
                  {f.icon}
                </div>
                <div>
                  <h3 className="text-white font-semibold mb-1">{f.title}</h3>
                  <p className="text-slate-400 text-sm">{f.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Disclaimer */}
      <section className="py-10 px-4">
        <div className="max-w-3xl mx-auto">
          <div className="bg-amber-500/10 border border-amber-500/30 rounded-2xl p-6 flex gap-4">
            <AlertTriangle size={24} className="text-amber-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="text-amber-400 font-semibold mb-2">Research Limitations Disclaimer</h3>
              <p className="text-slate-300 text-sm leading-relaxed">
                This tool is for <strong>academic research purposes only</strong>. The model was trained
                on a limited dataset (219 ASD + 328 Non-ASD samples) and has not been clinically validated.
                Results must not be used for diagnosis, screening, or any clinical decision-making.
                ASD diagnosis requires comprehensive multidisciplinary clinical evaluation by qualified
                healthcare professionals.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 px-4 text-center">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-3xl font-bold mb-4">Ready to Analyze a Scanpath?</h2>
          <p className="text-slate-400 mb-8">Upload your eye-tracking scanpath image and explore the model's explainability analysis.</p>
          <Link to="/analysis" className="btn-primary text-base px-8 py-3.5 inline-flex">
            <FlaskConical size={18} />
            Start Analysis
            <ChevronRight size={16} />
          </Link>
        </div>
      </section>
    </div>
  );
}
