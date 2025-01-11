from pyspark.sql import SparkSession
from pyspark.sql import Row

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Batch Data Test and Fix") \
    .getOrCreate()

# Path to the batch data file (replace with your actual path)
batch_data_path = "product_catalog.csv"

# Function to load batch data
def load_batch_data(path):
    try:
        # Attempt to load the batch data
        df = spark.read.format("csv") \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .load(path)
        return df
    except Exception as e:
        print(f"Error loading batch data: {e}")
        return None

# Function to validate batch data
def validate_batch_data(df):
    if df is None:
        print("Batch data is None. Check the data source or file path.")
        return False
    if df.count() == 0:
        print("Batch data is empty. No rows found.")
        return False
    print("Batch data is valid and contains rows.")
    return True

# Function to fix empty batch data by creating sample data
def fix_empty_batch_data():
    # Create sample batch data
    data = [
        Row(user_id=1, product_id="101", product_name="Test Product 1"),
        Row(user_id=2, product_id="102", product_name="Test Product 2")
    ]
    df = spark.createDataFrame(data)
    print("Sample batch data created to fix the issue.")
    return df

# Main script
if __name__ == "__main__":
    # Step 1: Load batch data
    batch_df = load_batch_data(batch_data_path)

    # Step 2: Validate batch data
    if not validate_batch_data(batch_df):
        # Step 3: Fix empty batch data by creating sample data
        batch_df = fix_empty_batch_data()

    # Step 4: Show the batch data
    print("Batch Data:")
    batch_df.show()

    # Step 5: Print the batch data schema
    print("Batch Data Schema:")
    batch_df.printSchema()

    # Stop the Spark session
    spark.stop()