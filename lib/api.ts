const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

export async function postJson<TResponse>(
  path: string,
  body: unknown,
): Promise<TResponse> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      detail: "Error inesperado",
    }));

    throw new Error(
      error.detail ?? "No fue posible ejecutar el algoritmo.",
    );
  }

  return response.json() as Promise<TResponse>;
}

