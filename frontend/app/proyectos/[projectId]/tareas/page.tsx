import TopNav from '@/components/top-nav';
import SearchBar from '@/components/search-bar';
import FilterBar from '@/components/filter-bar';
import ActionButtons from '@/components/action-buttons';
import KanbanBoard from '@/components/kanban-board';
import { fetcher } from '@/lib/api';

interface PageProps {
  params: { projectId: string };
}

async function getTasks(projectId: string) {
  try {
    return await fetcher<any[]>(`/projects/${projectId}/tasks`);
  } catch {
    return null;
  }
}

export default async function ProjectTasksPage({ params }: PageProps) {
  const tasks = await getTasks(params.projectId);

  return (
    <div className="min-h-screen bg-slate-100 px-4 py-6 lg:px-8">
      <div className="mx-auto max-w-[1500px] space-y-6">
        <TopNav />
        <div className="rounded-[2rem] bg-slate-100 p-6 shadow-sm">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Proyectos / Tareas</p>
                <h1 className="mt-2 text-3xl font-semibold text-slate-900">Nombre del proyecto activo</h1>
              </div>
              <ActionButtons />
            </div>
            <div className="mt-6 grid gap-4 lg:grid-cols-[1fr_0.4fr]">
              <div className="space-y-4">
                <SearchBar placeholder="Buscar tareas dentro del proyecto" />
                <FilterBar />
              </div>
              <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
                <p className="font-semibold text-slate-900">Acciones rápidas</p>
                <p className="mt-2">Vistas, filtros y estados del tablero kanban.</p>
              </div>
            </div>
          </div>
          <div className="mt-6 rounded-3xl border border-slate-200 bg-slate-50 p-6 shadow-sm">
            <div className="mb-4 flex items-center justify-between gap-3">
              <div>
                <h2 className="text-xl font-semibold text-slate-900">Tablero Kanban</h2>
                <p className="text-sm text-slate-500">Flujo de tareas por estado</p>
              </div>
              <div className="flex items-center gap-3 text-slate-600">
                <span className="rounded-full bg-white px-3 py-2 text-xs font-semibold uppercase tracking-[0.24em]">Vista estándar</span>
                <span className="rounded-full bg-white px-3 py-2 text-xs font-semibold uppercase tracking-[0.24em]">Filtrado</span>
              </div>
            </div>
            {tasks === null ? (
              <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center text-slate-500">No se pudo cargar el tablero. Verifica la conexión al backend.</div>
            ) : (
              <KanbanBoard tasks={tasks} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
