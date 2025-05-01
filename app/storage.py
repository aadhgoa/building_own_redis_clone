import json
import os
import threading
import time

DEFAULT_MEMORY_FILE = "memory.json"


def save_memory_to_file(memory: dict, filename="memory.json") -> None:
    """
    Save the memory dictionary to a file in JSON format.

    Args:
        memory (dict): The memory dictionary to save.
        filename (str): The name of the file to save the memory to.
    """
    try:
        with open(filename, 'w') as file:
            json.dump(memory, file)
        print(f"Memory saved successfully to {filename}")
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except PermissionError:
        print(f"Permission denied to write to {filename}.")
    except OSError as e:
        print(f"OS error: {e}")
    except TypeError:
        print(f"Error: Invalid data type in memory.")
    except ValueError:
        print(f"Error: Invalid value in memory.")
    except KeyboardInterrupt:
        print("Saving memory interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")

def load_memory_from_file(filename="memory.json") -> dict:
    """
    Load the memory dictionary from a file in JSON format.

    Args:
        filename (str): The name of the file to load the memory from.

    Returns:
        dict: The loaded memory dictionary.
    """
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                memory = json.load(file)
            print(f"Memory loaded from {filename}")
            return memory
        else:
            print(f"File {filename} not found.")
            return {}
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return {}
    except PermissionError:
        print(f"Permission denied to read from {filename}.")
        return {}
    except OSError as e:
        print(f"OS error: {e}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON data in {filename}.")
        return {}
    except TypeError:
        print(f"Error: Invalid data type in memory.")
        return {}
    except ValueError:
        print(f"Error: Invalid value in memory.")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}

def auto_save_memory(memory: dict, interval: int, stop_event: threading.Event, filename=DEFAULT_MEMORY_FILE):
    """
    Automatically save the memory dictionary to a file at regular intervals.

    Args:
        memory (dict): The memory dictionary to save.
        interval (int): The interval in seconds to save the memory.
        stop_event (threading.Event): Event to signal when to stop saving.
        filename (str): The name of the file to save the memory to.
    """
    while not stop_event.is_set():
        time.sleep(interval)
        save_memory_to_file(memory, filename)