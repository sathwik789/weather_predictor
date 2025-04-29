FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir flask pandas numpy scikit-learn matplotlib seaborn

# Expose the Flask port
EXPOSE 5000

# Run the app (change the filename if needed)
CMD ["python", "app.py"]
