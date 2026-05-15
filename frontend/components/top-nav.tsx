import { Settings, Bell } from 'lucide-react';

export default function TopNav() {
  return (
    <header className="flex items-center justify-between gap-4 rounded-b-2xl border-b border-slate-200 bg-brand-900 px-6 py-4 text-slate-100 shadow-sm">
      <div>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-300">Sistema interno</p>
        <h1 className="text-2xl font-semibold">Gestión de Proyectos</h1>
      </div>
      <div className="flex items-center gap-3 text-slate-100">
        <button className="rounded-2xl bg-slate-800/80 px-4 py-2 text-sm transition hover:bg-slate-700">Notificaciones</button>
        <Bell className="h-5 w-5" />
        <Settings className="h-5 w-5" />
      </div>
    </header>
  );
}
