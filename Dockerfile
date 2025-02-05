# Imagen base ligera
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt .
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto de FastAPI
EXPOSE 8000

# Comando para ejecutar la API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
