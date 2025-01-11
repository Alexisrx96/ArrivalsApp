# Análisis y Diseño

## Herramientas y Tecnologías Propuestas

- **FastAPI**: Framework de Python para construir APIs RESTful de alto rendimiento, basado en Starlette y Pydantic. Es una opción eficiente para desarrollar APIs de forma fácil, rápida y flexible.

- **SQLAlchemy**: ORM de Python que proporciona una capa de abstracción sobre bases de datos relacionales como PostgreSQL. Facilita el manejo de la base de datos y mejora la mantenibilidad del código.

- **MongoDB**: Base de datos NoSQL, ideal para almacenar datos desnormalizados y realizar consultas rápidas. Es utilizado en el patrón CQRS para manejar las consultas, optimizando la lectura. Se optó por MongoDB sobre Redis debido a que posee compatibilidad con diferentes tipos de datos.

- **Pydantic**: Biblioteca para la validación de datos en FastAPI, que asegura que las entradas sean correctas antes de procesarlas. Pydantic también se usa para la serialización de respuestas.

- **bcrypt y passlib**: Bibliotecas para el almacenamiento seguro de contraseñas. Estas herramientas utilizan algoritmos de hashing robustos para evitar que las contraseñas se almacenen en texto claro.

- **MediatR**: Biblioteca para implementar el patrón CQRS (Command Query Responsibility Segregation). Facilita la separación de la lógica de comandos y consultas, promoviendo la escalabilidad y mantenibilidad del código.

## Patrones de Diseño

- **Domain-Driven Design (DDD):** Un enfoque de diseño centrado en el modelo de dominio, que estructura el código alrededor de las reglas de negocio. Facilita la comprensión y extensión de la lógica de la aplicación.

- **Vertical Slices:** Inspirado en la arquitectura propuesta por Django, se organiza el código en módulos independientes (slices) que contienen todo lo necesario para un caso de uso específico, incluyendo la lógica de negocio, los modelos, las vistas y las rutas. Este enfoque mejora la mantenibilidad y escalabilidad.

- **Mediador:** Permite reducir las dependencias entre objetos. El patrón restringe las comunicaciones directas entre los objetos, forzándolos a colaborar únicamente a través de un objeto mediador. Este objeto se encarga de gestionar la forma en que un conjunto de clases se comunican entre sí.

- **Fachada:** Simplifica la interacció entre las clases internas y el exterior de una clase. La fachada proporciona una interfaz simple para el acceso a las funciones internas, ocultando la complejidad interna de la clase.
