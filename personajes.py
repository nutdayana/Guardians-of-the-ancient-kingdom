from abc import ABC, abstractmethod


from abc import ABC, abstractmethod


class Personaje(ABC):
    """Clase base abstracta para todos los guardianes del reino."""

    def __init__(self, nombre: str, vida: int, ataque: int, defensa: int):
        # Validaciones iniciales mediante setters
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa

    # ---------- nombre ----------
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    # ---------- vida ----------
    @property
    def vida(self) -> int:
        return self._vida

    @vida.setter
    def vida(self, valor: int):
        if not isinstance(valor, int):
            raise TypeError("La vida debe ser un entero.")
        if valor < 0 or valor > 100:
            raise ValueError("La vida debe estar entre 0 y 100.")
        self._vida = valor

    # ---------- ataque ----------
    @property
    def ataque(self) -> int:
        return self._ataque

    @ataque.setter
    def ataque(self, valor: int):
        if not isinstance(valor, int):
            raise TypeError("El ataque debe ser un entero.")
        if valor <= 0:
            raise ValueError("El ataque debe ser positivo.")
        self._ataque = valor

    # ---------- defensa ----------
    @property
    def defensa(self) -> int:
        return self._defensa

    @defensa.setter
    def defensa(self, valor: int):
        if not isinstance(valor, int):
            raise TypeError("La defensa debe ser un entero.")
        if valor < 0:
            raise ValueError("La defensa no puede ser negativa.")
        self._defensa = valor

    # ---------- métodos comunes ----------
    def recibir_danio(self, cantidad: int) -> int:
        """Aplica daño ya calculado. Devuelve el daño efectivo."""
        if not isinstance(cantidad, (int, float)):
            raise TypeError("La cantidad de daño debe ser numérica.")
        if cantidad < 0:
            raise ValueError("El daño no puede ser negativo.")
        cantidad = int(cantidad)  # por si llega float
        danio_efectivo = min(cantidad, self.vida)
        self._vida -= danio_efectivo
        return danio_efectivo

    def esta_vivo(self) -> bool:
        return self._vida > 0

    def mostrar_estado(self) -> str:
        return (f"{self._nombre} ({self.__class__.__name__}) — "
                f"Vida: {self._vida} | Ataque: {self._ataque} | Defensa: {self._defensa}")

    # ---------- método abstracto ----------
    @abstractmethod
    def atacar(self, objetivo: "Personaje") -> int:
        """Cada subclase implementa su propia forma de atacar."""
        ...

    # ---------- validaciones comunes de ataque ----------
    def _validar_ataque(self, objetivo: "Personaje"):
        if not isinstance(objetivo, Personaje):
            raise TypeError("El objetivo debe ser un Personaje válido.")
        if not self.esta_vivo():
            raise ValueError(f"{self._nombre} está derrotado y no puede atacar.")
        if not objetivo.esta_vivo():
            raise ValueError(f"{objetivo.nombre} ya está derrotado.")

        class Guerrero(Personaje):
            """Golpe poderoso: ataque × 1.20 antes de restar defensa."""

    def atacar(self, objetivo: Personaje) -> int:
        self._validar_ataque(objetivo)
        ataque_potenciado = int(self.ataque * 1.20)  # floor
        danio = max(0, ataque_potenciado - objetivo.defensa)
        return objetivo.recibir_danio(danio)

class Mago(Personaje):
    """Hechizo penetrante: ignora la defensa del objetivo."""

    def atacar(self, objetivo: Personaje) -> int:
        self._validar_ataque(objetivo)
        danio = self.ataque
        return objetivo.recibir_danio(danio)

