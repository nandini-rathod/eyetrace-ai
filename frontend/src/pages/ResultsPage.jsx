import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { 
  FlaskConical, AlertTriangle, CheckCircle2, XCircle, 
  Info, ChevronRight, BarChart3, Eye, Layers
} from 'lucide-react';
import HeatmapViz from '../components/HeatmapViz';
import ChannelViz from '../components/ChannelViz';

function ScoreBar({ value, label, color }) {
  return (
    <div className="mb-3">
      <div className="flex justify-between items-center mb-1">
        <span className="text-slate-300 text-sm">{label}</span>
        <span className="text-white font-mono text-sm font-semibold">{(value * 100).toFixed(1)}%</span>
      </div>
      <div className="w-full h-2 bg-navy-700 rounded-full overflow-hidden">
        <div
          className={`h-2 rounded-full transition-all duration-700 ${color}`}
          style={{ width: `${value * 100}%` }}
        />
      </div>
    </div>
  );
}

function AblationRow({ name, data }) {
  const isHigh = data.importance > 0.05;
  return (
    <div className="flex items-start gap-4 py-3 border-b border-navy-700 last:border-0">
      <div className="flex-1">
        <div className="text-white text-sm font-medium">{name}</div>
        <div className="text-slate-400 text-xs mt-0.5">
          Baseline: {(data.baseline_asd_probability * 100).toFixed(1)}% →
          Ablated: {(data.ablated_asd_probability * 100).toFixed(1)}%
        </div>
        <div className={`text-xs mt-0.5 ${data.delta > 0 ? 'text-amber-400' : 'text-slate-500'}`}>
          {data.direction}
        </div>
      </div>
      <div className="text-right">
        <div className={`font-mono text-sm font-bold ${isHigh ? 'text-cyan-400' : 'text-slate-400'}`}>
          Δ {(Math.abs(data.delta) * 100).toFixed(2)}%
        </div>
        <div className="text-slate-500 text-xs">importance</div>
      </div>
    </div>
  );
}

