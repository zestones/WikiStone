import { displayPropertyDetails } from "./displayProperty.js";

export function displayCreation() {
    document.querySelector("#property-details").style.display = "none";
    document.querySelector("#property-creation").style.display = "block";
}

export function createProperty() {
    const label = getElementText("#creation-title");
    const description = getElementText("#creation-description");
    const type = getElementText("#creation-type");

    createNewProperty(label, description, type)
        .then((id) => {
            const propertyList = document.querySelector('#property-names');

            // add active class to the clicked item
            const li = document.createElement('li');

            // Hide creation
            document.querySelector("#property-creation").style.display = "none";
            document.querySelector("#property-details").style.display = "block";

            // remove content of creation
            document.querySelector("#creation-title").innerHTML = "Enter a Title";
            document.querySelector("#creation-description").innerHTML = "Enter a Description";
            document.querySelector("#creation-type").innerHTML = "Enter a Type";

            li.textContent = id + ` (${label})`;

            updateElementText('#property-title', label);
            updateElementText('#property-description', description);
            updateElementText('#property-type', `Type: ${type}`);

            li.addEventListener('click', () => {
                // remove active class from any existing active list item
                const activeItem = propertyList.querySelector('.active');
                if (activeItem) activeItem.classList.remove('active');

                // Hide creation
                document.querySelector("#property-creation").style.display = "none";

                const properties = {};
                properties[id] = { label, description, type };

                // add active class to the clicked item
                li.classList.add('active');
                displayPropertyDetails(properties, id);
            });

            propertyList.appendChild(li);
            
            // Scroll to the position of the li
            li.scrollIntoView({ behavior: "smooth" });
            li.click();

            showElement('#property-details');

        }).catch((error) => {
            console.log(error);
        });
}

function getElementText(selector) {
    return document.querySelector(selector).textContent;
}

function updateElementText(selector, text) {
    document.querySelector(selector).textContent = text;
}

function showElement(selector) {
    document.querySelector(selector).style.display = 'block';
}

async function createNewProperty(label, description, type) {
    return await eel.createProperty(label, description, type)();
}

// Get the elements
const titleElement = document.querySelector("#creation-title");
const descriptionElement = document.querySelector("#creation-description");
const typeElement = document.querySelector("#creation-type");

// Store the original content of each element
const titleOriginalContent = titleElement.innerHTML;
const descriptionOriginalContent = descriptionElement.innerHTML;
const typeOriginalContent = typeElement.innerHTML;

function updateEditableContent(element, content) {
    if (element.innerHTML === "") element.innerHTML = content;
}

function clearEditableContent(element, originalContent) {
    if (element.innerHTML === originalContent) element.innerHTML = "";
}

// Add blur event listeners
titleElement.addEventListener("blur", function () {
    updateEditableContent(titleElement, titleOriginalContent);
});

descriptionElement.addEventListener("blur", function () {
    updateEditableContent(descriptionElement, descriptionOriginalContent);
});

typeElement.addEventListener("blur", function () {
    updateEditableContent(typeElement, typeOriginalContent);
});


// Add focus event listeners
titleElement.addEventListener("focus", function () {
    clearEditableContent(titleElement, titleOriginalContent);
});

descriptionElement.addEventListener("focus", function () {
    clearEditableContent(descriptionElement, descriptionOriginalContent);
});

typeElement.addEventListener("focus", function () {
    clearEditableContent(typeElement, typeOriginalContent);
});