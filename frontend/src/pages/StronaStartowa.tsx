import { useEffect, useState } from 'react'
import { api, type StatusSerwera } from '../api'

/** Sprawdza polaczenie z backendem przez GET /api/status. */
export default function StronaStartowa() {
  const [status, setStatus] = useState<StatusSerwera | null>(null)
  const [blad, setBlad] = useState<string | null>(null)

  useEffect(() => {
    api<StatusSerwera>('/status').then(setStatus).catch((e: Error) => setBlad(e.message))
  }, [])

  return (
    <section>
      <h1>System rejestracji czasu pracy</h1>
      {status && (
        <p className="ok">
          Backend działa. Czas serwera: {new Date(status.czasSerwera).toLocaleString('pl-PL')}
        </p>
      )}
      {blad && <p className="blad">Brak połączenia z backendem. {blad}</p>}
      {!status && !blad && <p>Sprawdzanie połączenia z backendem...</p>}
    </section>
  )
}
