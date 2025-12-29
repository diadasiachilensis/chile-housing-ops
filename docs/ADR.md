
# ADR 001: Selección del Patrón Strategy para el Motor de Valuación

* **Fecha:** Diciembre 2025
* **Autor:** *Diadasia chilensis*

## Contexto del Problema

El módulo de valuación de propiedades en 'Chile-Housing-ops' requiere realizar cálculos financieros dinámicos sobre el precio de los activos. Estos cálculos dependen de variables externas volátiles (valor de la UF, Dólar observado) y de algoritmos que cambian según el contexto (tasación comercial, tasación fiscal, conversión de moneda).

Inicialmente, se podría considerar el uso de estructuras de control condicionales (`switch` o `if/else`) dentro de la clase `Property` para manejar estas variantes. La pregunta central es: **¿Cómo gestionamos la variabilidad de los algoritmos de tasación sin degradar la mantenibilidad del código base?**

## Decisión

Se decide implementar el **Patrón de Diseño Strategy** para encapsular la lógica de valuación y conversión de divisas, descartando el uso de sentencias condicionales extensas (`switch/case`).

## Justificación Teórica y Bibliográfica

La decisión se fundamenta en tres principios de ingeniería extraídos de la literatura técnica analizada:

### 1. Principio Abierto/Cerrado (OCP) y Encapsulamiento

El uso de un bloque `switch` obliga a modificar la clase principal cada vez que se introduce una nueva regla de negocio (por ejemplo, una nueva fórmula de tasación bancaria). Como explican Freeman et al. (2004) en *Head First Design Patterns*, esto viola el principio de diseño que dicta "encapsular lo que varía". Al aplicar el patrón Strategy, definimos una familia de algoritmos, encapsulamos cada uno y los hacemos intercambiables. Esto permite que el algoritmo varíe independientemente de los clientes que lo utilizan, cumpliendo con el principio OCP: la clase `Property` queda cerrada a modificaciones pero abierta a extensiones mediante nuevas estrategias.

### 2. Desacoplamiento de la Volatilidad (Connascence)

Desde la perspectiva de la arquitectura moderna, Ford y Richards (2021) en *Software Architecture: The Hard Parts* advierten sobre los peligros del acoplamiento estático excesivo. Un `switch` gigante genera una alta "connascencia de algoritmo", donde múltiples partes del sistema deben conocer los detalles internos de cómo se calcula un precio. Al inyectar una interfaz `IValuationStrategy`, transformamos este acoplamiento en dinámico. Esto reduce la complejidad ciclomática del componente de valuación y facilita la evolución independiente de las reglas financieras sin riesgo de romper la lógica central del objeto de dominio.

### 3. Testabilidad y Cohesión

Richards y Ford (2020) en *Fundamentals of Software Architecture* enfatizan que la testabilidad es una característica estructural crítica. Probar un método con 15 ramas condicionales (`if/else`) es propenso a errores y difícil de cubrir al 100%. Al usar Strategy, cada algoritmo (ej. `UfConversionStrategy`) se aísla en su propia clase pequeña y cohesiva. Esto permite realizar pruebas unitarias granulares sobre la lógica matemática sin necesidad de instanciar objetos complejos o simular todo el entorno de la aplicación.

## Consecuencias

### Positivas

* **Extensibilidad:** Agregar soporte para una nueva divisa (ej. Bitcoin) solo requiere crear una nueva clase `BitcoinStrategy`, sin tocar el código existente.
* **Limpieza:** Se elimina la lógica condicional compleja de las clases de negocio principales.
* **Testabilidad:** Permite testear cada fórmula matemática de forma aislada.

### Negativas

* **Incremento de Clases:** Aumenta el número total de archivos en el proyecto (una clase por cada estrategia), lo cual añade una capa leve de complejidad estructural inicial (Freeman et al., 2004).

---

## Referencias (APA 7.ª Ed.)

* Ford, N., & Richards, M. (2021). *Software architecture: The hard parts: Modern trade-off analysis for distributed architectures*. O'Reilly Media.
* Freeman, E., Robson, E., Bates, B., & Sierra, K. (2004). *Head first design patterns*. O'Reilly Media.
* Richards, M., & Ford, N. (2020). *Fundamentals of software architecture: An engineering approach*. O'Reilly Media.

---

### Siguiente paso

¿Te gustaría que redactemos la **segunda pregunta** del ADR ("¿Por qué Factory para la ingesta?") utilizando el mismo rigor académico, o prefieres pasar a la implementación en código de este patrón Strategy?