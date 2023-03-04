import { updateProperty } from "./property.js";

export function displayProperties(properties) {
    const propertyNames = Object.keys(properties);
    const propertyList = document.querySelector('#property-names');

    if (propertyNames.length === 0) {
        console.warn('No properties found.');
        return;
    }

    const firstPropertyName = propertyNames[0];

    propertyNames.forEach(name => {
        const li = document.createElement('li');
        
        li.textContent = name + ` (${properties[name].label})`;
        li.addEventListener('click', () => {
            // remove active class from any existing active list item
            const activeItem = propertyList.querySelector('.active');
            if (activeItem) activeItem.classList.remove('active');
            
            // add active class to the clicked item
            li.classList.add('active');
            displayPropertyDetails(properties, name);
        });

        propertyList.appendChild(li);
    });

    // add active class to the first item
    propertyList.querySelector(`li:first-child`).classList.add('active');
    displayPropertyDetails(properties, firstPropertyName);
}

function displayPropertyDetails(properties, name) {
    const property = properties[name];
    updateElementText('#property-title', property.label);
    updateElementText('#property-description', property.description);
    updateElementText('#property-type', `Type: ${property.type}`);
    
    showElement('#property-details');
    
    replaceOrAddModifyButton('.btn-modify', () => {
        // Add your code to modify the property here
        const newLabel = getElementText('#property-title');
        const newDescription = getElementText('#property-description');
        
        // Call a function to update the property with the new details
        updateProperty(name, newLabel, newDescription);
        
        // Update the fields
        updateElementText('#property-title', newLabel);
        updateElementText('#property-description', newDescription);
        
        // Update the data Object
        properties[name].label = newLabel;
        properties[name].description = newDescription;
        
        // Update the label
        const propertyList = document.querySelector('#property-names');
        let activeItem = propertyList.querySelector('.active');
        activeItem.textContent = name + ` (${properties[name].label})`;
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

function replaceOrAddModifyButton(selector, onClick) {
    const existingButton = document.querySelector(selector);
    
    if (existingButton) existingButton.remove();

    const button = document.createElement('button');
    
    button.innerHTML = '<i class="fas fa-edit"></i>Modify';
    button.classList.add('btn-modify');
    button.onclick = onClick;
    
    document.querySelector('#property-details').appendChild(button);
}