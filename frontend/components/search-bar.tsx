import { Search } from 'lucide-react';

export default function SearchBar({ placeholder = 'Buscar...' }: { placeholder?: string }) {
  return (
    <div className="relative flex items-center gap-3 rounded-3xl border border-slate-200 bg-white px-4 py-2 shadow-sm">
      <Search className="h-4 w-4 text-slate-400" />
      <input className="w-full bg-transparent text-sm text-slate-900 outline-none" placeholder={placeholder} />
    </div>
  );
}
