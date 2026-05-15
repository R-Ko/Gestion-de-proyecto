'use client';

import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';
import { loginUser, saveCurrentUser } from '../../lib/auth';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      const user = await loginUser(email, password);
      saveCurrentUser(user);
      router.push('/proyectos');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No se pudo iniciar sesión');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-100 py-16 px-4">
      <div className="mx-auto flex w-full max-w-md flex-col gap-8 rounded-3xl bg-white p-10 shadow-xl">
        <div className="text-center">
          <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-3xl bg-gradient-to-br from-cyan-500 to-sky-700 text-white shadow-lg">
            <span className="text-3xl font-bold">G</span>
          </div>
          <h1 className="text-2xl font-semibold text-slate-900">Iniciar sesión</h1>
          <p className="mt-2 text-sm text-slate-500">Accede con tu correo y contraseña para entrar al sistema.</p>
        </div>

        <form onSubmit={handleSubmit} className="grid gap-4">
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
            {loading ? 'Iniciando...' : 'Iniciar sesión'}
          </button>

          <div className="flex items-center justify-between text-sm text-slate-600">
            <a href="/register" className="text-sky-600 hover:text-sky-700">Crear cuenta</a>
            <a href="/cambiar-contrasena" className="text-slate-500 hover:text-slate-700">Cambiar contraseña</a>
          </div>
        </form>
      </div>
    </main>
  );
}
