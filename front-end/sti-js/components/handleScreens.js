
function handleSetWeightsScreen() {
    let mainScreen = document.getElementById('main-screen');
    mainScreen.classList.remove('screen-act')
    mainScreen.classList.add('screen-off')

    let weightScreen = document.getElementById('weights-screen');
    weightScreen.classList.remove('screen-off')
    weightScreen.classList.add('screen-act')
}

function handleShowResultsScreen() {
    let weightScreen = document.getElementById('weights-screen');
    weightScreen.classList.remove('screen-act')
    weightScreen.classList.add('screen-off')

    let resultsScreen = document.getElementById('results-screen');
    resultsScreen.classList.remove('screen-off')
    resultsScreen.classList.add('screen-act')
}