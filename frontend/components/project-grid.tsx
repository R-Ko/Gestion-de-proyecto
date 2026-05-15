import ProjectCard from './project-card';

const placeholder = [
  { id: 1, name: 'Migración ERP', type: 'Consultoría', productLine: 'ERP Core', updatedAt: 'hace 2h', lastLogDate: 'hoy', taskCount: 12, ticketCount: 4, favorite: true },
  { id: 2, name: 'Dashboard Comercial', type: 'Software', productLine: 'Analytics', updatedAt: 'ayer', lastLogDate: 'hace 1d', taskCount: 8, ticketCount: 2, favorite: false },
  { id: 3, name: 'Control de Calidad', type: 'Operaciones', productLine: 'QA Suite', updatedAt: '2 días', lastLogDate: 'hace 5h', taskCount: 14, ticketCount: 7, favorite: false },
];

export default function ProjectGrid({ projects }: { projects?: Array<any> }) {
  const items = projects ?? placeholder;

  return (
    <div className="grid gap-4 xl:grid-cols-3 lg:grid-cols-2 md:grid-cols-2 sm:grid-cols-1">
      {items.map((project) => (
        <ProjectCard key={project.id} {...project} />
      ))}
    </div>
  );
}
