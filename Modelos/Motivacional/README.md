# Componentes Stakeholder (Motivation)

* **Stakeholder**: grupo o persona con interés o preocupación en la arquitectura. (Definición en la guía y cartillas oficiales.) ([www.opengroup.org][1])
* **Driver**: condición interna/externa que motiva a la organización a definir objetivos y realizar cambios. ([www.opengroup.org][2])
* **Assessment**: resultado de un análisis del estado frente a un *driver* (típicamente SWOT). ([www.opengroup.org][2])
* **Goal**: declaración de intención/dirección o estado deseado de alto nivel. ([www.opengroup.org][2])
* **Outcome**: resultado final logrado (efecto/consecuencia medible). ([www.opengroup.org][2])
* *(Opcional pero útil en este punto de la arquitectura)*

  * **Principle**: criterio/lineamiento general que guía decisiones. ([www.opengroup.org][2])
  * **Requirement**: necesidad concreta que el sistema debe cumplir para materializar metas/principios. ([www.opengroup.org][2])
  * **Constraint**: limitación a la arquitectura o a la realización de metas (p. ej., normativa, presupuesto). ([www.opengroup.org][1])

---

# Relaciones recomendadas (y cuándo usarlas)

> En Motivation, la **relación clave** es **Influence** (con signo **+ / −** para indicar efecto positivo o negativo). También se usan **Realization**, **Aggregation/Composition**, **Association** y, ocasionalmente, **Specialization**. ([www.opengroup.org][1])

* **Stakeholder — Association → Driver**
  Úsala para expresar que un stakeholder “tiene interés/concern” en un driver. La especificación y material de referencia muestran *stakeholders* asociados a *drivers* y *assessments*. ([sparxsystems.com][3])

* **Assessment — Influence (+/−) → Goal**
  Un diagnóstico (p. ej., “Baja comprensión pública”) **influye** en los objetivos (elevar alfabetización ambiental, etc.). **Influence** puede ir entre cualquier elemento de motivación y admite **+/−**. ([www.opengroup.org][1])

* **Driver — Influence (+/−) → Goal**
  Un driver como “Exigencia regulatoria” empuja objetivos de cumplimiento; “Presupuesto limitado” puede influir **−**. ([www.opengroup.org][1])

* **Goal — Aggregation/Composition → Sub-goals**
  Descompón metas de alto nivel en sub-metas (p. ej., “Transparencia de datos” → “APIs abiertas”, “Panel ciudadano”). **Aggregation/Composition** son las relaciones estructurales válidas para *goal decomposition*. ([www.opengroup.org][2])

* **Outcome — Realization → Goal**
  Un *outcome* concreto (p. ej., “Panel público en producción”) **realiza** la meta abstracta (“Informar a la ciudadanía”). Este patrón es común en los *goal realization viewpoints*. ([sparxsystems.com][4])

* **Principle — Influence (+) → Goal**
  Los principios (p. ej., “Open by default”) guían y refuerzan el logro de metas. ([www.opengroup.org][1])

* **Requirement — Realization → Principle / Goal**
  Requisitos específicos (p. ej., “API debe exponer PM2.5 en ≤60 s”) **realizan** principios/objetivos. ([www.opengroup.org][1])

* **Constraint — Influence (−) → Goal / Requirement**
  Las restricciones (leyes, presupuesto, SLA heredados) **limitan** la realización de metas y requisitos. ([www.opengroup.org][1])

* **Association (genérica)**
  Úsala cuando la semántica precisa no aplique (p. ej., vincular un *assessment* a su *driver* como “assessment de este driver”). La propia documentación de herramientas muestra **assessments asociados a drivers**. ([sparxsystems.com][3])

* **Specialization (cuando se necesite)**
  Para definir variantes más específicas (p. ej., *Goal* “Mejorar UX” → *Goal* especializado “Mejorar accesibilidad”). ([www.opengroup.org][1])

---

# Cómo trazar las relaciones en **Archi** (Magic Connector)

1. Selecciona la herramienta **Magic Connector** → 2) Clic en el elemento origen → 3) Clic en el destino (o en lienzo para crear elemento+relación) → 4) En el menú en cascada, Archi mostrará **solo** las relaciones permitidas entre esos dos tipos; elige la más adecuada. ([ArchiMate Tool][5])

---

## Correcciones y aclaraciones Docente

* **Goals**: enunciarlos como **acciones** (“Incrementar…”, “Reducir…”, “Asegurar…”).
* **Outcomes**: deben ser **resultados observables** de esas acciones (idealmente con indicador/umbral).


[1]: https://www.opengroup.org/sites/default/files/docs/downloads/n221p.pdf?utm_source=chatgpt.com "ArchiMate 3.2 Specification Reference Cards"
[2]: https://www.opengroup.org/sites/default/files/docs/downloads/n190p_5.pdf?utm_source=chatgpt.com "ArchiMate® 3.1 Specification"
[3]: https://sparxsystems.com/resources/user-guides/16.1/model-domains/languages/archimate.pdf?utm_source=chatgpt.com "ArchiMate Modeling Language"
[4]: https://sparxsystems.com/resources/tutorials/archimate/?utm_source=chatgpt.com "Archimate Tutorial - Viewpoint Examples"
[5]: https://www.archimatetool.com/downloads/archi/Archi%20User%20Guide.pdf?utm_source=chatgpt.com "Archi User Guide"
