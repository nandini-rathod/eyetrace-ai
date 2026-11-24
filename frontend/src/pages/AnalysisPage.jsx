import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { FlaskConical, Loader2, AlertCircle, AlertTriangle, ServerCrash } from 'lucide-react';
import ImageUploader from '../components/ImageUploader';
import ModelStatus from '../components/ModelStatus';
import { predictImage } from '../services/api';

const STAGES = [
  'Uploading image...',
  'Preprocessing (resize + Gaussian blur)...',
  'Extracting MobileNet features...',
  'Applying PCA (250 components)...',
  'Running Stacking Classifier...',
  'Computing explainability (occlusion + channel ablation)...',
  'Finalizing results...',
];

export default function AnalysisPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [stageIdx, setStageIdx] = useState(0);
  const [error, setError] = useState('');
  const [modelError, setModelError] = useState('');

  const handleAnalyze = useCallback(async () => {
    if (!file) return;
    setLoading(true);
    setError('');
    setModelError('');
    setStageIdx(0);

    // Animate stages (approximate timing — real work happens on backend)
    const stageTimer = setInterval(() => {
      setStageIdx((prev) => Math.min(prev + 1, STAGES.length - 1));
    }, 1800);

    try {
      const { data } = await predictImage(file, (evt) => {
        if (evt.loaded === evt.total) setStageIdx(1);
      });
      clearInterval(stageTimer);
      // Store result and navigate
      sessionStorage.setItem('eyetrace_result', JSON.stringify(data));
      sessionStorage.setItem('eyetrace_filename', file.name);
      navigate('/results');
    } catch (err) {
      clearInterval(stageTimer);
      setLoading(false);
      setStageIdx(0);
      const detail = err.response?.data?.detail;
      if (err.response?.status === 503) {
        setModelError(
          typeof detail === 'object'
            ? detail.detail || 'Model artifacts are not loaded.'
            : String(detail || 'Backend model is not ready.')
        );
      } else if (err.response?.status === 415) {
        setError(typeof detail === 'string' ? detail : 'Unsupported file type.');
      } else if (err.response?.status === 413) {
        setError('File is too large. Maximum size is 10 MB.');
      } else if (err.code === 'ERR_NETWORK' || err.code === 'ECONNREFUSED') {
        setModelError('Cannot reach the backend server. Please ensure it is running on http://127.0.0.1:8000.');
      } else {
        setError(
          typeof detail === 'string'
            ? detail
            : 'An unexpected error occurred. Check the backend console for details.'
        );
      }
    }
  }, [file, navigate]);

  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/15 border border-cyan-500/25 flex items-center justify-center text-cyan-400">
            <FlaskConical size={20} />
          </div>
          <h1 className="text-3xl font-bold text-white">Scanpath Analysis</h1>
        </div>
        <p className="text-slate-400 text-sm ml-13 pl-1">
          Upload an RGB-encoded eye-tracking scanpath image for ASD classification.
        </p>
        <div className="mt-3">
          <ModelStatus />
        </div>
      </div>

      {/* Upload */}
      {!loading && (
        <div className="card mb-6">
          <h2 className="text-white font-semibold mb-4">Upload Scanpath Image</h2>
          <ImageUploader
            selectedFile={file}
            onFileSelected={setFile}
            onClear={() => setFile(null)}
          />
        </div>
      )}

      {/* Loading state */}
      {loading && (
        <div className="card mb-6 text-center py-10">
          <div className="flex flex-col items-center gap-4">
            <div className="relative">
              <div className="w-16 h-16 rounded-full border-4 border-navy-700 border-t-cyan-500 animate-spin" />
              <div className="absolute inset-0 flex items-center justify-center">
                <Brain size={18} className="text-cyan-400" />
              </div>
            </div>
            <div>
              <p className="text-white font-semibold text-lg mb-1">Analyzing...</p>
              <p className="text-cyan-400 text-sm font-mono">{STAGES[stageIdx]}</p>
            </div>
            <div className="w-full max-w-xs bg-navy-700 rounded-full h-1.5">
              <div
                className="bg-gradient-to-r from-cyan-500 to-blue-500 h-1.5 rounded-full transition-all duration-1000"
                style={{ width: `${((stageIdx + 1) / STAGES.length) * 100}%` }}
              />
            </div>
            <p className="text-slate-500 text-xs">
              Occlusion sensitivity analysis may take 30–90 seconds depending on hardware.
            </p>
          </div>
        </div>
      )}

      {/* Model/server error */}
      {modelError && (
        <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-5 mb-5 flex gap-3">
          <ServerCrash size={20} className="text-amber-400 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-amber-400 font-semibold text-sm mb-1">Model Unavailable</p>
            <p className="text-slate-300 text-sm">{modelError}</p>
            <p className="text-slate-400 text-xs mt-2">
              Run the backend: <code className="bg-navy-700 px-2 py-0.5 rounded text-cyan-300">uvicorn app.main:app --reload</code> in <code className="bg-navy-700 px-2 py-0.5 rounded text-cyan-300">backend/</code>
            </p>
          </div>
        </div>
      )}

      {/* General error */}
      {error && (
        <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-4 mb-5 flex gap-3">
          <AlertCircle size={18} className="text-rose-400 flex-shrink-0 mt-0.5" />
          <p className="text-rose-300 text-sm">{error}</p>
        </div>
      )}

      {/* Analyze button */}
      {!loading && (
        <div className="flex flex-col sm:flex-row gap-4 items-start">
          <button
            onClick={handleAnalyze}
            disabled={!file}
            className={`btn-primary text-base px-8 py-3.5 ${!file ? 'opacity-40 cursor-not-allowed' : ''}`}
          >
            <FlaskConical size={18} />
            Analyze Scanpath
          </button>
          {!file && (
            <p className="text-slate-500 text-sm self-center">Select an image to enable analysis.</p>
          )}
        </div>
      )}

      {/* Disclaimer */}
      <div className="mt-10 flex gap-3 bg-navy-800/60 border border-navy-700 rounded-xl p-4">
        <AlertTriangle size={16} className="text-amber-400 flex-shrink-0 mt-0.5" />
        <p className="text-slate-400 text-xs leading-relaxed">
          <strong className="text-slate-300">Research use only.</strong> This tool runs your locally
          trained model for academic research. Results must not be used for clinical decisions,
          diagnosis, or screening. The model's classification does not constitute a medical opinion.
        </p>
      </div>
    </div>
  );
}

function Brain({ size, className }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={className}>
      <path d="M12 5C8.5 5 6 7.5 6 10c0 1.5.7 2.9 1.8 3.8C6.7 14.6 6 15.9 6 17.4 6 19.9 8.5 22 12 22s6-2.1 6-4.6c0-1.5-.7-2.8-1.8-3.6C17.3 12.9 18 11.5 18 10c0-2.5-2.5-5-6-5z"/>
    </svg>
  );
}
