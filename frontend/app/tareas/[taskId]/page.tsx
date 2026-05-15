import TopNav from '@/components/top-nav';
import TaskDetailHeader from '@/components/task-detail-header';
import TaskMetaGrid from '@/components/task-meta-grid';
import TaskTabs from '@/components/task-tabs';
import ActivitySidebar from '@/components/activity-sidebar';
import { fetcher } from '@/lib/api';

interface PageProps {
  params: { taskId: string };
}

async function getTask(taskId: string) {
  try {
    return await fetcher<any>(`/tasks/${taskId}`);
  } catch {
    return null;
  }
}

export default async function TaskDetailPage({ params }: PageProps) {
  const task = await getTask(params.taskId);

  const metaData = [
    { label: 'ID', value: task?.id?.toString() ?? 'N/A' },
    { label: 'Proyecto', value: 'Migración ERP' },
    { label: 'Asignada a', value: 'Carlos Vega' },
    { label: 'Sprint', value: task?.sprint ?? 'S1' },
    { label: 'Fecha límite', value: task?.due_date ?? '2026-06-05' },
    { label: 'Inicio', value: task?.project_start_date ?? '2026-05-01' },
    { label: 'Plazo', value: task?.project_deadline ?? '2026-06-30' },
    { label: 'Categorías', value: task?.category ?? 'Configuración' },
    { label: 'Recordatorio', value: task?.reminder ?? '2026-06-01' },
    { label: 'Prioridad', value: task?.priority ?? 'Alta' },
  ];

  return (
    <div className="min-h-screen bg-slate-100 px-4 py-6 lg:px-8">
      <div className="mx-auto max-w-[1500px] space-y-6">
        <TopNav />
        <div className="rounded-[2rem] bg-slate-100 p-6 shadow-sm">
          <div className="grid gap-6 xl:grid-cols-[1.4fr_0.8fr]">
            <div className="space-y-6">
              <TaskDetailHeader title={task?.title ?? 'Detalle de tarea'} />
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <TaskMetaGrid data={metaData} />
              </div>
              <TaskTabs />
            </div>
            <ActivitySidebar />
          </div>
        </div>
      </div>
    </div>
  );
}
