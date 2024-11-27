import os
import psycopg2

from scripts.connect import connect
from scripts.config import load_config

# Path to the samples folder
SAMPLES_DIR = "../samples/"

def parse_filename(filename):
    """
    Parse the filename to extract chord, type, and shape.
    Example: G#_min_2.mp3 -> chord: G#, type: min, shape: 2
    """
    base_name = os.path.splitext(filename)[0]  # Remove file extension
    try:
        chord, type_, shape = base_name.split('_')
    except ValueError:
        raise ValueError(f"Filename {filename} does not match expected format 'Chord_Type_Shape.mp3'")
    return chord, type_, shape

def main():
    # Connect to the database
    try:
        # Connection with local postgreSQL server
        postgres_config = load_config()
        postgres_conn = connect(postgres_config)
        postgres_cur = postgres_conn.cursor()
        
        # Recreate the Samples table
        postgres_cur.execute("DROP TABLE IF EXISTS Samples;")
        postgres_cur.execute("""
            CREATE TABLE Samples (
                Chord VARCHAR(10),
                Type VARCHAR(10),
                Shape INT,
                File BYTEA
            );
        """)
        print("Table 'Samples' recreated successfully.")
        
        # Process each file in the samples directory
        for filename in os.listdir(SAMPLES_DIR):
            if filename.endswith(".mp3"):
                filepath = os.path.join(SAMPLES_DIR, filename)
                
                # Parse the filename to extract data
                try:
                    chord, type_, shape = parse_filename(filename)
                except ValueError as e:
                    print(e)
                    continue
                
                # Read the audio file
                with open(filepath, "rb") as f:
                    file_data = f.read()
                
                # Insert data into the table
                postgres_cur.execute("""
                    INSERT INTO Samples (Chord, Type, Shape, File)
                    VALUES (%s, %s, %s, %s);
                """, (chord, type_, int(shape), file_data))
                
                print(f"Inserted {filename} into the database.")
        
        # Commit the changes
        postgres_conn.commit()
        print("All samples have been loaded into the database.")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Close the database connection
        if postgres_cur:
            postgres_cur.close()
        if postgres_conn:
            postgres_conn.close()

if __name__ == "__main__":
    main()
