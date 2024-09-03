import os
import moviepy.editor as mp
import random
import string
import time

# Supported audio file extensions
SUPPORTED_EXTENSIONS = ['.mp3', '.wav', '.ogg', '.flac']

def get_audio_files(directory):
    """Returns a list of audio files in the given directory."""
    audio_files = []
    for filename in os.listdir(directory):
        if os.path.splitext(filename)[1].lower() in SUPPORTED_EXTENSIONS:
            audio_files.append(filename)
    return audio_files

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

def compress_audio(file_path, output_path, target):
    """Compresses the audio file at the given path and saves it to the output path."""
    audio = mp.AudioFileClip(file_path)
    compressed_audio = audio.volumex(target / 100)
    compressed_audio.write_audiofile(output_path)

def calculate_file_size(file_path):
    """Returns the file size in bytes."""
    return os.path.getsize(file_path)

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
            break  # Exit the loop after processing all files
        
        if not file_name:
            # Just list all files and prompt again
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
        
        # Prompt for the output directory after file selection
        output_directory = input("Enter the output location for the compressed file: ")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        output_file_name = f"{os.path.splitext(file_name)[0]}_{''.join(random.choice(string.ascii_uppercase) for _ in range(5))}.mp3"
        output_path = os.path.join(output_directory, output_file_name)
        
        target = get_compression_target()
        start_time = time.time()
        
        # Compress the audio file
        original_file_path = os.path.join(directory, file_name)
        compress_audio(original_file_path, output_path, target)
        
        # Calculate file size reduction
        original_size = calculate_file_size(original_file_path)
        compressed_size = calculate_file_size(output_path)
        size_reduction_percentage = ((original_size - compressed_size) / original_size) * 100
        
        file_compression_results.append((output_file_name, size_reduction_percentage))
        
        elapsed_time = time.time() - start_time
        print(f"Compression completed in {elapsed_time:.2f} seconds")
        break  # Exit the loop after processing the selected file

    # Print the results for all files
    print("\nCompressed files and size reduction percentages:")
    for i, (file_name, reduction) in enumerate(file_compression_results):
        print(f"{i+1}. {file_name} - Reduction: -{reduction:.2f}%")

if __name__ == "__main__":
    main()
