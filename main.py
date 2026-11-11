from personajes import Personaje, Guerrero, Mago, Arquero, Combate


def linea(titulo=""):
    print("\n" + "=" * 60)
    if titulo:
        print(f"  {titulo}")
        print("=" * 60)


def probar_creacion():
    linea("1. Creación correcta de los tres tipos")
    g = Guerrero("Arthas", 100, 30, 20)
    m = Mago("Gandalf", 80, 40, 10)
    a = Arquero("Legolas", 90, 35, 15)
    for p in (g, m, a):
        print("  ✔", p.mostrar_estado())


def probar_validaciones():
    linea("2-4. Rechazo de valores inválidos")
    casos = [
        ("Vida > 100", lambda: Guerrero("X", 120, 30, 20)),
        ("Vida negativa", lambda: Mago("Y", -5, 40, 10)),
        ("Nombre vacío", lambda: Arquero("", 90, 35, 15)),
        ("Ataque cero", lambda: Guerrero("Z", 50, 0, 20)),
        ("Defensa negativa", lambda: Mago("W", 50, 40, -1)),
    ]
    for desc, fn in casos:
        try:
            fn()
            print(f"  ✘ {desc}: NO se lanzó excepción (ERROR)")
        except (ValueError, TypeError) as e:
            print(f"  ✔ {desc}: rechazado → {e}")


def probar_habilidades():
    linea("5-7. Habilidades especiales")
    # Guerrero: 30 × 1.20 = 36; 36 - 10 = 26
    g = Guerrero("Arthas", 100, 30, 20)
    m = Mago("Gandalf", 80, 40, 10)
    print(f"  Guerrero daño esperado 26 → obtenido {g.atacar(m)}")
    print(f"     Vida Gandalf: {m.vida}")

    # Mago ignora defensa: 40
    m2 = Mago("Merlin", 80, 40, 10)
    g2 = Guerrero("Rexxar", 100, 30, 20)
    print(f"  Mago daño esperado 40 → obtenido {m2.atacar(g2)}")

    # Arquero: (35 - 15) × 2 = 40
    a = Arquero("Legolas", 90, 35, 15)
    objetivo = Guerrero("Thrall", 100, 25, 15)
    print(f"  Arquero daño esperado 40 → obtenido {a.atacar(objetivo)}")

    # Arquero con ataque ≤ defensa → 0
    a2 = Arquero("Robin", 90, 10, 15)
    obj2 = Guerrero("Tank", 100, 25, 20)
    print(f"  Arquero sin crítico (10 ≤ 20) → {a2.atacar(obj2)}")


def probar_vida_no_negativa():
    linea("8. Vida nunca negativa")
    g = Guerrero("Arthas", 20, 30, 20)
    danio = g.recibir_danio(50)
    print(f"  Daño aplicado: {danio} (esperado 20)")
    print(f"  Vida final: {g.vida} (esperado 0)")
    print(f"  ¿Vivo? {g.esta_vivo()} (esperado False)")


def probar_atacar_derrotado():
    linea("9. No atacar derrotado")
    g = Guerrero("Arthas", 10, 30, 20)
    m = Mago("Gandalf", 80, 40, 10)
    m.atacar(g)          # deja a Arthas en 0
    print(f"  Vida Arthas: {g.vida}")
    try:
        g.atacar(m)
        print("  ✘ No se lanzó excepción (ERROR)")
    except ValueError as e:
        print(f"  ✔ Excepción esperada: {e}")


def probar_combate_completo():
    linea("10-11. Combate completo (Arthas vs Gandalf)")
    a = Guerrero("Arthas", 100, 30, 20)
    g = Mago("Gandalf", 80, 40, 10)
    combate = Combate(a, g)
    ganador = combate.iniciar()
    print(f"\n  Ganador detectado: {ganador.nombre if ganador else 'Empate'}")


def probar_empate_tecnico():
    linea("12. Empate técnico (sin daño)")
    # Dos magos con defensa muy alta pero ataque 1 → 0 daño
    # Mejor: dos guerreros con ataque bajo y defensa alta
    g1 = Guerrero("Piedra1", 100, 5, 50)
    g2 = Guerrero("Piedra2", 100, 5, 50)
    combate = Combate(g1, g2)
    combate.iniciar()


if __name__ == "__main__":
    probar_creacion()
    probar_validaciones()
    probar_habilidades()
    probar_vida_no_negativa()
    probar_atacar_derrotado()
    probar_combate_completo()
    probar_empate_tecnico()
    print("Todos los casos de prueba ejecutados.")
