class Utils:

    def save_json_to_file(self, data, filename):
            try:
                with open(filename, 'w') as file:
                    json.dump(data, file, indent=4)
                print(f"Data saved to {filename}")
            except IOError as e:
                print(f"Error saving file: {e}")