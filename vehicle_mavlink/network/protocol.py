import json

def encode_message(data_dict):
    """
    Takes a Python dictionary, converts to JSON string,
    and appends a newline character for framing.
    Returns bytes encoded in utf-8.
    """
    try:
        json_str = json.dumps(data_dict)
        return (json_str + "\n").encode('utf-8')
    except Exception as e:
        print(f"[ERROR] Could not encode message: {e}")
        return b""

class MessageBuffer:
    """
    Helper class to buffer incoming bytes and extract complete
    newline-delimited JSON messages.
    """
    def __init__(self):
        self.buffer = ""

    def add_data(self, data_bytes):
        """
        Adds newly received bytes to the buffer.
        """
        try:
            self.buffer += data_bytes.decode('utf-8')
        except UnicodeDecodeError:
            print("[ERROR] Invalid utf-8 data received.")

    def get_messages(self):
        """
        Extracts all complete newline-delimited JSON messages from the buffer.
        Returns a list of parsed Python dictionaries.
        """
        messages = []
        while "\n" in self.buffer:
            line, self.buffer = self.buffer.split("\n", 1)
            line = line.strip()
            if line:
                try:
                    msg = json.loads(line)
                    messages.append(msg)
                except json.JSONDecodeError:
                    print(f"[ERROR] Invalid JSON message received: {line}")
        return messages
