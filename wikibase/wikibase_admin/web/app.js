// Expose functions to Python
eel.expose(say_hello_js);
function say_hello_js(x) {
    console.log("Hello from " + x);
}

class ComponentLoader {
    constructor(elementId, componentPath) {
        this.element = document.getElementById(elementId);
        this.componentPath = componentPath;
        this.elementId = elementId;
        this.element.style.display = 'none';
    }

    loadComponent() {
        return fetch(this.componentPath)
            .then(response => response.text())
            .then(data => {
                this.element.innerHTML = data;
            })
            .catch(error => console.error(error));
    }

    hideComponents(elements) {
        elements.forEach(element => {
            if (element.id == this.elementId) {
                element.style.display = 'block';
            }
            else {
                element.style.display = 'none';
            }
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

loaders.forEach(loader => loader.loadComponent());
console.log(loaders)

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