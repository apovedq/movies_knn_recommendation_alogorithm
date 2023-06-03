

//Check connection with the server
async function logJSONData() {
  const response = await fetch("http://127.0.0.1:5001/");
  const jsonData = await response.json();
  return jsonData
}

const connectionComponent = document.getElementById("server-conection-status");

const myJsonResponse = logJSONData();
myJsonResponse.then((response) => {
    response != null || undefined ? myInfo.innerHTML = response.msg : "No hay conexion";
    connectionComponent.style.backgroundColor = "rgb(77, 237, 101)";
})


