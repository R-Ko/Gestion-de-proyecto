export default function TaskMetaGrid({ data }: { data: Array<{ label: string; value: string }> }) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {data.map((item) => (
        <div key={item.label} className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
          <p className="text-xs uppercase tracking-[0.18em] text-slate-500">{item.label}</p>
          <p className="mt-2 text-sm font-semibold text-slate-900">{item.value}</p>
        </div>
      ))}
    </div>
  );
}
