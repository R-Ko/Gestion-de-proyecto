import Link from 'next/link';

export default function ActionButtons() {
  return (
    <div className="flex flex-wrap items-center gap-3">
      <Link href="#" className="rounded-2xl bg-brand-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-brand-400">
        + Crear
      </Link>
      <Link href="#" className="rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-100">
        Importar
      </Link>
    </div>
  );
}
