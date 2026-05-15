import TaskCard from './task-card';

export default function KanbanColumn({ title, count, tasks }: { title: string; count: number; tasks?: Array<any> }) {
  const items = tasks?.filter((task) => task.status === title) ?? [];
  const display = items.length ? items : [{ id: 'empty', title: 'Sin tareas en esta columna', status: title, assignee: null, priority: null, favorite: false, comments: 0 }];

  return (
    <section className="min-w-[300px] rounded-3xl border border-slate-200 bg-slate-50 p-4 shadow-sm">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-700">{title}</h3>
          <p className="text-xs text-slate-500">{count} tarjetas</p>
        </div>
        <div className="h-8 w-8 rounded-full bg-white text-center text-sm font-semibold text-brand-700 shadow-sm">{count}</div>
      </div>
      <div className="space-y-3">
        {display.map((task) => (
          <TaskCard key={task.id} task={task} />
        ))}
      </div>
    </section>
  );
}
