'use client';

import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';
import { saveCurrentUser } from '../../lib/auth';
import { API_BASE_URL } from '../../lib/api';

export default function RegisterPage() {
  const router = useRouter();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ full_name: fullName, email, password }),
      });

      if (!response.ok) {
        const data = await response.json().catch(() => null);
        throw new Error(data?.detail || 'No se pudo crear la cuenta');
      }

      const payload = await response.json();
      saveCurrentUser(payload.data);
      router.push('/proyectos');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No se pudo crear la cuenta');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-100 py-16 px-4">
      <div className="mx-auto flex w-full max-w-md flex-col gap-8 rounded-3xl bg-white p-10 shadow-xl">
        <div className="text-center">
          <h1 className="text-2xl font-semibold text-slate-900">Crear nueva cuenta</h1>
          <p className="mt-2 text-sm text-slate-500">Registra tu nombre, correo y contraseña para empezar.</p>
        </div>

        <form onSubmit={handleSubmit} className="grid gap-4">
          <label className="space-y-2 text-sm font-medium text-slate-700">
            <span>Nombre completo</span>
            <input
              value={fullName}
              onChange={(event) => setFullName(event.target.value)}
              required
              className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            />
          </label>

          <label className="space-y-2 text-sm font-medium text-slate-700">
            <span>Correo electrónico</span>
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
              className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            />
          </label>

          <label className="space-y-2 text-sm font-medium text-slate-700">
            <span>Contraseña</span>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
              className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            />
          </label>

          {error ? <p className="text-sm text-red-600">{error}</p> : null}

          <button
            type="submit"
            disabled={loading}
            className="rounded-2xl bg-sky-600 px-4 py-3 text-white transition hover:bg-sky-700 disabled:cursor-not-allowed disabled:bg-slate-400"
          >
            {loading ? 'Creando cuenta...' : 'Crear cuenta'}
          </button>

          <div className="text-center text-sm text-slate-600">
            <a href="/login" className="text-sky-600 hover:text-sky-700">¿Ya tienes cuenta? Inicia sesión</a>
          </div>
        </form>
      </div>
    </main>
  );
}
