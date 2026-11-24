import { Link, useLocation } from 'react-router-dom';
import { Brain, FlaskConical, BookOpen, Menu, X } from 'lucide-react';
import { useState } from 'react';

const navLinks = [
  { to: '/', label: 'Home' },
  { to: '/analysis', label: 'Analyze' },
  { to: '/research', label: 'Research' },
];

export default function Navbar() {
  const { pathname } = useLocation();
  const [open, setOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 bg-navy-900/80 backdrop-blur-md border-b border-navy-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 group">
          <div className="w-8 h-8 rounded-lg bg-cyan-500 flex items-center justify-center group-hover:bg-cyan-400 transition-colors">
            <Brain size={18} className="text-navy-900" />
          </div>
          <span className="text-white font-bold text-lg tracking-tight">
            EyeTrace <span className="text-cyan-400">AI</span>
          </span>
        </Link>

        {/* Desktop nav */}
        <div className="hidden md:flex items-center gap-1">
          {navLinks.map(({ to, label }) => (
            <Link
              key={to}
              to={to}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                pathname === to
                  ? 'bg-navy-700 text-cyan-400'
                  : 'text-slate-300 hover:text-white hover:bg-navy-800'
              }`}
            >
              {label}
            </Link>
          ))}
          <Link to="/analysis" className="ml-4 btn-primary py-2 text-sm">
            <FlaskConical size={15} />
            Analyze Scanpath
          </Link>
        </div>

        {/* Mobile hamburger */}
        <button
          className="md:hidden p-2 text-slate-300 hover:text-white"
          onClick={() => setOpen(!open)}
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="md:hidden border-t border-navy-700 bg-navy-900 px-4 py-3 flex flex-col gap-2">
          {navLinks.map(({ to, label }) => (
            <Link
              key={to}
              to={to}
              onClick={() => setOpen(false)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                pathname === to
                  ? 'bg-navy-700 text-cyan-400'
                  : 'text-slate-300 hover:text-white hover:bg-navy-800'
              }`}
            >
              {label}
            </Link>
          ))}
          <Link to="/analysis" onClick={() => setOpen(false)} className="btn-primary text-sm mt-1">
            <FlaskConical size={15} />
            Analyze Scanpath
          </Link>
        </div>
      )}
    </nav>
  );
}
