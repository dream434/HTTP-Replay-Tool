FROM python:3.11-slim

WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers de l'app (templates, static, JSON inclus)
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
