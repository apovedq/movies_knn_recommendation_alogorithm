// Different localhosts
const LOCALHOST = "http://127.0.0.1:5001";

// Post method function
async function postData(url = "", data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Content-Type": "application/json",
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify(data), // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}

//Bring user from the db
async function bringUser(url) {
  const response = await fetch(url);
  const jsonData = await response.json();
  return jsonData
}


//Function to check name actualized
async function handleSetUserName() {

  const myUser = document.getElementById("myUser")

const userFromDB = (bringUser( LOCALHOST + "/getCurrentUser"))
userFromDB.then((response) => {myUser.innerText = `Esta es nuestra recomendacion para ti `  + response.msg})
}

//Changes and save the user choosen in the db
async function handleSaveNameinDB() {

  //Get my element from the html document
  let dropdown = document.getElementById("names_dropdown");
  let  selectedName = dropdown.value;

  //Funcion para verificar que se escoja el nombre y que se mande a la base de datos
  if (selectedName !== "") {
    await postData(LOCALHOST + "/post_name", { answer: selectedName }).then((raw) => 
        (raw.response.answer)
    ).then((response) => { console.log("Nombre guardado en la base de datos: " + response) });

    // Aquí puedes realizar otras acciones con el valor seleccionado
  } else {
    alert("Por favor, selecciona un nombre");
  }
}

let selectedMethod = "";

//Save the aggregation method choosen in the db
async function handleGetAgregattionMethod() {
  let dropdown = document.getElementById("agregation_dropdown");
  selectedMethod = parseInt(dropdown.value);
  console.log(selectedMethod);

  let explainedMethod = document.getElementById("explained-method");

  if (selectedMethod === 0) {
    console.log("aqui");
    explainedMethod.innerText = "En este caso, calcularías el promedio de las preferencias de todos tus amigos. Cada uno daría su opinión y luego se sumarían todas las puntuaciones y se dividirían entre el número de amigos. El resultado final sería el promedio de las valoraciones individuales.";
  } else if (selectedMethod === 1) {
    explainedMethod.innerText = "Con este enfoque, elegirías la película que evite la mayor cantidad de insatisfacción entre tus amigos. Tomarías en cuenta la opinión del amigo menos interesado o menos entusiasmado y elegirías la película que a él o ella le parezca más aceptable, incluso si otros amigos tienen preferencias más altas.";
  } else if (selectedMethod === 2) {
    explainedMethod.innerText = "Aquí buscarías maximizar el disfrute de tus amigos. Considerarías las preferencias individuales y seleccionarías la película que tenga la puntuación más alta o que la mayoría de tus amigos estén emocionados por ver.";
  } else if (selectedMethod === 3) {
    explainedMethod.innerText = "En este caso, calcularías el promedio de las preferencias, pero dándole más peso a las opiniones de tus amigos más satisfechos. Tomarías en cuenta las preferencias de todos, pero considerarías más las opiniones de aquellos amigos que estén más emocionados o satisfechos con la elección.";
  }

   await postData(LOCALHOST + "/post_method", { answer: selectedMethod }).then((raw) => 
        raw.response.answer
    ).then((response) => { console.log("Metodo guardado en la base de datos: " + response) });
}

let sliderValues = [];

//Save the slider values choosen in the db
async function handleGetSlidersValue() {
  sliderValues = [];
  actors.forEach((actor) => {
    let nameIdentifier = actor.name.substring(0, actor.name.indexOf(" "));
    let currentValue = document.getElementById(nameIdentifier).value;
    sliderValues.push(currentValue)
  })

  await postData(LOCALHOST + "/post_slider_values", { answer: sliderValues }).then((raw) => 
        (raw.response.answer)
    ).then((response) => { console.log("Valores de slider guardados en la base de datos: " + response) });
}

//Save the # of neighboors 
let knnValue = ""
async function handleGetKnnValue() {
  knnValue = document.getElementById("knn-value").value
  
  await postData(LOCALHOST + "/post_knn_value", { answer: knnValue }).then((raw) => 
        (raw.response.answer)
    ).then((response) => { console.log("El valor de vecinos se ha guardado en la base de datos: " + response) });
}



//Send all the info to the db 
async function setVariables() {
  handleSaveNameinDB()
  handleGetAgregattionMethod()
  handleGetKnnValue()
}

document.getElementById("continue-btn").addEventListener("click", setVariables);

// shows the result screen
async function handleSetInfoInDB() {
  handleGetSlidersValue()
  handleSetUserName()

  handleSetResults()
  handleShowResultsScreen() 
}








