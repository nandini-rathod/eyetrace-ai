import { useCallback, useRef, useState } from 'react';
import { Upload, X, ImageIcon, CheckCircle2, AlertCircle } from 'lucide-react';

const ALLOWED_TYPES = ['image/png', 'image/jpeg', 'image/jpg'];
const MAX_SIZE_MB = 10;

export default function ImageUploader({ onFileSelected, selectedFile, onClear }) {
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState('');
  const inputRef = useRef(null);

  const validateFile = (file) => {
    if (!ALLOWED_TYPES.includes(file.type)) {
      return 'Only PNG, JPG, and JPEG files are accepted.';
    }
    if (file.size > MAX_SIZE_MB * 1024 * 1024) {
      return `File exceeds ${MAX_SIZE_MB} MB limit.`;
    }
    return null;
  };

  const handleFile = useCallback((file) => {
    const err = validateFile(file);
    if (err) {
      setError(err);
      return;
    }
    setError('');
    onFileSelected(file);
  }, [onFileSelected]);

  const onDrop = useCallback((e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }, [handleFile]);

  const onInputChange = (e) => {
    const file = e.target.files[0];
    if (file) handleFile(file);
  };

  if (selectedFile) {
    const previewURL = URL.createObjectURL(selectedFile);
    return (
      <div className="border-2 border-cyan-500/40 rounded-2xl p-6 bg-navy-800">
        <div className="flex flex-col sm:flex-row gap-6 items-start">
          <div className="relative flex-shrink-0">
            <img
              src={previewURL}
              alt="Scanpath preview"
              className="w-48 h-48 object-cover rounded-xl border border-navy-700"
              onLoad={() => URL.revokeObjectURL(previewURL)}
            />
            <button
              onClick={onClear}
              className="absolute -top-2 -right-2 w-7 h-7 bg-rose-500 hover:bg-rose-400 text-white rounded-full flex items-center justify-center transition-colors shadow-lg"
            >
              <X size={14} />
            </button>
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle2 size={18} className="text-cyan-400 flex-shrink-0" />
              <span className="text-white font-semibold text-sm truncate">{selectedFile.name}</span>
            </div>
            <p className="text-slate-400 text-sm mb-1">
              {(selectedFile.size / 1024).toFixed(1)} KB · {selectedFile.type}
            </p>
            <p className="text-slate-500 text-xs">
              Image ready for analysis. Dimensions will be resized to 224×224 during preprocessing.
            </p>
            <button
              onClick={onClear}
              className="mt-4 btn-secondary text-sm py-1.5 px-4"
            >
              Replace Image
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div
        onClick={() => inputRef.current?.click()}
        onDragEnter={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={(e) => { e.preventDefault(); setDragging(false); }}
        onDragOver={(e) => e.preventDefault()}
        onDrop={onDrop}
        className={`border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all duration-200 ${
          dragging
            ? 'border-cyan-400 bg-cyan-500/10'
            : 'border-navy-600 hover:border-cyan-500/60 hover:bg-navy-800/50'
        }`}
      >
        <div className="flex flex-col items-center gap-4">
          <div className={`w-16 h-16 rounded-2xl flex items-center justify-center transition-colors ${
            dragging ? 'bg-cyan-500/20' : 'bg-navy-700'
          }`}>
            <Upload size={28} className={dragging ? 'text-cyan-400' : 'text-slate-400'} />
          </div>
          <div>
            <p className="text-white font-semibold text-lg mb-1">
              {dragging ? 'Drop to upload' : 'Drag & drop your scanpath image'}
            </p>
            <p className="text-slate-400 text-sm">or click to browse files</p>
          </div>
          <div className="flex flex-wrap gap-2 justify-center">
            {['PNG', 'JPG', 'JPEG'].map(fmt => (
              <span key={fmt} className="px-2.5 py-0.5 bg-navy-700 border border-navy-600 rounded-md text-xs text-slate-300 font-mono">
                {fmt}
              </span>
            ))}
            <span className="px-2.5 py-0.5 bg-navy-700 border border-navy-600 rounded-md text-xs text-slate-300">
              Max 10 MB
            </span>
          </div>
        </div>
        <input
          ref={inputRef}
          type="file"
          accept=".png,.jpg,.jpeg"
          className="hidden"
          onChange={onInputChange}
        />
      </div>

      {error && (
        <div className="mt-3 flex items-center gap-2 text-rose-400 text-sm bg-rose-500/10 border border-rose-500/20 rounded-xl px-4 py-3">
          <AlertCircle size={16} className="flex-shrink-0" />
          {error}
        </div>
      )}
    </div>
  );
}
