class ComponentLoader {

    constructor(elementId, componentPath) {
        this.element = document.getElementById(elementId);
        this.componentPath = componentPath;

        this.elementId = elementId;
        this.element.style.display = 'none';

        this.htmlContent = null;
    }

    loadComponent() {
        return fetch(this.componentPath)
            .then(response => response.text())
            .then(data => {
                this.htmlContent = data;
                this.element.innerHTML = data;
            })
            .catch(error => console.error(error));
    }

    hideComponents(elements) {
        elements.forEach(element => {
            if (element.id == this.elementId) {
                element.style.display = 'block';
            } else {
                element.style.display = 'none';
            }
        });
    }

    loadScripts() {
        if (!this.htmlContent) {
            console.error('HTML content not loaded yet.');
            return;
        }

        const parser = new DOMParser();
        const html = parser.parseFromString(this.htmlContent, 'text/html');
        const body = html.querySelector('body');
        const scripts = html.querySelectorAll('script');

        scripts.forEach(script => {
            const scriptTag = document.createElement('script');
            scriptTag.type = script.type;
            
            if (script.src) scriptTag.src = script.src;
            else scriptTag.textContent = script.textContent;
            
            document.body.appendChild(scriptTag);
        });
    }

}


const tabs = [
    { id: 'home', path: 'components/home/home.html', tabId: 'home-tab' },
    { id: 'source', path: 'components/source/source.html', tabId: 'source-tab' },
    { id: 'property', path: 'components/property/property.html', tabId: 'property-tab' },
    { id: 'settings', path: 'components/settings/settings.html', tabId: 'settings-tab' }
];

export const components = tabs.map(tab => document.getElementById(tab.id));
export const loaders = tabs.map(tab => new ComponentLoader(tab.id, tab.path));
export const tabsElements = tabs.map(tab => document.querySelector(`#${tab.tabId}`));

Promise.all(loaders.map(loader => loader.loadComponent())).then(() => {
    loaders.forEach(loader => loader.loadScripts());
});

function hideAllComponents() {
    components.forEach(component => component.style.display = 'none');
}

function showComponent(component) {
    component.style.display = 'block';
}

function onTabClick(tabIndex) {
    hideAllComponents();
    showComponent(components[tabIndex]);
}

tabsElements.forEach((tab, index) => {
    tab.addEventListener('click', () => onTabClick(index));
});

// Load the home component by default
showComponent(components[0]);