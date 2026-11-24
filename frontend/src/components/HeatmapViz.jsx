export default function HeatmapViz({ b64, title = 'Occlusion Sensitivity Heatmap' }) {
  return (
    <div className="card">
      <h3 className="text-white font-semibold mb-1">{title}</h3>
      <p className="text-slate-400 text-sm mb-4">
        Warm (red/yellow) regions indicate image areas whose occlusion most reduces the
        model's ASD probability — i.e., regions most influential to this classification.
        This is a model attribution map, not a clinical gaze heatmap.
      </p>
      {b64 ? (
        <img
          src={`data:image/png;base64,${b64}`}
          alt="Occlusion sensitivity heatmap"
          className="w-full max-w-sm mx-auto rounded-xl border border-navy-700 object-contain"
        />
      ) : (
        <div className="w-full h-40 flex items-center justify-center rounded-xl border border-navy-700 bg-navy-800/50 text-slate-500 text-sm">
          Heatmap not available
        </div>
      )}
    </div>
  );
}
