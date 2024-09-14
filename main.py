import multiprocessing
from compressor import compress_folder
from decompressor import decompress_folder

if __name__ == "__main__":
    # Step 1: Compression
    # Define the folder containing the decompressed files and the output folder for compressed files
    decrompressed_folder = r"PATH TO DECOMPRESSED INPUT" # Folder with decompressed files can also be a single file or other data
    compressed_output_folder = r"PATH TO COMPRESSED OUTPUT" # Output folder for compressed files

    # Compress all files in the folder
    print("Starting compression...")
    compress_folder(decrompressed_folder, compressed_output_folder, chunk_size=1024 * 1024, num_workers=multiprocessing.cpu_count()) # Optionally specify the chunk size and number of workers to suit the system configuration
    print("All files in the folder have been compressed!")

    # Step 2: Decompression
    # Define the folder containing the compressed files and the output folder for decompressed files
    compressed_folder = r"PATH TO COMPRESSED INPUT"  # Folder with compressed files can also be a single file or other data
    decompressed_output_folder = r"PATH TO DECOMPRESSED OUTPUT"  # Output folder for decompressed files

    # Decompress all files in the folder
    print("Starting decompression...")
    decompress_folder(compressed_folder, decompressed_output_folder, chunk_size=1024 * 1024, num_workers=multiprocessing.cpu_count()) # Optionally specify the chunk size and number of workers to suit the system configuration
    print("All files in the folder have been decompressed!")


# NOTE: 
# The compressor and decompressor functions can be used interchangeably with any folder containing files to be compressed or decompressed.
# The script uses multiprocessing to speed up the compression and decompression processes by utilizing multiple CPU cores.
# The script automatically determines the number of CPU cores available and uses them for parallel processing.
# The script prints messages to indicate the progress of the compression and decompression processes.
# The compressed files are saved with the ".compressed" extension, and the decompressed files are saved without the extension.
# The script can handle large files efficiently by splitting them into chunks and processing them in parallel.
# The script can be easily modified to change the chunk size or the number of workers for compression and decompression.
# The script is designed to be user-friendly and can be run from the command line or integrated into other scripts or applications.
# The script provides detailed comments and docstrings to explain the purpose and usage of each function.
# The script can be further optimized for performance by fine-tuning the chunk size, number of workers, or other parameters based on the system configuration and requirements.
# The script works with any type of file format, as it reads and writes files in binary mode, making it suitable for general-purpose compression and decompression tasks.