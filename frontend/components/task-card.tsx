import Link from 'next/link';
import { Star, MessageCircle, CircleDot } from 'lucide-react';

export default function TaskCard({ task }: { task: any }) {
  return (
    <Link href={`/tareas/${task.id}`} className="group block rounded-3xl border border-slate-200 bg-white p-4 shadow-sm transition hover:border-brand-500 hover:shadow-md">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-sm font-semibold text-slate-900">{task.title}</p>
          <p className="mt-1 text-xs text-slate-500">#{task.id} · {task.status}</p>
        </div>
        <Star className={`h-4 w-4 ${task.is_favorite ? 'text-brand-500' : 'text-slate-300'}`} />
      </div>
      <div className="mt-4 flex items-center justify-between text-xs text-slate-600">
        <span className="inline-flex items-center gap-1 rounded-full bg-slate-100 px-2 py-1">
          <CircleDot className="h-3 w-3" />
          {task.priority ?? 'Medio'}
        </span>
        <span className="inline-flex items-center gap-1">
          <MessageCircle className="h-3 w-3" />
          {task.comments ?? 0}
        </span>
      </div>
    </Link>
  );
}
