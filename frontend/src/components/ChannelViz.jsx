export default function ChannelViz({ b64, label, description, color }) {
  const colorClass = {
    red: 'border-red-500/40 bg-red-500/10',
    green: 'border-emerald-500/40 bg-emerald-500/10',
    blue: 'border-blue-500/40 bg-blue-500/10',
    default: 'border-navy-600 bg-navy-700/50',
  }[color] || 'border-navy-600 bg-navy-700/50';

  const textColor = {
    red: 'text-red-400',
    green: 'text-emerald-400',
    blue: 'text-blue-400',
    default: 'text-slate-300',
  }[color] || 'text-slate-300';

  return (
    <div className={`rounded-xl border p-4 ${colorClass}`}>
      <div className={`font-semibold text-sm mb-1 ${textColor}`}>{label}</div>
      <p className="text-slate-400 text-xs mb-3">{description}</p>
      {b64 ? (
        <img
          src={`data:image/png;base64,${b64}`}
          alt={label}
          className="w-full rounded-lg border border-navy-700 object-contain"
        />
      ) : (
        <div className="w-full h-32 flex items-center justify-center rounded-lg border border-navy-700 bg-navy-800 text-slate-500 text-xs">
          Not available
        </div>
      )}
    </div>
  );
}
