import { API_BASE_URL } from './api';

export type UserSession = {
  id: number;
  full_name: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at?: string;
};

const STORAGE_KEY = 'gestion_proyecto_user';

export function getCurrentUser(): UserSession | null {
  if (typeof window === 'undefined') return null;
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as UserSession;
  } catch {
    return null;
  }
}

export function saveCurrentUser(user: UserSession) {
  if (typeof window === 'undefined') return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(user));
}

export function clearCurrentUser() {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(STORAGE_KEY);
}

export async function loginUser(email: string, password: string) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => null);
    throw new Error(error?.detail || 'Error al iniciar sesión');
  }

  const payload = await response.json();
  return payload.data as UserSession;
}
