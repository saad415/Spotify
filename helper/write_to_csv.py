import os

subfolder = 'data'

def write_csv(data, csv_file_name):
      # Create the subfolder if it doesn't exist
    os.makedirs(subfolder, exist_ok=True)
    
    # Define the CSV file path within the subfolder
    csv_file = os.path.join(subfolder, csv_file_name)
    
    # Save the DataFrame to a CSV file
    data.to_csv(csv_file, index=False)
    print(f"Information has been written to {csv_file_name}")
