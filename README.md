# VaxiCode Parser

The VaxiCode Parser is a command-line tool for decoding Smart Health Card (SHC) information from QR codes embedded in PDFs, images, or provided as a string.

## Project Description

The Smart Health Card (SHC) is a standard format for securely storing and sharing COVID-19 vaccination and testing information. This tool helps decode the encoded health information contained within SHC QR codes, allowing users to view the decoded data in a human-readable format.

## Webpage Version

Alternatively, a webpage version of the VaxiCode Parser is available, providing a user-friendly interface for decoding SHC information. The webpage runs entirely on the client-side, ensuring that no data is stored or sent anywhere. Users can upload PDF files, images, or enter SHC strings directly for decoding. The decoded information is displayed on the webpage for easy access.

You can access the webpage version of the VaxiCode Parser [here](https://antoinepoulin.com/vaxicode-parser)

**NOTE: To use the PDF/image decoding features you need to have canvas reading enabled in your browser for QR codes to be read with JavaScript (privacy.resistFingerprinting must be turned off for Firefox users)**

## Prerequisites

Before installing and using the VaxiCode Parser, ensure you have the following prerequisites:

- **Python**: Ensure you have Python (>=3.6) installed on your system.
- **Poppler**: For decoding PDF files, you need to have Poppler installed. Instructions for installing Poppler on different operating systems are provided below.
- **Poetry**: Poetry is a dependency manager for Python projects. You'll need Poetry to install and manage the dependencies for this project. Follow the installation instructions below.

## Installing Poppler

### Linux (Ubuntu/Debian)

```bash
sudo apt update && sudo apt upgrade
sudo apt install poppler-utils
```
### MacOS

```bash
brew install poppler
```

### Windows
1. Download the latest version of Poppler from [oschwartz10612/poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases)
2. Extract the latest release .zip to C:\Program Files
3. Add the absolute path to the Poppler bin directory to your system PATH

## Installing Poetry

To install Poetry, run the following command:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

For detailed installation instructions, refer to the [Poetry documentation](https://python-poetry.org/docs/#installing-with-the-official-installer).

## Installation

To install the VaxiCode Parser and its dependencies, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/Dwarf1er/vaxicode-parser.git
```

2. Navigate to the project directory:
```bash
cd path/to/vaxicode-parser
```

3. Install dependencies using Poetry:
```bash
poetry install
```

## Usage

After installing the VaxiCode Parser, you can use it to decode SHC information from PDFs, images, or SHC strings using the following command-line interface:

1. Enter the poetry virtual environment:

```bash
poetry shell
```
2. Use the command line interface:
```bash
python vaxicode-parser.py --pdf <path_to_pdf_file>
python vaxicode-parser.py --image <path_to_image_file>
python vaxicode-parser.py --shc <shc_string>
```
Replace <path_to_pdf_file>, <path_to_image_file>, and <shc_string> with the appropriate values.

## Authors

  - **Antoine Poulin**
    [Dwarf1er](https://github.com/Dwarf1er)

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE)

## Acknowledgments

  - **Billie Thompson**, this README was based on the template provided [here](https://github.com/PurpleBooth/a-good-readme-template)
  - **Mikkel Paulson**, this project was inspired by the project found [here](https://github.com/MikkelPaulson/smart-health-card-parser)
