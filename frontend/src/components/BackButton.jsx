import { useNavigate, useLocation } from 'react-router-dom'

export default function BackButton() {
  const navigate = useNavigate();
  const location = useLocation();

  // No mostramos el botón de retroceso en la landing page principal
  if (location.pathname === '/') {
    return null;
  }

  return (
    <button 
      className="btn-back-global animar-entrada" 
      onClick={() => navigate(-1)}
      title="Volver atrás"
    >
      <span className="material-symbols-outlined">arrow_back</span>
    </button>
  )
}
