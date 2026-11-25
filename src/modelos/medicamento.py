class Medicamento:
    """
    Modela un medicamento del inventario hospitalario,
    controlando su nombre, identificador y la cantidad disponible en stock.
    """
    def __init__(self, id_medicamento, nombre, stock):
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        self.__id_medicamento = id_medicamento
        self.__nombre = nombre
        self.__stock = stock

    def get_id_medicamento(self):
        return self.__id_medicamento

    def get_nombre(self):
        return self.__nombre

    def get_stock(self):
        return self.__stock

    def actualizar_stock(self, cantidad):
        """
        Suma o resta unidades al stock actual.
        lanza un error si la operacion deja el inventario por debajo de cero.
        """
        nuevo_stock = self.__stock + cantidad

        if nuevo_stock < 0:
            raise ValueError("Stock insuficiente.")

        self.__stock = nuevo_stock
