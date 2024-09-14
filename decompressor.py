import os
import zlib
import multiprocessing
from tqdm import tqdm

def decompress_chunk(data_chunk):
    """
    Decompresses a single chunk of data using zlib decompression.

    Args:
        data_chunk (bytes): A chunk of compressed data. It must be a bytes object.

    Preconditions:
        - `data_chunk` must be a bytes object that was compressed using zlib.

    Postconditions:
        - Returns the decompressed version of the input chunk as a bytes object.

    Returns:
        bytes: The decompressed data chunk.
    """
    return zlib.decompress(data_chunk)


def split_data_generator(data, chunk_size):
    """
    Splits the input data into chunks of a specified size.

    Args:
        data (bytes): The input data to be split into chunks.
        chunk_size (int): The size of each chunk in bytes.

    Preconditions:
        - `data` must be a bytes object.
        - `chunk_size` must be a positive integer.

    Postconditions:
        - Yields chunks of the data, each of size `chunk_size`, except for the last chunk, 
          which may be smaller if the data does not divide evenly.

    Yields:
        bytes: A chunk of the input data of size `chunk_size` or smaller for the last chunk.
    """
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def decompress_data_parallel(data, chunk_size, num_workers):
    """
    Decompresses large data in parallel using zlib and multiprocessing.

    This function splits the input compressed data into chunks and decompresses each chunk
    in parallel using the multiprocessing module. The results are joined into a single decompressed output.

    Args:
        data (bytes): The compressed data to be decompressed.
        chunk_size (int, optional): The size of each chunk to split the data into. 
        num_workers (int, optional): The number of processes to use for parallel 
            decompression.

    Preconditions:
        - `data` must be a bytes object that was compressed using zlib.
        - `chunk_size` must be a positive integer.
        - `num_workers` must be a positive integer.

    Postconditions:
        - Returns a decompressed version of the input data as a bytes object.

    Vars:
        data_chunks (generator): A generator that yields chunks of compressed data.
        total_chunks (int): The total number of chunks generated from the input data.

    Returns:
        bytes: The decompressed data obtained by joining all decompressed chunks.

    Example:
        >>> compressed_data = b"...compressed data..."
        >>> decompressed_data = decompress_data_parallel(compressed_data)
    """
    data_chunks = split_data_generator(data, chunk_size)
    total_chunks = (len(data) + chunk_size - 1) // chunk_size

    with multiprocessing.Pool(num_workers) as pool:
        with tqdm(total=total_chunks, desc="Decompressing", unit="chunk") as pbar:
            decompressed_chunks = []
            for result in pool.imap(decompress_chunk, data_chunks):
                decompressed_chunks.append(result)
                pbar.update(1)

    # Combine the decompressed chunks into one
    return b''.join(decompressed_chunks)


def decompress_folder(compressed_folder, output_folder, chunk_size, num_workers):
    """
    Decompresses all files in a specified folder using zlib and multiprocessing.

    Args:
        compressed_folder (str): The path to the folder containing compressed files.
        output_folder (str): The path to the folder where decompressed files will be saved.
        chunk_size (int, optional): The size of each chunk to split the file data into.
        num_workers (int, optional): The number of processes to use for parallel 
            decompression. 

    Preconditions:
        - `compressed_folder` must be a valid path to a folder containing compressed files.
        - `output_folder` must be a valid path where the decompressed files will be saved.
        - `chunk_size` must be a positive integer.
        - `num_workers` must be a positive integer.
        - Files inside the `compressed_folder` must have the ".compressed" extension.

    Postconditions:
        - All ".compressed" files in the `compressed_folder` will be decompressed and saved 
          in the `output_folder` with the ".compressed" extension removed.
        - If a file with the same name already exists in the output folder, it will be overwritten.

    Returns:
        None: The function decompresses files and saves them to the output folder.

    Example:
        >>> compressed_folder = "/path/to/compressed_folder"
        >>> output_folder = "/path/to/decompressed_output"
        >>> decompress_folder(compressed_folder, output_folder, chunk_size=1024*1024, num_workers=8)
    """
    # Make sure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Walk through the folder and decompress each file
    for root, dirs, files in os.walk(compressed_folder):
        for file in files:
            if file.endswith(".compressed"):  # Only process the compressed files
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                
                # Read the compressed file data as bytes
                with open(file_path, 'rb') as f:
                    compressed_data = f.read()
                
                # Decompress the file data
                decompressed_data = decompress_data_parallel(compressed_data, chunk_size, num_workers)
                
                # Create the output path (remove .compressed extension)
                output_file_path = os.path.join(output_folder, file.replace(".compressed", ""))
                
                # Save the decompressed data
                with open(output_file_path, 'wb') as f:
                    f.write(decompressed_data)
                print(f"File {file_path} decompressed and saved to {output_file_path}")