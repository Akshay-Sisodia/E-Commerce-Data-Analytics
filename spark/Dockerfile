FROM apache/spark:3.3.1

# Set working directory
WORKDIR /app

# Install Python, pip, curl, and other dependencies
USER root
RUN apt-get update && apt-get install -y python3 python3-pip curl build-essential libsnappy1v5 libsnappy-dev && \
    pip3 install --upgrade pip

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Add PostgreSQL JDBC driver to Spark's jars directory
RUN curl -L -o /opt/spark/jars/postgresql-42.5.4.jar https://jdbc.postgresql.org/download/postgresql-42.5.4.jar

# Copy the Python script
COPY data_processing.py .

# Command to run the script
CMD ["spark-submit", \
     "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1,org.apache.kafka:kafka-clients:2.8.1,org.apache.spark:spark-streaming-kafka-0-10_2.12:3.3.1", \
     "--driver-class-path", "/opt/spark/jars/postgresql-42.5.4.jar", \
     "data_processing.py"]