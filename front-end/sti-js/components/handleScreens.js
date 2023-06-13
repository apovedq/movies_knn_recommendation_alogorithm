async function getFromDB(url) {
  const response = await fetch(url);
  const jsonData = await response.json();
  return jsonData
}

async function resetDB() {

const reset = getFromDB("http://127.0.0.1:5001/")
    reset.then((response) => {
        console.log(response);
    })
}

function handleSetWeightsScreen() {
    let weightScreen = document.getElementById('weights-screen');
    weightScreen.classList.remove('screen-off')
    weightScreen.classList.add('screen-act')
}

function handleShowResultsScreen() {

    let resultsScreen = document.getElementById('results-screen');
    resultsScreen.classList.remove('screen-off')
    resultsScreen.classList.add('screen-act')
}

function resetScreens() {
    let weightScreen = document.getElementById('weights-screen');
    weightScreen.classList.remove('screen-act')
    weightScreen.classList.add('screen-off')

    let resultsScreen = document.getElementById('results-screen');
    resultsScreen.classList.remove('screen-act')
    resultsScreen.classList.add('screen-off')
    
    const recommendedUsersComponent = document.getElementById("recommended-users");
    recommendedUsersComponent.innerHTML = ``;
    resetDB();
}
