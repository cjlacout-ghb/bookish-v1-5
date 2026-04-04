---
description: Estándares e implementación del DatePicker con diseño Noir/Art Déco.
---

# Implementación del DatePicker (Calendario)

Para mantener la consistencia estética del sistema *Noir/Art Déco*, cualquier componente de selección de fecha en la aplicación debe utilizar `react-datepicker` configurado con nuestra estandarización.

## 1. Importaciones Necesarias

Debes importar la librería, los estilos base y la localización (español):

```javascript
import DatePicker, { registerLocale } from 'react-datepicker'
import { es } from 'date-fns/locale/es'
import "react-datepicker/dist/react-datepicker.css"

// Registrar el idioma español para los nombres de días y meses
registerLocale('es', es)
```

## 2. Estructura y Estilos del Componente

**No uses el `input type="date"` nativo**. En su lugar, envuelve el `DatePicker` en un contenedor con la clase `.campo` si lleva etiqueta, y asegúrate de aplicar la clase `.campo__entrada` al componente para que herede los estilos de formulario de Bookish.

### Ejemplo de Implementación Estándar:

```javascript
<div className="campo">
  <label className="campo__etiqueta" htmlFor="mi-fecha">Fecha</label>
  <DatePicker
    // 1. Manejo seguro de la fecha local
    selected={fecha ? new Date(fecha + 'T12:00:00') : null}
    
    // 2. Conversión a string (YYYY-MM-DD) para el estado
    onChange={(date) => {
      const val = date ? date.toISOString().split('T')[0] : ''
      setFecha(val)
    }}
    
    // 3. Estilos y configuración visual
    className="campo__entrada"
    dateFormat="dd-MM-yyyy"
    locale="es"
    placeholderText="dd-mm-aaaa"
    autoComplete="off"
    id="mi-fecha"
    
    // 4. (Opcional) Restricciones, ej: no permitir fechas futuras
    maxDate={new Date()} 
  />
</div>
```

## 3. Puntos Críticos a Recordar

- **Manejo de Zonas Horarias**: Al convertir de un string (ej. `2026-04-04`) a un objeto `Date` en JavaScript, añade `T12:00:00` (ej: `new Date(fecha + 'T12:00:00')`). Esto previene el clásico bug donde la fecha se desplaza un día atrás en algunas zonas horarias.
- **Clase CSS del Input**: Añadir `className="campo__entrada"` es vital. Esto renderiza la caja de texto transparente con el borde elegante, en vez de un input blanco sin estilo.

## 4. Diseño Art Déco (Referencia de Estilos)

El aspecto *Noir* del calendario (colores oscuros, botones dorados, fuente Cinzel para el mes y bordes rectos) funciona invalidando los estilos por defecto de `react-datepicker` mediante `!important` utilizando las variables globales del sistema. 

Si necesitas depurar o alterar el diseño, busca bajo `/* ── React DatePicker (Custom Theme) ── */` en el `global.css`. Estos son los patrones CSS centrales utilizados:

```css
/* Contenedor principal: Fondo oscuro, borde dorado, bordes rectos */
.react-datepicker {
  background-color: var(--superficie) !important;
  color: var(--texto-primario) !important;
  border: 1px solid var(--oro-borde) !important;
  border-radius: 0px !important;
  font-family: var(--fuente-cuerpo) !important;
}

/* Cabecera (Mes y Año): Tipografía Cinzel, todo en mayúsculas color oro */
.react-datepicker__header {
  background-color: var(--sup-alta) !important;
  border-bottom: 1px solid var(--oro-oscuro) !important;
  border-radius: 0px !important;
}

.react-datepicker__current-month {
  font-family: var(--fuente-titular) !important;
  color: var(--oro-primario) !important;
  text-transform: uppercase !important;
  letter-spacing: 0.1em !important;
}

/* Día seleccionado: Fondo dorado puro, texto oscuro */
.react-datepicker__day--selected {
  background-color: var(--oro-primario) !important;
  color: var(--fondo) !important;
  font-weight: bold !important;
  border-radius: 0px !important;
}

/* Hover: Iluminación sutil */
.react-datepicker__day:hover {
  background-color: var(--sup-max) !important;
  color: var(--oro-primario) !important;
}

/* Días "fuera de mes": Atenuados y color oscuro */
.react-datepicker__day--outside-month {
  color: var(--oro-oscuro) !important;
  opacity: 0.4 !important;
}

/* Triángulo del Popover */
.react-datepicker__triangle {
  border-bottom-color: var(--oro-borde) !important;
}
```

*Cualquier mejora en el diseño del selector de fechas debe modificar estas reglas, manteniendo siempre el contraste alto y el enfoque arquitectónico (sin bordes redondeados).*
