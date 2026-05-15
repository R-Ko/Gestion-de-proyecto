export default function TaskTabs() {
  const sections = [
    { title: 'Descripción', body: 'Esta tarea forma parte del flujo central del proyecto y contiene todos los requerimientos detallados.' },
    { title: 'Dependencias', body: 'Depende de la aprobación de documentación, recursos asignados y ambiente de pruebas.' },
    { title: 'Partes de horas', body: '20h estimadas, 8h completadas. Control de tiempos con seguimiento en cada iteración.' },
    { title: 'Información extra', body: 'Notas técnicas, bloqueos y comentarios internos del equipo de desarrollo.' },
  ];

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-4 flex flex-wrap gap-3">
        {sections.map((section) => (
          <button key={section.title} className="rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-100">
            {section.title}
          </button>
        ))}
      </div>
      <div className="space-y-5">
        {sections.map((section) => (
          <div key={section.title}>
            <h3 className="text-base font-semibold text-slate-900">{section.title}</h3>
            <p className="mt-2 text-sm leading-7 text-slate-600">{section.body}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
