import os
import zlib
import multiprocessing
from tqdm import tqdm

def compress_chunk(data_chunk):
    """
    Compresses a single chunk of data using zlib compression.

    Args:
        data_chunk (bytes): A chunk of data to be compressed. It should be a bytes object.

    Preconditions:
        - `data_chunk` must be a bytes object.

    Postconditions:
        - Returns a compressed version of the input chunk as a bytes object.

    Returns:
        bytes: The compressed data chunk.
    """
    return zlib.compress(data_chunk)


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
        - Yields chunks of the data, each of size `chunk_size`, except for the last chunk 
          which may be smaller if the data does not divide evenly.

    Yields:
        bytes: A chunk of the input data of size `chunk_size` or smaller for the last chunk.
    """
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def compress_data_parallel(data, chunk_size, num_workers): 
    """
    Compresses large data using zlib in parallel across multiple processes.

    This function splits the input data into chunks and compresses each chunk
    in parallel using the multiprocessing module. The results are joined into 
    a single compressed output.

    Args:
        data (bytes): The data to be compressed.
        chunk_size (int, optional): The size of each chunk to split the data into. 
        num_workers (int, optional): The number of processes to use for parallel 
            compression.
            
    Preconditions:
        - `data` must be a bytes object.
        - `chunk_size` must be a positive integer.
        - `num_workers` must be a positive integer.

    Postconditions:
        - Returns a compressed version of the input data as a bytes object.

    Vars:
        data_chunks (generator): A generator that yields chunks of data.
        total_chunks (int): The total number of chunks generated from the input data.

    Returns:
        bytes: The compressed data obtained by joining all compressed chunks.

    Example:
        >>> large_data = b"This is a large data" * 1000000
        >>> compressed_data = compress_data_parallel(large_data)
    """
    data_chunks = split_data_generator(data, chunk_size)
    total_chunks = (len(data) + chunk_size - 1) // chunk_size

    with multiprocessing.Pool(num_workers) as pool:
        with tqdm(total=total_chunks, desc="Compressing", unit="chunk") as pbar:
            compressed_chunks = []
            for result in pool.imap(compress_chunk, data_chunks):
                compressed_chunks.append(result)
                pbar.update(1)

    return b''.join(compressed_chunks)


def compress_folder(decrompressed_folder, output_folder, chunk_size, num_workers):
    """
    Compresses all files in a specified folder using zlib and multiprocessing.

    Args:
        decrompressed_folder (str): The path to the folder containing files to be compressed.
        output_folder (str): The path to the folder where compressed files will be saved.
        chunk_size (int, optional): The size of each chunk to split the file data into.
        num_workers (int, optional): The number of processes to use for parallel 
            compression.

    Preconditions:
        - `decrompressed_folder` must be a valid path to a folder containing files.
        - `output_folder` must be a valid path where the compressed files will be saved.
        - `chunk_size` must be a positive integer.
        - `num_workers` must be a positive integer.
        - Files inside the `decrompressed_folder` must be readable.

    Postconditions:
        - All files in the `decrompressed_folder` will be compressed and saved in the `output_folder` 
          with the ".compressed" extension.
        - If a file with the same name already exists in the output folder, it will be overwritten.

    Returns:
        None: The function compresses files and saves them to the output folder.

    Example:
        >>> decrompressed_folder = "/path/to/folder"
        >>> output_folder = "/path/to/compressed_output"
        >>> compress_folder(decrompressed_folder, output_folder, chunk_size=1024*1024, num_workers=8)
    """
    # Make sure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Walk through the folder and compress each file
    for root, dirs, files in os.walk(decrompressed_folder):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")
            
            # Read the file data as bytes
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Compress the file data
            compressed_data = compress_data_parallel(file_data, chunk_size, num_workers)
            
            # Create the output path
            output_file_path = os.path.join(output_folder, file + ".compressed")
            
            # Save the compressed data
            with open(output_file_path, 'wb') as f:
                f.write(compressed_data)
            print(f"File {file_path} compressed and saved to {output_file_path}")