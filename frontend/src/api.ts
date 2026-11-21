// Wspolna funkcja do wywolan REST API backendu.
// Pozniej dojdzie tu dolaczanie tokenu JWT do naglowka Authorization.

export async function api<T>(sciezka: string, opcje: RequestInit = {}): Promise<T> {
  const odpowiedz = await fetch(`/api${sciezka}`, {
    ...opcje,
    headers: { 'Content-Type': 'application/json', ...opcje.headers },
  })
  if (!odpowiedz.ok) {
    throw new Error(`Blad ${odpowiedz.status}: ${await odpowiedz.text()}`)
  }
  return odpowiedz.json() as Promise<T>
}

export interface StatusSerwera {
  aplikacja: string
  status: string
  czasSerwera: string
}
