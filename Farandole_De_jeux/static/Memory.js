let cardArray = [ 
{ name: "youtube", img: "static/Pictures/Memory/logoyotube.jpg", },
{ name: "youtube", img: "static/Pictures/Memory/logoyotube.jpg", },
{ name: "facebook", img: "static/Pictures/Memory/logofacebook.jpg", },
{ name: "facebook", img: "static/Pictures/Memory/logofacebook.jpg", },
{ name: "insta", img: "static/Pictures/Memory/logoinsta.jpg", },
{ name: "insta", img: "static/Pictures/Memory/logoinsta.jpg", },
{ name: "chrome", img: "static/Pictures/Memory/logochrome.jpg", },
{ name: "chrome", img: "static/Pictures/Memory/logochrome.jpg", },
{ name: "g+", img: "static/Pictures/Memory/logog+.jpg", },
{ name: "g+", img: "static/Pictures/Memory/logog+.jpg", },
{ name: "twitch", img: "static/Pictures/Memory/logotwitch.jpg", },
{ name: "twitch", img: "static/Pictures/Memory/logotwitch.jpg", },
]; 

//define variables and get DOM element

let grid = document.querySelector(".grid"); 
let scoreBoard = document.querySelector(".scoreBoard"); 
let popup = document.querySelector(".popup"); 
let playAgain = document.querySelector(".playAgain"); 
let clickBoard = document.querySelector(".clickBoard"); 
let imgs; 
let cardsId = []; 
let cardsSelected = []; 
let cardsWon = 0; 
let clicks = 0;// JavaScript source code

document.addEventListener("DOMContentLoaded", function () {
//define functions 

createBoard(grid, cardArray); 
arrangeCard();
playAgain.addEventListener("click", replay); 

//add a click function for images 

imgs = document.querySelectorAll("img");
Array.from(imgs).forEach(img => 
img.addEventListener("click", flipCard)
) 
});
//createBoard function


function createBoard(grid, array) { 
    popup.style.display = "none";
    array.forEach((arr, index) => {
        let img = document.createElement("img");
        img.setAttribute("src", "static/Pictures/Memory/blank.png");
        img.setAttribute("data-id", index);
        grid.appendChild(img);
    })
}

// arrangeCard function

function arrangeCard() { 
    cardArray.sort(() => 0.5 - Math.random())
}

// flip Card function

function flipCard() { 
    let selected = this.dataset.id;
      let clicked =cardArray[selected].name
    cardsSelected.push(clicked);




    cardsId.push(selected);
    this.classList.add("flip");
    this.setAttribute("src", cardArray[selected].img);
    if (cardsId.length === 2) {
        setTimeout(checkForMatch, 500);
    }
}
// checkForMatch function

function checkForMatch() { 
    let imgs = document.querySelectorAll("img");
    let firstCard = cardsId[0];
    let secondCard = cardsId[1];
    if (cardsSelected[0] === cardsSelected[1] && firstCard !== secondCard) {
        alert("you have found a match");
        cardsWon += 1;
        scoreBoard.innerHTML = cardsWon;
        setTimeout(checkWon,500)
    } else {
        imgs[firstCard].setAttribute("src", "static/Pictures/Memory/blank.png");
        imgs[secondCard].setAttribute("src", "static/Pictures/Memory/blank.png"); alert("wrong, please try again"); imgs[firstCard].classList.remove("flip"); imgs[secondCard].classList.remove("flip");
    }
    cardsSelected = [];
    cardsId = [];
    clicks += 1;
    clickBoard.innerHTML = clicks;
}

function checkWon() {
    if (cardsWon == cardArray.length / 2) {
        alert("You won")
        setTimeout(()=> popup.style.display = "flex" ,300);
    }
}
// The replay function

function replay() { 
    arrangeCard();
    grid.innerHTML = "";
    createBoard(grid, cardArray);
    cardsWon = 0;
    clicks = 0;
    clickBoard.innerHTML = 0;
    scoreBoard.innerHTML = 0;
    popup.style.display = "none";
}
