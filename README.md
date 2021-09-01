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

This script can receive 3 different input formats:
  - The government-issued PDF file containing your QR code
  - A PNG file containing your QR code
  - The SHC contained in your QR code

#### To Use This Project With A PDF

```bash
# Go into the repository
$ cd vaxicode-parser

# Execute parse.py and pass the filepath to your government-issued PDF file containing your QR code
$ python parse.py -p path/to/your/PDF/QR/code
```

#### To Use This Project With A PNG

```bash
# Go into the repository
$ cd vaxicode-parser

# Execute parse.py and pass the filepath to your government-issued PDF file containing your QR code
$ python parse.py -i path/to/your/PNG/QR/code
```

#### To Use This Project With A SHC

```bash
# Go into the repository
$ cd vaxicode-parser

# Execute parse.py and pass the filepath to your government-issued PDF file containing your QR code
$ python parse.py -s 'your SHC here'
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
