import { Link } from 'react-router-dom';
import { Brain } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-navy-700 bg-navy-900 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <div className="w-7 h-7 rounded-lg bg-cyan-500 flex items-center justify-center">
                <Brain size={15} className="text-navy-900" />
              </div>
              <span className="font-bold text-white">EyeTrace <span className="text-cyan-400">AI</span></span>
            </div>
            <p className="text-slate-400 text-sm leading-relaxed">
              Academic research platform for ASD eye-tracking scanpath classification.
              Not for clinical use.
            </p>
          </div>

          {/* Links */}
          <div>
            <h3 className="text-white font-semibold mb-3 text-sm uppercase tracking-wider">Navigation</h3>
            <ul className="space-y-2">
              {[['/', 'Home'], ['/analysis', 'Analyze'], ['/research', 'Research']].map(([to, label]) => (
                <li key={to}>
                  <Link to={to} className="text-slate-400 hover:text-cyan-400 text-sm transition-colors">
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Disclaimer */}
          <div>
            <h3 className="text-white font-semibold mb-3 text-sm uppercase tracking-wider">Disclaimer</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              This tool is for academic and research purposes only. It must not be used as a
              clinical diagnostic instrument. ASD diagnosis requires comprehensive clinical evaluation
              by qualified professionals.
            </p>
          </div>
        </div>

        <div className="border-t border-navy-700 mt-8 pt-6 text-center text-slate-500 text-xs">
          © {new Date().getFullYear()} EyeTrace AI — Academic Research Project
        </div>
      </div>
    </footer>
  );
}
