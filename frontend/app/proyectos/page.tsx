'use client';

import { useEffect, useState } from 'react';
import TopNav from '@/components/top-nav';
import ModuleMenu from '@/components/module-menu';
import SearchBar from '@/components/search-bar';
import FilterBar from '@/components/filter-bar';
import ProjectGrid from '@/components/project-grid';
import { fetcher } from '@/lib/api';
import { getCurrentUser } from '@/lib/auth';

async function getProjects(userId: number) {
  try {
    return await fetcher<any[]>(`/projects?user_id=${userId}`);
  } catch {
    return null;
  }
}

export default function ProjectsPage() {
  const [projects, setProjects] = useState<any[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const user = getCurrentUser();
    if (!user) {
      setError('Debes iniciar sesión para ver tus proyectos.');
      setLoading(false);
      return;
    }

    getProjects(user.id)
      .then((data) => {
        if (data === null) {
          setError('No se pudieron cargar los proyectos.');
        } else {
          setProjects(data);
        }
      })
      .catch(() => {
        setError('No se pudieron cargar los proyectos.');
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-slate-100 px-4 py-6 lg:px-8">
      <div className="mx-auto max-w-[1500px] space-y-6">
        <TopNav />
        <div className="rounded-[2rem] bg-slate-100 p-6 shadow-sm">
          <ModuleMenu />
          <div className="mt-6 grid gap-5 xl:grid-cols-[1.2fr_0.8fr]">
            <div className="space-y-5">
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex flex-wrap items-center justify-between gap-4">
                  <div>
                    <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Proyectos</p>
                    <h2 className="mt-2 text-3xl font-semibold text-slate-900">Estado de portafolio</h2>
                  </div>
                  <div className="flex flex-wrap gap-3">
                    <button className="rounded-2xl bg-brand-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-brand-400">+ Nuevo proyecto</button>
                    <button className="rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-100">Exportar</button>
                  </div>
                </div>
              </div>
              <div className="grid gap-4 lg:grid-cols-[1fr_0.6fr]">
                <SearchBar placeholder="Buscar proyectos, códigos o responsables" />
                <FilterBar />
              </div>
            </div>
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Resumen rápido</p>
              <div className="mt-5 grid gap-4 sm:grid-cols-2">
                {['Proyectos activos', 'Tareas abiertas', 'Tickets pendientes', 'Favoritos'].map((label) => (
                  <div key={label} className="rounded-3xl bg-slate-50 p-4 text-sm font-semibold text-slate-800">{label}</div>
                ))}
              </div>
            </div>
          </div>
        </div>
        <section className="space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Catálogo</p>
              <h3 className="text-2xl font-semibold text-slate-900">Proyectos de la empresa</h3>
            </div>
            <p className="text-sm text-slate-500">Tarjetas completamente clickeables</p>
          </div>
          {loading ? (
            <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center text-slate-500">Cargando proyectos...</div>
          ) : error ? (
            <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center text-slate-500">{error}</div>
          ) : projects === null ? (
            <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center text-slate-500">No se pudieron cargar los proyectos. Intenta nuevamente más tarde.</div>
          ) : projects.length === 0 ? (
            <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center text-slate-500">No hay proyectos disponibles.</div>
          ) : (
            <ProjectGrid projects={projects} />
          )}
        </section>
      </div>
    </div>
  );
}
