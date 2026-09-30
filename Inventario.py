import json # Módulo para manejar la serialización y deserialización de datos en formato JSON
import os # Módulo para interactuar con el sistema operativo, utilizado aquí para limpiar la pantalla de la consola
 
# Archivo donde se guardarán los datos de forma permanente
ARCHIVO_DATOS = "inventario.json"


def limpiar_pantalla():
    """Limpia la consola según el sistema operativo (cls para Windows, clear para Linux/Mac)."""
    os.system("cls" if os.name == "nt" else "clear")


def cargar_inventario():
    """Carga los datos guardados previamente desde el archivo JSON."""
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            try:
                return json.load(archivo)
            except json.JSONDecodeError:
                # Si el archivo está vacío o dañado, retorna un diccionario vacío
                return {}
    return {}


def guardar_inventario(inventario):
    """Guarda el estado actual del inventario en el archivo JSON."""
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(inventario, archivo, indent=4, ensure_ascii=False)


def registrar_producto(inventario):
    """Registra un nuevo producto solicitando datos al usuario."""
    limpiar_pantalla()
    print("========================================")
    print("          REGISTRAR PRODUCTO            ")
    print("========================================\n")

    codigo = input("Ingrese el código único del producto: ").strip()

    # Validar que el código no exista previamente en el inventario
    if codigo in inventario:
        print("\n⚠ Error: Ya existe un producto registrado con ese código.")
    else:
        nombre = input("Nombre del producto: ").strip()
        try:
            # Entrada y conversión de tipos numéricos
            precio = float(input("Precio unitario: "))
            cantidad = int(input("Cantidad inicial en stock: "))
            stock_minimo = int(input("Stock mínimo de alerta: "))

            # Se agregan los datos estructurados al diccionario
            inventario[codigo] = {
                "nombre": nombre,
                "precio": precio,
                "cantidad": cantidad,
                "stock_minimo": stock_minimo,
            }

            # Guardar automáticamente los cambios en el archivo
            guardar_inventario(inventario)
            print(f"\n✓ Producto '{nombre}' registrado correctamente.")

        except ValueError:
            print(
                "\n⚠ Entrada inválida. El precio y las cantidades deben ser números."
            )

    input("\nPresione ENTER para volver al menú principal...")


def mostrar_inventario(inventario):
    """Muestra todos los productos registrados en formato de tabla."""
    limpiar_pantalla()
    print("========================================")
    print("          LISTA DE PRODUCTOS            ")
    print("========================================\n")

    if not inventario:
        print("El inventario se encuentra vacío.")
    else:
        # Encabezados con formato alineado
        print(
            f"{'Código':<10} | {'Nombre':<20} | {'Precio':<10} | {'Stock':<8} | {'Estado':<10}"
        )
        print("-" * 65)

        # Recorrer e imprimir cada elemento del diccionario
        for codigo, datos in inventario.items():
            # Evaluar si el stock actual está por debajo del mínimo configurado
            estado = (
                "⚠ Reabastecer"
                if datos["cantidad"] <= datos.get("stock_minimo", 0)
                else "OK"
            )
            print(
                f"{codigo:<10} | {datos['nombre']:<20} | ${datos['precio']:<9.2f} | {datos['cantidad']:<8} | {estado:<10}"
            )

    input("\nPresione ENTER para volver al menú principal...")


def buscar_producto(inventario):
    """Busca un producto coincidiendo con el código o parte del nombre."""
    limpiar_pantalla()
    print("========================================")
    print("            BUSCAR PRODUCTO             ")
    print("========================================\n")

    # .lower() para realizar búsquedas insensibles a mayúsculas/minúsculas
    criterio = (
        input("Ingrese el código o nombre del producto: ").strip().lower()
    )
    encontrado = False

    for codigo, datos in inventario.items():
        if criterio == codigo.lower() or criterio in datos["nombre"].lower():
            print("\n--- Resultado Encontrado ---")
            print(f"Código:       {codigo}")
            print(f"Nombre:       {datos['nombre']}")
            print(f"Precio:       ${datos['precio']:.2f}")
            print(f"Stock actual: {datos['cantidad']}")
            print(
                f"Stock mínimo: {datos.get('stock_minimo', 'No definido')}"
            )
            encontrado = True
            break

    if not encontrado:
        print("\n⚠ No se encontró ningún producto con ese criterio.")

    input("\nPresione ENTER para volver al menú principal...")


def eliminar_producto(inventario):
    """Elimina un producto del inventario mediante su código."""
    limpiar_pantalla()
    print("========================================")
    print("           ELIMINAR PRODUCTO            ")
    print("========================================\n")

    codigo = input("Ingrese el código del producto a eliminar: ").strip()

    if codigo in inventario:
        # Eliminar del diccionario y retornar el elemento eliminado
        eliminado = inventario.pop(codigo)
        guardar_inventario(inventario)
        print(f"\n✓ Producto '{eliminado['nombre']}' eliminado correctamente.")
    else:
        print("\n⚠ Error: El código ingresado no existe en el inventario.")

    input("\nPresione ENTER para volver al menú principal...")


def menu_principal():
    """Controla el flujo principal del programa y la navegación."""
    # Cargar datos al iniciar el sistema
    inventario = cargar_inventario()

    while True:
        limpiar_pantalla()
        print("========================================")
        print("   SISTEMA DE GESTIÓN DE INVENTARIO     ")
        print("========================================")
        print("1. Registrar nuevo producto")
        print("2. Mostrar todos los productos")
        print("3. Buscar producto")
        print("4. Eliminar producto")
        print("5. Salir")
        print("========================================")

        opcion = input("Seleccione una opción (1-5): ").strip()

        # Evaluación de la opción seleccionada
        if opcion == "1":
            registrar_producto(inventario)
        elif opcion == "2":
            mostrar_inventario(inventario)
        elif opcion == "3":
            buscar_producto(inventario)
        elif opcion == "4":
            eliminar_producto(inventario)
        elif opcion == "5":
            limpiar_pantalla()
            print("Guardando datos y saliendo del sistema... ¡Hasta luego!\n")
            break


# Punto de entrada principal para la ejecución del script
if __name__ == "__main__":
    menu_principal()