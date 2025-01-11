# E-Commerce Analytics with Docker Compose

This project sets up an **E-Commerce Analytics** environment using Docker Compose. It includes the following services:

- **Zookeeper**: Manages Kafka's metadata and coordination.
- **Kafka**: A distributed event streaming platform for real-time data processing.
- **MinIO**: An object storage service for storing and retrieving data.
- **PostgreSQL**: A relational database for storing e-commerce data.
- **Spark**: A distributed computing framework for big data processing.
- **Metabase**: A business intelligence and analytics tool for visualizing data.

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

### Setup

1. Clone this repository (if applicable):

   ```bash
   git clone https://github.com/Akshay-Sisodia/E-Commerce-Data-Analytics.git
   cd ecommerce-data-analyser
   ```

2. Start the services using Docker Compose:

   ```bash
   docker-compose up -d
   ```

   > **Note**: The `-d` flag runs the containers in detached mode.

3. Verify that all containers are running:

   ```bash
   docker-compose ps
   ```

---

## 🛠️ Services Overview

### 1. **Zookeeper**
- **Port**: `2181`
- **Role**: Manages Kafka's metadata and coordination.

### 2. **Kafka**
- **Ports**:
  - Internal: `9092`
  - External: `9093`
- **Role**: Handles real-time event streaming.

### 3. **MinIO**
- **Ports**:
  - API: `9000`
  - Console: `9001`
- **Credentials**:
  - Username: `minioadmin`
  - Password: `minioadmin`
- **Role**: Provides object storage for data.

### 4. **PostgreSQL**
- **Port**: `5432`
- **Credentials**:
  - Username: `admin`
  - Password: `password`
  - Database: `ecommerce`
- **Role**: Stores e-commerce data.

### 5. **Spark**
- **Role**: Processes big data and performs analytics.
- **Dependencies**: Kafka, MinIO, and PostgreSQL.

### 6. **Metabase**
- **Port**: `3000`
- **Role**: Provides a web-based interface for data visualization and analytics.

---

## 🔧 Customization

### Environment Variables
You can customize the services by modifying the `environment` section in the `docker-compose.yml` file. For example:

```yaml
postgres:
  environment:
    POSTGRES_USER: custom_user
    POSTGRES_PASSWORD: custom_password
```

### Persistent Data
The following services store data on your local machine:
- **MinIO**: Data is stored in `./minio/data`.
- **PostgreSQL**: The database schema is initialized using `./postgres/init.sql`.
- **Spark**: The application code is mounted from `./spark`.

---

## 🛑 Stopping the Services

To stop all services, run:

```bash
docker-compose down
```

To remove all containers, volumes, and networks, use:

```bash
docker-compose down --volumes
```

---

## 📄 Documentation

- **Kafka**: [Confluent Kafka Documentation](https://docs.confluent.io/)
- **MinIO**: [MinIO Documentation](https://min.io/docs/)
- **PostgreSQL**: [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- **Spark**: [Apache Spark Documentation](https://spark.apache.org/docs/)
- **Metabase**: [Metabase Documentation](https://www.metabase.com/docs/)

---

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

If you have any questions or need assistance, feel free to reach out:

- **Your Name** - [akshaysisodia.studies@gmail.com](mailto:akshaysisodia.studies@gmail.com)
- **GitHub Profile**: [Akshay Sisodia](https://github.com/Akshay-Sisodia)
