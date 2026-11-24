import { CheckCircle2, XCircle, AlertTriangle, Loader2, Server } from 'lucide-react';
import { useEffect, useState } from 'react';
import { checkHealth } from '../services/api';

export default function ModelStatus({ className = '' }) {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const poll = async () => {
      try {
        const { data } = await checkHealth();
        setStatus(data);
      } catch {
        setStatus(null);
      } finally {
        setLoading(false);
      }
    };
    poll();
    const interval = setInterval(poll, 15000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className={`flex items-center gap-2 text-slate-400 text-sm ${className}`}>
        <Loader2 size={14} className="animate-spin" />
        Connecting to backend...
      </div>
    );
  }

  if (!status) {
    return (
      <div className={`flex items-center gap-2 text-rose-400 text-sm ${className}`}>
        <XCircle size={14} />
        Backend offline — start the FastAPI server
      </div>
    );
  }

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      {status.model_loaded ? (
        <span className="flex items-center gap-1.5 text-emerald-400 text-sm font-medium">
          <CheckCircle2 size={14} />
          Model ready
        </span>
      ) : (
        <span className="flex items-center gap-1.5 text-amber-400 text-sm font-medium">
          <AlertTriangle size={14} />
          Model unavailable
        </span>
      )}
      <span className="text-slate-600">|</span>
      <span className="flex items-center gap-1.5 text-emerald-400 text-sm">
        <Server size={12} />
        Backend online
      </span>
    </div>
  );
}
