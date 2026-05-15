export default function FilterBar() {
  const pills = ['Filtros', 'Agrupar por', 'Favoritos'];

  return (
    <div className="flex flex-wrap items-center gap-3 rounded-3xl bg-white px-4 py-3 shadow-sm">
      {pills.map((pill) => (
        <button key={pill} className="rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] text-slate-600 transition hover:border-brand-500 hover:text-brand-900">
          {pill}
        </button>
      ))}
    </div>
  );
}
