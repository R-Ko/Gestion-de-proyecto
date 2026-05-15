import TimelineItem from './timeline-item';

const actions = [
  { label: 'Enviar mensaje', color: 'bg-brand-500' },
  { label: 'Poner una nota', color: 'bg-slate-700' },
  { label: 'Planificar actividad', color: 'bg-brand-400' },
];

const events = [
  { author: 'Ana Romero', time: 'Hace 20 min', content: 'Se agregó un comentario nuevo al ticket de integración.' },
  { author: 'Carlos Vega', time: 'Hace 1 hora', content: 'La tarea fue actualizada al estado En progreso.' },
  { author: 'Equipo QA', time: 'Ayer', content: 'Se validó el módulo en ambiente de pruebas.' },
];

export default function ActivitySidebar() {
  return (
    <aside className="space-y-5 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm md:w-[380px]">
      <div className="space-y-3">
        {actions.map((action) => (
          <button key={action.label} className={`w-full rounded-2xl px-4 py-3 text-sm font-semibold text-white ${action.color} transition hover:opacity-95`}>
            {action.label}
          </button>
        ))}
      </div>
      <div className="rounded-3xl bg-slate-50 p-4">
        <p className="text-sm font-semibold text-slate-900">Timeline de actividad</p>
        <div className="mt-4 space-y-4">
          {events.map((event) => (
            <TimelineItem key={event.time + event.author} {...event} />
          ))}
        </div>
      </div>
    </aside>
  );
}
