# Especificaciones de Requerimientos del Sistema (SRS)

## Contexto del Proyecto
* **Caso de Estudio:** Policlínico EsSalud "Juan José Rodríguez Lazo" (Chorrillos).
* **Objetivo:** Optimizar el registro de asegurados, agendamiento de citas y control de farmacia mediante una aplicación de escritorio local, inmutable y segura.

## Requerimientos Funcionales (R1 - R6)

| Código | Requerimiento | Descripción | Paradigma Principal |
| :--- | :--- | :--- | :--- |
| **R1** | **Registro de Pacientes** | Registro y consulta de asegurados con código único para evitar duplicidad de fichas médicas. | POO + Funcional |
| **R2** | **Citas sin Solapamiento** | Agendamiento validando disponibilidad en tiempo real de médicos y consultorios. | POO + Eventos |
| **R3** | **Historial Clínico Seguro** | Vinculación inmutable entre el paciente y su historial con validación de congruencia médica. | POO + Funcional |
| **R4** | **Cancelación y Liberación** | Anulación ágil de turnos y liberación instantánea del cupo para listas de espera. | Eventos + Funcional |
| **R5** | **Control de Medicamentos** | Monitoreo de inventario por lotes y caducidad con alertas de stock mínimo. | POO + Funcional |
| **R6** | **Operatividad Local y RBAC** | Funcionamiento autónomo offline en ventanilla y control de acceso basado en roles. | POO + Funcional |

## Restricciones de Sistema

1. **Protección de Datos (Ley N.° 29733):** Prohibido almacenar DNI o diagnósticos en texto plano; aplicación obligatoria de algoritmos de cifrado SHA-256.
2. **Hardware de Bajos Recursos:** Rendimiento optimizado para computadoras con memoria RAM $\le$ 4 GB.
3. **Código Abierto y Control de Versiones:** Desarrollado en Python 3.x con repositorio público en GitHub ($\ge$ 10 commits descriptivos).
4. **Almacenamiento Local:** Base de datos relacional SQLite (`gestion_essalud.db`) sin costo de licencias ni dependencia de conexión a Internet.

## Criterios de Éxito Medibles

* **Tiempo de atención en ventanilla:** Reducción de 10 minutos a $< 2$ minutos por asegurado.
* **Integridad de fichas:** $0\%$ de errores por cruce de diagnósticos o identificación.
* **Recuperación de cupos:** Recuperación de al menos el $25\%$ de las citas canceladas.
