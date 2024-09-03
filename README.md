---

# Audio File Compressor

## Overview

The Audio File Compressor is a Python script designed to compress audio files in various formats using a specified target percentage. It allows users to compress individual files or all audio files in a directory, and it provides detailed information about file size reductions.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Compress a Single File](#compress-a-single-file)
  - [Compress All Files in a Directory](#compress-all-files-in-a-directory)
- [Code Breakdown](#code-breakdown)
  - [Functions](#functions)
  - [Main Logic](#main-logic)
- [Case Examples](#case-examples)
- [License](#license)

## Features

- Supports various audio file formats: `.mp3`, `.wav`, `.ogg`, `.flac`
- Compresses audio files with a specified target percentage
- Can compress a single file or all files in a directory
- Outputs the new file names and percentage reduction in size

## Installation

1. **Ensure Python is Installed**

   Make sure you have Python 3.6 or higher installed on your system. You can download Python from the [official website](https://www.python.org/downloads/).

2. **Install Required Libraries**

   You need to install the following Python libraries:
   - `moviepy`
   - `tqdm`

   You can install them using pip:

   ```bash
   pip install moviepy tqdm
   ```

## Usage

### Compress a Single File

1. **Run the Script**

   Execute the script from the command line:

   ```bash
   python audio_compressor.py
   ```

2. **Provide Input**

   - **Directory Location**: Enter the directory where your audio files are located.
   - **File Selection**: Enter the name of the file you want to compress or type 'all' to compress all files.
   - **Output Location**: Specify where you want the compressed file(s) to be saved.
   - **Compression Target**: Enter the target percentage for compression (1-200%).

3. **View Results**

   After compression, the script will display the compressed file names and the percentage reduction in file size.

### Compress All Files in a Directory

1. **Run the Script**

   Execute the script as described above.

2. **Provide Input**

   - **Directory Location**: Enter the directory where your audio files are located.
   - **File Selection**: Type 'all' to compress all files in the directory.
   - **Output Location**: Specify where you want the compressed files to be saved.
   - **Compression Target**: Enter the target percentage for compression (1-200%).

3. **View Results**

   The script will list all the compressed files along with their size reduction percentages.

## Code Breakdown

### Functions

#### `get_audio_files(directory)`

Returns a list of audio files with supported extensions in the given directory.

```python
def get_audio_files(directory):
    """Returns a list of audio files in the given directory."""
    audio_files = []
    for filename in os.listdir(directory):
        if os.path.splitext(filename)[1].lower() in SUPPORTED_EXTENSIONS:
            audio_files.append(filename)
    return audio_files
```

#### `get_compression_target()`

Prompts the user for the compression target percentage and validates the input.

```python
def get_compression_target():
    """Asks the user for the compression target percentage."""
    while True:
        try:
            target = float(input("Enter the compression target percentage (1-200): "))
            if 1 <= target <= 200:
                return target
            else:
                print("Please enter a value between 1 and 200.")
        except ValueError:
            print("Invalid input. Please enter a number.")
```

#### `compress_audio(file_path, output_path, target)`

Compresses the audio file and saves it to the specified output path.

```python
def compress_audio(file_path, output_path, target):
    """Compresses the audio file at the given path and saves it to the output path."""
    audio = mp.AudioFileClip(file_path)
    compressed_audio = audio.volumex(target / 100)
    compressed_audio.write_audiofile(output_path)
```

#### `calculate_file_size(file_path)`

Returns the size of the file in bytes.

```python
def calculate_file_size(file_path):
    """Returns the file size in bytes."""
    return os.path.getsize(file_path)
```

### Main Logic

The `main` function controls the flow of the script:

1. **Directory Validation**: Checks if the provided directory exists.
2. **File Listing**: Lists audio files in the directory.
3. **User Input**: Handles user input for file selection, output directory, and compression target.
4. **Compression**: Compresses files based on user input and calculates size reductions.
5. **Results Display**: Outputs the names of compressed files and their size reductions.

```python
def main():
    print("Supported audio file extensions:")
    for ext in SUPPORTED_EXTENSIONS:
        print(ext)
    
    directory = input("Enter the location of the audio files: ")
    if not os.path.exists(directory):
        print("Invalid directory. Please try again.")
        return
    
    audio_files = get_audio_files(directory)
    if not audio_files:
        print("No audio files found in the given directory.")
        return
    
    print("Found the following audio files:")
    for i, file in enumerate(audio_files):
        print(f"{i+1}. {file}")
    
    file_compression_results = []

    while True:
        file_name = input("Enter the name of the file you want to compress (or type 'all' to compress all files, or press enter to list all files): ")
        
        if file_name.lower() == "all":
            output_directory = input("Enter the output location for the compressed files: ")
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            
            target = get_compression_target()
            start_time = time.time()
            
            for audio_file in audio_files:
                original_file_path = os.path.join(directory, audio_file)
                output_file_name = f"{os.path.splitext(audio_file)[0]}_{''.join(random.choice(string.ascii_uppercase) for _ in range(5))}.mp3"
                output_path = os.path.join(output_directory, output_file_name)
                
                compress_audio(original_file_path, output_path, target)
                
                # Calculate file size reduction
                original_size = calculate_file_size(original_file_path)
                compressed_size = calculate_file_size(output_path)
                size_reduction_percentage = ((original_size - compressed_size) / original_size) * 100

                file_compression_results.append((output_file_name, size_reduction_percentage))
            
            elapsed_time = time.time() - start_time
            print(f"Compression completed in {elapsed_time:.2f} seconds for all files.")
            break
        
        if not file_name:
            continue
        
        matching_files = [file for file in audio_files if file.lower().startswith(file_name.lower())]
        if not matching_files:
            print("No matching files found. Please try again.")
            continue
        
        if len(matching_files) > 1:
            print("Multiple matching files found. Please select one:")
            for i, file in enumerate(matching_files):
                print(f"{i+1}. {file}")
            
            while True:
                try:
                    choice = int(input("Enter the number of your choice: "))
                    if 1 <= choice <= len(matching_files):
                        file_name = matching_files[choice-1]
                        break
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            file_name = matching_files[0]
        
        output_directory = input("Enter the output location for the compressed file: ")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        output_file_name = f"{os.path.splitext(file_name)[0]}_{''.join(random.choice(string.ascii_uppercase) for _ in range(5))}.mp3"
        output_path = os.path.join(output_directory, output_file_name)
        
        target = get_compression_target()
        start_time = time.time()
        
        original_file_path = os.path.join(directory, file_name)
        compress_audio(original_file_path, output_path, target)
        
        original_size = calculate_file_size(original_file_path)
        compressed_size = calculate_file_size(output_path)
        size_reduction_percentage = ((original_size - compressed_size) / original_size) * 100
        
        file_compression_results.append((output_file_name, size_reduction_percentage))
        
        elapsed_time = time.time() - start_time
        print(f"Compression completed in {elapsed_time:.2f} seconds")
        break

    print("\nCompressed files and size reduction percentages:")
    for i, (file_name, reduction) in enumerate(file_compression_results):
        print(f"{i+1}. {file_name} - Reduction: -{reduction:.2f}%")
```

## Case Examples

### Case 1: Compressing a Single File

**Scenario:** You have a file named `example.mp3` in the directory `C:/audio_files` and want to compress it to 50% of its original size.

**Steps:**
1. Run the script:

   ```bash
   python audio_compressor.py
   ```

2. Enter the directory:

   ```
   C:/audio_files
   ```

3. Enter the file name:

   ```
   example
   ```

4. Enter the output location:

   ```
   C:/compressed_files
   ```

5. Enter the compression target:

   ```
   50
   ```

**Result:** The script compresses `example.mp3` to a file in `C:/compressed_files` and outputs the percentage reduction in size.

### Case 2: Compressing All Files in a Directory

**Scenario:** You want to compress all audio files in the directory `C:/audio_files` to 30% of their original size.

**Steps:**
1. Run the script:

   ```bash
   python audio_compressor.py
   ```

2. Enter the directory:

   ```
   C:/audio_files
   ```

3. Type `all` when prompted for the file name:

   ```
   all
   ```

4. Enter the output location:

   ```
   C:/compressed_files
   ```

5. Enter the compression target:

   ```
   30
   ```

**Result:** The script compresses all audio files in `C:/audio_files` and saves them to `C:/compressed_files`. It then outputs the file names and percentage reductions for all compressed files.

**Steps:**
1. Run the script.
2. Enter `C:/audio_files` when prompted for the directory.
3. Enter `example` when prompted for the file name.
4. Enter `C:/compressed_files

## License

This script is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