class Arquero(Personaje):
    """Disparo crítico: duplica el daño si el ataque supera la defensa."""

    def atacar(self, objetivo: Personaje) -> int:
        self._validar_ataque(objetivo)
        if self.ataque > objetivo.defensa:
            danio = (self.ataque - objetivo.defensa) * 2
        else:
            danio = 0
        return objetivo.recibir_danio(danio)

    class Combate:
        """Administra un enfrentamiento entre dos personajes (agregación)."""

    MAX_RONDAS = 50

    def __init__(self, personaje1: Personaje, personaje2: Personaje):
        if not isinstance(personaje1, Personaje) or not isinstance(personaje2, Personaje):
            raise TypeError("Ambos participantes deben ser Personaje.")
        if personaje1 is personaje2:
            raise ValueError("Un personaje no puede combatir contra sí mismo.")
        self.personaje1 = personaje1
        self.personaje2 = personaje2
        self.turno_actual = personaje1   # empieza el primero
        self.rondas = 0
        self.ganador = None
        self.empate = False

    def cambiar_turno(self):
        self.turno_actual = (self.personaje2
                             if self.turno_actual is self.personaje1
                             else self.personaje1)

    def _oponente_de(self, atacante: Personaje) -> Personaje:
        return self.personaje2 if atacante is self.personaje1 else self.personaje1

    def verificar_ganador(self):
        p1_vivo = self.personaje1.esta_vivo()
        p2_vivo = self.personaje2.esta_vivo()
        if not p1_vivo and not p2_vivo:
            self.empate = True
            self.ganador = None
            return True
        if not p1_vivo:
            self.ganador = self.personaje2
            return True
        if not p2_vivo:
            self.ganador = self.personaje1
            return True
        return False

    def iniciar(self):
        print("=" * 55)
        print(f"⚔  COMBATE: {self.personaje1.nombre} vs {self.personaje2.nombre}")
        print("=" * 55)
        print(self.personaje1.mostrar_estado())
        print(self.personaje2.mostrar_estado())
        print("-" * 55)

        numero_turno = 0
        while True:
            # 1) ¿Ya hay ganador antes de iniciar la ronda?
            if self.verificar_ganador():
                break

            # 2) Límite de rondas
            if self.rondas >= self.MAX_RONDAS:
                self.empate = True
                break

            # al comenzar cada ronda (antes del primer ataque de la ronda)
            self.rondas += 1
            self._vida_inicio_ronda = (self.personaje1.vida, self.personaje2.vida)
            numero_turno += 1
            atacante = self.turno_actual
            objetivo = self._oponente_de(atacante)

            # 3) Polimorfismo: no preguntamos el tipo
            danio = atacante.atacar(objetivo)

            print(f"Turno {numero_turno}: {atacante.nombre} ataca a "
                  f"{objetivo.nombre} → {danio} de daño")
            print(f"   {self.personaje1.mostrar_estado()}")
            print(f"   {self.personaje2.mostrar_estado()}")

            # 4) ¿Fin por KO?
            if self.verificar_ganador():
                break

            # 5) Ronda completa sin daño → empate técnico
            #    (se evalúa tras ambos turnos)
            if numero_turno % 2 == 0:
                # Si en una ronda completa ambos hicieron 0 daño:
                if (not self.personaje1.esta_vivo() is False and  # sigue vivo
                        self._ronda_sin_danio()):
                    self.empate = True
                    break

            self.cambiar_turno()

        self.mostrar_resultado()
        return self.ganador

    # ---- auxiliar para detectar ronda sin daño ----
    def _ronda_sin_danio(self) -> bool:
        # Recalculamos de forma segura: si ambos siguen con vida plena
        # y no ha habido cambios de vida, se considera empate técnico.
        # Para una implementación robusta, guardamos vida al inicio de la ronda.
        return self._vida_inicio_ronda == (self.personaje1.vida, self.personaje2.vida)

    def mostrar_resultado(self):
        print("-" * 55)
        if self.ganador:
            print(f"GANADOR: {self.ganador.nombre} "
                  f"({self.ganador.__class__.__name__})")
        elif self.empate:
            print("EMPATE (técnico o por límite de rondas).")
        else:
            print("Combate sin resolución.")
        print(self.personaje1.mostrar_estado())
        print(self.personaje2.mostrar_estado())
        print("=" * 55)
