import KanbanColumn from './kanban-column';

const columns = [
  { title: 'Backlog', count: 3 },
  { title: 'En progreso', count: 2 },
  { title: 'QA', count: 1 },
  { title: 'En validación', count: 0 },
  { title: 'Realizadas', count: 1 },
  { title: 'Desplegadas en Dev/Terminadas', count: 1 },
];

export default function KanbanBoard({ tasks }: { tasks?: Array<any> }) {
  return (
    <div className="flex min-w-full gap-4 overflow-x-auto pb-4 no-scrollbar">
      {columns.map((column) => (
        <KanbanColumn key={column.title} title={column.title} count={column.count} tasks={tasks} />
      ))}
    </div>
  );
}
