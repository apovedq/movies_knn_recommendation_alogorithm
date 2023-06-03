const nombres = [
  'Andres Poveda',
  'Camilo Munera',
  'Sebastian Mosquera',
  'Juan P Bueno',
  'Natalia Betancout',
  'Alejandro Medina',
  'Andrea Torrente',
  'Samuel Ortiz',
  'Carlos Laverde',
  'Camila Lerma'
];

const actors = [
  {
    name: "Leonardo DiCaprio",
    img: "https://flxt.tmsimg.com/assets/435_v9_bc.jpg"
  },
  {
    name: "Martin Scorsese",
    img: "https://images.ecestaticos.com/6DGfFYebwk8FVQqIVzVrQ6Dd6Wk=/91x5:2068x1488/1200x900/filters:fill(white):format(jpg)/f.elconfidencial.com%2Foriginal%2Ff95%2F0a8%2Fd12%2Ff950a8d126d7b6813dae8b1b7a4d27bd.jpg"
  },
  {
    name: "Johnny Depp",
    img: "https://flxt.tmsimg.com/assets/33623_v9_bd.jpg"
  },
  {
    name: "Tim Burton",
    img: "https://es.web.img2.acsta.net/medias/nmedia/18/35/36/86/19313141.jpg"
  },
  {
    name: "Robert De Niro",
    img: "https://www.biografiasyvidas.com/biografia/n/fotos/niro.jpg"
  },
  {
    name: "Joe Pesci",
    img: "https://m.media-amazon.com/images/M/MV5BMzc3MTcxNDYxNV5BMl5BanBnXkFtZTcwOTI3NjE1Mw@@._V1_.jpg"
  },
  {
    name: "Adam Sandler",
    img: "https://cdn.britannica.com/52/243652-050-FEE0A5E4/Actor-Adam-Sandler-2019.jpg"
  },
  {
    name: "Bob Schneider",
    img: "https://cdn2.estamosrodando.com/biografias/7/4/rod-schneider-318475.jpg"
  },
  {
    name: "Will Ferrell",
    img: "https://images.fandango.com/ImageRenderer/300/0/redesign/static/img/default_poster.png/0/images/masterrepository/performer%20images/211430/WillFerrell-2020.jpg"
  },
  {
    name: "John C. Reilly",
    img: "https://sm.ign.com/ign_jp/cover/j/john-c-rei/john-c-reilly_amr5.jpg"
  }
];

function handleFillDropdown() {
  let namesDropdown = document.getElementById('names_dropdown')
  nombres.forEach((name) => {
      
      namesDropdown.innerHTML += `<option value="${name}">${name} </option>`
    })
}

function handleFillSliders() {
  const slidersContainer = document.getElementById('weights-sliders');
  console.log(slidersContainer)
  actors.forEach((actor) => {
    //Get the name of the actor to identify the value in the slider
    let nameIdentifier = actor.name.substring(0, actor.name.indexOf(" "));

    slidersContainer.innerHTML += `
    <div class="character-value">
                <img class="image-slider" src=${actor.img} alt="">
                <div>
                    <p> ${actor.name}</p>
                    <section>
                        <p> 0 </p>
                        <input  id="${nameIdentifier}" type="range" id="slider-ch" min="0" max="10" value="0" step="1">
                        <p> 10 </p>
                    </section>

                </div>
            </div>
    `
})
}




handleFillDropdown()
handleFillSliders()