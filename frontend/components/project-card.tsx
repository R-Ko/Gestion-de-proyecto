import Link from 'next/link';
import { Star, Briefcase, CalendarCheck, MessageCircle } from 'lucide-react';

interface ProjectCardProps {
  id: number;
  name: string;
  type: string;
  productLine: string;
  updatedAt: string;
  lastLogDate: string;
  taskCount: number;
  ticketCount: number;
  favorite: boolean;
}

export default function ProjectCard({ id, name, type, productLine, updatedAt, lastLogDate, taskCount, ticketCount, favorite }: ProjectCardProps) {
  return (
    <Link href={`/proyectos/${id}/tareas`} className="group block rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.24em] text-slate-500">{type}</p>
          <h2 className="mt-2 text-lg font-semibold text-slate-900">{name}</h2>
        </div>
        <div className="rounded-full bg-slate-100 p-2 text-brand-700">
          <Star className="h-4 w-4" />
        </div>
      </div>
      <div className="mt-4 grid gap-3 text-sm text-slate-600">
        <div className="flex items-center gap-2">
          <Briefcase className="h-4 w-4" />
          <span>{productLine}</span>
        </div>
        <div className="flex items-center gap-2">
          <CalendarCheck className="h-4 w-4" />
          <span>Actualizado {updatedAt}</span>
        </div>
        <div className="flex items-center gap-2">
          <MessageCircle className="h-4 w-4" />
          <span>Último log {lastLogDate}</span>
        </div>
      </div>
      <div className="mt-5 flex items-center justify-between rounded-3xl bg-slate-50 px-4 py-3 text-sm text-slate-700">
        <span>Tareas {taskCount}</span>
        <span>Tickets {ticketCount}</span>
      </div>
    </Link>
  );
}
