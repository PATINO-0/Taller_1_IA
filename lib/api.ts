const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "/api";

export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, init);

  if (!response.ok) {
    throw new Error(`Error de API: ${response.status}`);
  }

  return (await response.json()) as T;
}

