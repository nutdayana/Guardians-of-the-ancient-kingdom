# Guardians-of-the-ancient-kingdom
En este repositorio presento mi trabajo de 2do corte de Programacion Orientada a Objetos, en el cual pongo en practica todo lo aprendido sobre herencia, polimorfismo, encapsulamiento, métodos y relaciones entre clases.
<img width="2939" height="3663" alt="deepseek_mermaid_20261111_db42fb" src="https://github.com/user-attachments/assets/d68f37d1-6999-40aa-a1a9-4b52c530af9a" />
¿Por qué atacar() debe ser abstracto, pero recibir_danio() puede estar implementado en la clase base?

1. La responsabilidad de Personaje.
Personaje representa lo común a todo guardián: tiene nombre, vida, ataque y defensa, y sabe recibir daño. Su rol es definir el contrato que todo guardián debe cumplir (por eso es una clase abstracta), no decidir cómo ataca cada orden.

2. Comportamientos compartidos.
recibir_danio() es idéntico para los tres tipos: se descuenta la vida sin bajar de cero y se devuelve el daño efectivo. Es una operación estructural, no depende del tipo de personaje. Implementarla una sola vez en la base evita duplicación (principio DRY) y garantiza consistencia (por ejemplo, la regla "la vida nunca queda negativa" se cumple siempre). Lo mismo ocurre con esta_vivo() o mostrar_estado().

3. ¿Por qué atacar() sí debe ser abstracto?
Porque la fórmula del daño cambia según la orden:

Guerrero: int(ataque × 1.20) − defensa

Mago: ataque (ignora defensa)

Arquero: (ataque − defensa) × 2 si ataque > defensa, si no 0

No existe una fórmula "genérica" correcta. Si Personaje implementara un atacar() por defecto, las subclases tendrían que sobrescribirlo igualmente y el método base sería engañoso. La clase abstracta obliga a cada subclase a definir su propio comportamiento (implementación obligatoria) y impide instanciar Personaje directamente.

4. Relación con los pilares de POO.

Abstracción: Personaje define qué hace un guardián (atacar, recibir_danio, esta_vivo) sin fijar cómo ataca cada uno.

Herencia: las subclases reutilizan atributos y métodos validados (recibir_danio, setters, _validar_ataque).

Polimorfismo: Combate.iniciar() llama atacante.atacar(objetivo) sin preguntar el tipo; en tiempo de ejecución se invoca la versión del Guerrero, Mago o Arquero. Añadir un nuevo guardián (p. ej., Sanador) solo requiere heredar de Personaje e implementar atacar(); la clase Combate no cambia.
