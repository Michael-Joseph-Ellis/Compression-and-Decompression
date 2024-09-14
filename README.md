# Parallel Compression/Decompression Module
This project is a Python-based module for efficient file compression and decompression using `zlib` and `multiprocessing`. By leveraging parallel processing, the tool can handle large datasets efficiently, making it suitable for general-purpose tasks or integration into larger projects.

## Features
- **Parallel Processing**: Utilizes multiple CPU cores to speed up compression and decompression.
- **Customizable Parameters**: Users can specify chunk size and the number of worker processes to optimize performance for different systems.
- **Modular Design**: Can be easily integrated into larger projects.
- **Wide File Format Support**: Works with any file type, as it reads and writes files in binary mode.
- **User-Friendly**: Designed to be simple to run via command line or as part of other scripts/applications.

## Syntax 

### Compression

```Python 
compress_folder(decompressed_input, compressed_output, chunk_size, num_workers)
```

- `decompressed_input`: Path to the file/folder content needed to be compressed.
- `compressed_output`: Path to save the compressed content.
- `chunk_size`: (int) Size of each chunk to split the file data into (recommended: 1MB = 1048576 bytes).
- `num_workers`: (int) Number of worker processes to use for parallel decompression.

### Decompression

```Python 
decompress_folder(compressed_input, decompressed_output, chunk_size, num_workers)
```

- `compressed_folder`: Path to the folder containing compressed files.
- `output_folder`: Path to save decompressed files.
- `chunk_size`: (int) Size of each chunk to split the compressed data into (recommended: 1MB = 1048576 bytes).
- `num_workers`: (int) Number of worker processes to use for parallel decompression.

### Example

```Python
compress_folder("/path/to/decompressed", "/path/to/compressed", 1024 * 1024, 8)
decompress_folder("/path/to/compressed", "/path/to/decompressed", 1024 * 1024, 8)
```

### Smaller Notes

- The input data is split into chunks, each of a defined size. 
- The chunks are processed in parallel  by multiple worker processes using Python's `multiprocessing` library.
- Each chunk is either compressed or decompressed using `zlib`.
- The processed chunks are recombined into a single output file. 
- Adjust `chunk_size` based on file size and system memory for optimal results. 
- Use `num_workers` argument to match your system's CPU core count minus 2 - 4 for faster processing. 

## License 
This project is licensed under MIT License.  
