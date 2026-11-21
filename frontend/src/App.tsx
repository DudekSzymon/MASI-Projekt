import { NavLink, Route, Routes } from 'react-router-dom'
import StronaStartowa from './pages/StronaStartowa'
import PanelPracownika from './pages/PanelPracownika'
import PanelKierownika from './pages/PanelKierownika'
import PanelAdministratora from './pages/PanelAdministratora'

export default function App() {
  return (
    <>
      <header className="naglowek">
        <strong>Rejestracja czasu pracy</strong>
        <nav>
          <NavLink to="/" end>Start</NavLink>
          <NavLink to="/pracownik">Pracownik</NavLink>
          <NavLink to="/kierownik">Kierownik</NavLink>
          <NavLink to="/administrator">Administrator</NavLink>
        </nav>
      </header>
      <main className="tresc">
        <Routes>
          <Route path="/" element={<StronaStartowa />} />
          <Route path="/pracownik" element={<PanelPracownika />} />
          <Route path="/kierownik" element={<PanelKierownika />} />
          <Route path="/administrator" element={<PanelAdministratora />} />
        </Routes>
      </main>
    </>
  )
}
