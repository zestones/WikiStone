import { components, loaders } from '../../App.js';

loaders.forEach(loader => {
    loader.loadComponent().then(() => {
        const tabLink = document.querySelector(`#${loader.elementId}-tab a`);
        const btn = document.querySelector(`#${loader.elementId}-btn`);

        if (tabLink && btn) {
            btn.addEventListener('click', () => {
                tabLink.dispatchEvent(new MouseEvent('click'));
                loader.hideComponents(components);
            });
        } else {
            console.warn(`Could not find element(s) for ${loader.elementId} component`);
        }
    });
});
