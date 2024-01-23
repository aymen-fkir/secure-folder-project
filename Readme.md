# Secure Folder Project

The Secure Folder project is a simple security system that uses facial recognition to control access to a folder. Users can add their face encoding to a database, and the system will lock or unlock the specified folder based on facial recognition.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- OpenCV
- face_recognition
- Supabase (Database)
- NumPy

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your_username/secure-folder-project.git
    cd secure-folder-project
    ```

2. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your environment variables:**

    Create a `.env` file in the project directory with the following content:

    ```env
    project_url=your_supabase_project_url
    secret_key=your_supabase_secret_key
    ```
  ```

## Contributing

Contributions are welcome! If you find any issues or have ideas for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
