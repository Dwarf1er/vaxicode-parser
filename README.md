# Vaxicode Parser

Vaxicode Parser aims at taking the Québec-issued PDF of your vaccination QR code and extracting the information that is contained in it.

## Getting Started

To clone and run this application, you'll need [Git](https://git-scm.com) and [Python](https://www.python.org/downloads/) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/Dwarf1er/vaxicode-parser.git

# Go into the repository
$ cd vaxicode-parser

# Install virtualenv
$ sudo pip install virtualenv

# Create a virtual environment
$ python -m venv .venv

# Activate the virtual environment
  #Windows:
$ .venv\Scripts\Activate.bat

  #MacOS and Linux:
$ source .venv/bin/activate

# Install the dependencies
$ pip install -r requirements.txt
```

## How To Use This Project

The script expects to receive the government-issued PDF filepath as a command-line argument, the script will then convert the PDF to a PNG to allow OpenCV to read and decode the QR code. Since the PDF has to be converted to a PNG before the QR code can be deconstructed and decrypted the process can take a while before completing.

```bash
# Go into the repository
$ cd vaxicode-parser

# Execute parse.py and pass the filepath to your government-issued PDF file containing your QR code
$ python parse.py path/to/your/PDF/QR/code
```

### Prerequisites
 
- [Git](https://git-scm.com)
- [Python](https://www.python.org/downloads/)

## Authors

  - **Antoine Poulin**
    [Dwarf1er](https://github.com/Dwarf1er)

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE)

## Acknowledgments

  - **Billie Thompson**, this README was based on the template provided [here](https://github.com/PurpleBooth/a-good-readme-template)
  - **Mikkel Paulson**, this project was inspired by the project found [here](https://github.com/MikkelPaulson/smart-health-card-parser)
