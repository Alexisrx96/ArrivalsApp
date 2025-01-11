# Requerimientos

1. Análisis y Diseño
    - [ ] Realiza un análisis técnico y describe la solución propuesta:
        - [ ] Herramientas, tecnologías y patrones de diseño a utilizar.
        - [ ] Justificación detrás de las decisiones técnicas.
    - [ ] Define la arquitectura de la solución (diagrama de componentes, flujos de datos o diagramas CQRS).
        - [ ] Requisitos adicionales: Implementar principios SOLID y al menos un patrón de diseño (ejemplo: repositorio, estrategia, fábrica).
        - [ ] Considera cómo mejorar la seguridad de la solución utilizando al menos una práctica de OWASP (por ejemplo, sanitización de entradas, protección CSRF o validación robusta).

2. Implementación
    - [ ] Desarrolla un CRUD funcional con operaciones básicas (crear, leer, actualizar y eliminar datos).
    - [ ] Datos masivos: Genera al menos 100,000 registros aleatorios para medir el rendimiento puede ser al consumir un endpoint o hacer click a un boton.
    - [ ] CQRS: Implementa:
        - [ ] Base de datos para escritura (PostgreSQL recomendado).
        - [ ] Base de datos para lectura (MongoDB   o Redis recomendados). Si usas otra combinación, justifica tu elección.
    - [ ] Reporte:
        - [ ] Diseña un reporte que muestre métricas relevantes del problema seleccionado.
    - [ ] Implementa SOLID: Refleja los principios en el diseño de clases y manejo de dependencias.
    - [ ] Incluye una práctica OWASP: Por ejemplo:
        - [ ] Sanitización de entradas para evitar inyecciones de SQL.
        - [ ] Uso de autenticación segura (JWT, OAuth).
        - [ ] Implementación de validaciones robustas en los datos recibidos.
        - [ ] Cualquier otra.

3. Uso de Docker
    - [ ] Proporciona un archivo docker-compose.yml o Dockerfile para levantar la aplicación y los servicios necesarios.
    - [ ] Asegúrate de que la solución sea fácilmente ejecutable en cualquier entorno que soporte Docker, por lo que el uso de DevContainers es preferible.

4. Uso de Git
    - [ ] Usa Git para gestionar el código del proyecto.
    - [ ] Envía la URL del repositorio en GitHub o GitLab (perfil público preferido).
    - [ ] Incluye:
        - [ ] Código fuente estructurado.
        - [ ] Archivos de configuración para Docker.
        - [ ] Documentación (README y Diagramas)

5. Frontend (opcional)
   - [ ] Implementa una interfaz básica para interactuar con el CRUD y el reporte. Puedes elegir cualquier tecnología, pero recomendamos Vue.js o React.js.
