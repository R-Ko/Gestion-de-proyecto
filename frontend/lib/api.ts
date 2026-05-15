export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '/api/v1';

export async function fetcher<T>(path: string) {
  const response = await fetch(`${API_BASE_URL}${path}`, { cache: 'no-store' });
  if (!response.ok) {
    throw new Error(`Error al cargar ${path}`);
  }
  const payload = await response.json();
  return payload.data as T;
}
