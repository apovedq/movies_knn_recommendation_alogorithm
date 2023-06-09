async function getFromDB(url) {
  const response = await fetch(url);
  const jsonData = await response.json();
  return jsonData
}

//Function to bring recommended users from db
async function handleSetRecommenedUsers() {
const recommendedUsersComponent = document.getElementById("recommended-users");
    
const users = getFromDB("http://127.0.0.1:5001/get_recommended_user")
    users.then((response) => {
        const recommendedUsers = response.msg;
        console.log(response);
        recommendedUsers.forEach(element => {
            recommendedUsersComponent.innerHTML += `<li> ${element} </li>`
        });
    })
}

//Function to bring recommended movie  from db

async function handleSetRecommendedMovie() {
const recommendedMovieComponent = document.getElementById("recommended-movie");

const movie = getFromDB("http://127.0.0.1:5001/get_recommended_movie")
    movie.then((response) => {
        console.log(response);
        const recommendedMovie = response.msg;
        recommendedMovieComponent.innerText = recommendedMovie;
        handleSetRecommenedUsers()
    })
}

//Function to set the grafic results
function handleSetResults() {
    handleSetRecommendedMovie()
    
}

