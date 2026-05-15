import { Star } from 'lucide-react';

export default function TaskDetailHeader({ title }: { title: string }) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-semibold text-slate-900">{title}</h1>
          <p className="mt-2 text-sm text-slate-500">Detalle de tarea y seguimiento interno del proyecto</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-700 transition hover:bg-slate-100">Editar</button>
          <button className="rounded-2xl bg-brand-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-brand-400">Crear</button>
          <span className="rounded-full bg-slate-100 p-3 text-brand-700"><Star className="h-5 w-5" /></span>
        </div>
      </div>
    </div>
  );
}
