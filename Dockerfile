# 1. Base Python image choose karein
FROM python:3.10-slim

# 2. Container ke andar working directory set karein
WORKDIR /app

# 3. Dependencies list copy karein aur install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Baaki saara project code container mein copy karein
COPY . .

# 5. Flask Port expose karein
EXPOSE 5000

# 6. Container start hote hi app run karne ki command
CMD ["python", "app.py"]