export default function ResultsPage() {
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [filename, setFilename] = useState('');

  useEffect(() => {
    const raw = sessionStorage.getItem('eyetrace_result');
    const name = sessionStorage.getItem('eyetrace_filename') || 'scanpath.png';
    if (!raw) {
      navigate('/analysis');
      return;
    }
    try {
      setResult(JSON.parse(raw));
      setFilename(name);
    } catch {
      navigate('/analysis');
    }
  }, [navigate]);

  if (!result) return null;

  const isASD = result.prediction === 'ASD';
  const exp = result.explainability || {};
  const viz = result.visualizations || {};
  const ablation = exp.channel_ablation || {};

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      {/* Header */}
      <div className="mb-8 flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white mb-1">Analysis Results</h1>
          <p className="text-slate-400 text-sm">File: <code className="text-cyan-300">{filename}</code> · ID: <code className="text-cyan-300">{result.analysis_id}</code></p>
        </div>
        <Link to="/analysis" className="btn-secondary text-sm py-2 px-4 self-start">
          <FlaskConical size={15} />
          Analyze Another
        </Link>
      </div>

      {/* Top row: prediction + scores */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Prediction */}
        <div className="card">
          <h2 className="text-slate-400 text-sm font-semibold uppercase tracking-wider mb-4">Classification</h2>
          <div className={`inline-flex items-center gap-3 px-5 py-3 rounded-xl text-xl font-bold border mb-4 ${
            isASD
              ? 'bg-rose-500/15 border-rose-500/40 text-rose-400'
              : 'bg-emerald-500/15 border-emerald-500/40 text-emerald-400'
          }`}>
            {isASD ? <XCircle size={22} /> : <CheckCircle2 size={22} />}
            {result.prediction}
          </div>

          <p className="text-slate-400 text-sm mb-6">
            {isASD
              ? 'The model classified this scanpath as exhibiting patterns consistent with the ASD class in the training data.'
              : 'The model classified this scanpath as exhibiting patterns consistent with the Non-ASD class in the training data.'}
          </p>

          <ScoreBar value={result.asd_probability} label="ASD Probability" color="bg-rose-500" />
          <ScoreBar value={result.non_asd_probability} label="Non-ASD Probability" color="bg-emerald-500" />
          <ScoreBar value={result.confidence} label="Confidence (max prob)" color="bg-cyan-500" />

          <div className="mt-4 flex items-start gap-2 bg-navy-700/50 rounded-xl p-3">
            <Info size={15} className="text-cyan-400 flex-shrink-0 mt-0.5" />
            <p className="text-slate-400 text-xs">
              Confidence is the maximum class probability from the meta-learner (Logistic Regression).
              A higher value means the stacking ensemble is more certain in its assignment.
            </p>
          </div>
        </div>

        {/* Original + model info */}
        <div className="card">
          <h2 className="text-slate-400 text-sm font-semibold uppercase tracking-wider mb-4">Scanpath Image</h2>
          {viz.original_b64 ? (
            <img
              src={`data:image/png;base64,${viz.original_b64}`}
              alt="Original scanpath"
              className="w-full max-h-56 object-contain rounded-xl border border-navy-700 mb-4"
            />
          ) : (
            <div className="w-full h-40 bg-navy-700 rounded-xl border border-navy-600 flex items-center justify-center text-slate-500 text-sm mb-4">
              Image not available
            </div>
          )}
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Model</span>
              <span className="text-white text-right text-xs max-w-[200px]">{result.model_name}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Preprocessing</span>
              <span className="text-white text-xs">224×224, Gaussian blur (5×5)</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Features</span>
              <span className="text-white text-xs">MobileNet → 1024 → PCA → 250</span>
            </div>
          </div>
        </div>
      </div>

      {/* RGB Channel visualizations */}
      <div className="card mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Eye size={18} className="text-cyan-400" />
          <h2 className="text-white font-semibold">RGB Channel Visualizations</h2>
        </div>
        <p className="text-slate-400 text-sm mb-5">
          Each RGB channel encodes a different kinematic property of the original eye-tracking scanpath.
          The colormap is applied for visual clarity only — it does not alter the data used by the model.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <ChannelViz
            b64={viz.red_velocity_b64}
            label="Red Channel"
            description="Velocity — gaze speed (hot colormap)"
            color="red"
          />
          <ChannelViz
            b64={viz.green_acceleration_b64}
            label="Green Channel"
            description="Acceleration — rate of velocity change (summer colormap)"
            color="green"
          />
          <ChannelViz
            b64={viz.blue_jerk_b64}
            label="Blue Channel"
            description="Jerk — rate of acceleration change (cool colormap)"
            color="blue"
          />
        </div>
      </div>

      {/* Occlusion heatmap */}
      {exp.occlusion_heatmap_b64 && (
        <div className="mb-6">
          <HeatmapViz b64={exp.occlusion_heatmap_b64} />
        </div>
      )}

      {/* Channel ablation */}
      {Object.keys(ablation).length > 0 && (
        <div className="card mb-6">
          <div className="flex items-center gap-2 mb-2">
            <BarChart3 size={18} className="text-cyan-400" />
            <h2 className="text-white font-semibold">Channel Ablation Analysis</h2>
          </div>
          <p className="text-slate-400 text-sm mb-4">
            Each RGB channel is zeroed out independently to measure its contribution to the ASD prediction.
            A large positive Δ indicates that channel strongly supported the classification.
          </p>
          <div>
            {Object.entries(ablation).map(([name, data]) => (
              <AblationRow key={name} name={name} data={data} />
            ))}
          </div>
        </div>
      )}

      {/* Explainability method info */}
      <div className="card mb-6">
        <div className="flex items-center gap-2 mb-3">
          <Layers size={18} className="text-cyan-400" />
          <h2 className="text-white font-semibold">Explainability Methodology</h2>
        </div>
        <p className="text-slate-400 text-sm leading-relaxed mb-3">
          <strong className="text-slate-200">Method:</strong> {exp.method}
        </p>
        <p className="text-slate-400 text-sm leading-relaxed">
          {exp.description}
        </p>
        <div className="mt-4 bg-amber-500/10 border border-amber-500/20 rounded-xl p-3 flex gap-2">
          <Info size={15} className="text-amber-400 flex-shrink-0 mt-0.5" />
          <p className="text-amber-200 text-xs">
            Grad-CAM is NOT applicable here. The final classifier is a scikit-learn StackingClassifier
            (non-differentiable with respect to the input). Occlusion sensitivity is model-agnostic
            and valid for any pipeline. These heatmaps show <em>model attribution</em> —
            not human gaze patterns or clinical indicators.
          </p>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="bg-amber-500/10 border border-amber-500/30 rounded-2xl p-6 flex gap-4">
        <AlertTriangle size={22} className="text-amber-400 flex-shrink-0 mt-0.5" />
        <div>
          <h3 className="text-amber-400 font-semibold mb-2">Research Disclaimer</h3>
          <p className="text-slate-300 text-sm leading-relaxed">{result.disclaimer}</p>
        </div>
      </div>
    </div>
  );
}
