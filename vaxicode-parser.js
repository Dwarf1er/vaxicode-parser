function urlSafeBase64Decode(base64UrlSafeString) {
    const base64String = base64UrlSafeString.replace(/-/g, "+").replace(/_/g, "/");

    const binaryString = atob(base64String);

    const length = binaryString.length;
    const bytes = new Uint8Array(length);
    for (let i = 0; i < length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }

    return bytes;
}

function readFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => resolve(event.target.result);
        reader.onerror = (error) => reject(error);
        reader.readAsArrayBuffer(file);
    });
}

async function pdfToImage(pdfInput) {
    const arrayBuffer = await readFile(pdfInput);
    const pdf = await pdfjsLib.getDocument(arrayBuffer).promise;
    const page = await pdf.getPage(1);
    const viewport = page.getViewport({ scale: 2.0 });
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    canvas.width = viewport.width;
    canvas.height = viewport.height;
    const renderContext = { canvasContext: context, viewport: viewport };
    await page.render(renderContext).promise;
    return new Promise((resolve, reject) => {
        canvas.toBlob((blob) => {
            if (blob) {
                resolve(blob);
            } else {
                reject(new Error("Failed to convert canvas to blob."));
            }
        });
    });
}

function getImageData(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => {
            const image = new Image();
            image.onload = () => {
                const canvas = document.createElement("canvas");
                const context = canvas.getContext("2d");
                canvas.width = image.width;
                canvas.height = image.height;
                context.drawImage(image, 0, 0);
                resolve(context.getImageData(0, 0, canvas.width, canvas.height));
            };
            image.onerror = (error) => reject(error);
            image.src = event.target.result;
        };
        reader.onerror = (error) => reject(error);
        reader.readAsDataURL(file);
    });
}

async function readQRCode(imageInput) {
    const imageData = await getImageData(imageInput);
    const code = jsQR(imageData.data, imageData.width, imageData.height);
    const errorElement = document.getElementById("errorOutput");

    if (code) {
        return code.data;
    } else {
        errorElement.style.color = "red";
        errorElement.textContent = "No QR code was found in this image, or reading information from canvas is disabled in your browser";
        return null;
    }
}

function shcToJwt(shcString) {
    shcString = shcString.split("/")[1];
    
    const pairs = [];
    for (let i = 0; i < shcString.length; i += 2) {
        pairs.push(shcString.slice(i, i + 2));
    }

    const asciiChars = [];
    for (const pair of pairs) {
        const asciiChar = parseInt(pair, 10);
        asciiChars.push(String.fromCharCode(asciiChar + 45));
    }

    const jwt = asciiChars.join("");

    return jwt;
}

function decodeJwt(jwt) {
    const [header, payload, signature] = jwt.split(".");

    const base64UrlSafePayload = urlSafeBase64Decode(payload);
    const inflatedPayload = pako.inflateRaw(base64UrlSafePayload);
    const decodedPayload = new TextDecoder().decode(inflatedPayload);

    return decodedPayload;
}

async function decodeShc() {
    const shcInput = document.getElementById("shcInput").value.trim();
    const imageInput = document.getElementById("imageInput").files[0];
    const pdfInput = document.getElementById("pdfInput").files[0];

    const errorElement = document.getElementById("errorOutput");
    errorElement.style.color = "red";
    errorElement.textContent = "";

    try {
        let shcString;

        if (pdfInput) {
            const imageBlob = await pdfToImage(pdfInput);
            shcString = await readQRCode(imageBlob);
            document.getElementById("pdfInput").value = null;
        } else if (imageInput) {
            shcString = await readQRCode(imageInput);
            document.getElementById("imageInput").value = null;
        } else if (shcInput) {
            shcString = shcInput;
            document.getElementById("shcInput").value = null;
        } else {
            throw new Error("Please provide either a SHC string, QR code image, or PDF!");
        }

        if (shcString) {
            const jwt = shcToJwt(shcString);
            const decodedData = decodeJwt(jwt);
            const decodedOutput = JSON.stringify(JSON.parse(decodedData), null, 4);
            document.getElementById("decodedOutput").value = decodedOutput;
        } else {
            throw new Error("SHC string is empty.");
        }
    } catch (error) {
        errorElement.textContent = error.message;
    }
}
