# PCBuilderBackend

This project is a Python-based web application that generates optimised PC builds based on a user-specified budget. 
It uses Flask for the backend, MongoDB for data storage, and Beautiful Soup for scraping up-to-date part data.

## Features

- Budget-based PC build generation
- Ability to edit generated builds on the fly to meet expectations
- Web scraping for current part prices and specifications
- MongoDB integration for efficient data storage and retrieval
- RESTful API for easy frontend integration

## Technologies Used

- Python 3.8+
- Flask
- MongoDB
- Beautiful Soup 4
- Requests

## Installation

1. Clone the repository and go to that directory

2. Set up a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies:
   pip install -r requirements.pip

4. Create a .env file in the root directory and create environment variables that are called in pc_builder_backend/constants.py

## API Reference

Detailed API documentation can be found [HERE]() file.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## Frontend

The frontend for this project can be found at: [PCBuildGeneratorFrontend](https://github.com/Cian-McKelvey/PCBuilderFrontend)

## Acknowledgments

- X.

## Contact

If you have any questions or feedback, please open an issue on this repository.