import Link from 'next/link';

const items = [
  { label: 'Proyectos', href: '/proyectos' },
  { label: 'Todas las tareas', href: '/tareas/1' },
  { label: 'Hitos', href: '/proyectos' },
  { label: 'Sprint', href: '/proyectos' },
];

export default function ModuleMenu() {
  return (
    <nav className="flex flex-wrap gap-2 rounded-3xl bg-slate-50 px-4 py-3 shadow-sm">
      {items.map((item) => (
        <Link key={item.href} href={item.href} className="rounded-full px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-brand-500/10 hover:text-brand-900">
          {item.label}
        </Link>
      ))}
    </nav>
  );
}
