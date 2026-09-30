# language: es
@example
Característica: Página de ejemplo
  Como equipo de automatización
  quiero ejecutar un escenario local sin depender de Internet
  para comprobar que el template está correctamente configurado.

  Escenario: Validar el encabezado de la página de ejemplo
    Dado que el usuario abre la aplicación de ejemplo
    Entonces se muestra el encabezado "Example Domain"
