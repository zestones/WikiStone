function processData(button) {
    
    const animation = document.querySelector(`.processing.${button.id.split('-')[0]}`);
    animation.classList.add('processing-animation');
    animation.style.display = 'inline-block';

    button.style.display = 'none';

    getDataFromPython(button.id).then((data) => {
        animation.style.display = 'none';
        button.style.display = 'block';
    });
}

async function getDataFromPython(buttonId) {
    if (buttonId.includes('json')) {
        await eel.process_api_data()();
    }
    else if (buttonId.includes('csv')) {
        await eel.process_csv_data()();
    }
    else if (buttonId.includes('web')) {
        await eel.process_web_data()();
    }
}
