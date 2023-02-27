import { components, loaders } from '../../App.js';

export function changePage(button) {
    loaders.forEach(loader => {
        if (loader.elementId === button.id.replace('-btn', '')) {
            const tabLink = document.querySelector(`#${loader.elementId}-tab a`);
            if (tabLink) {
                tabLink.dispatchEvent(new MouseEvent('click'));
                loader.hideComponents(components);
            } else {
                console.warn(`Could not find element for ${loader.elementId} component`);
            }
        }
    });
}