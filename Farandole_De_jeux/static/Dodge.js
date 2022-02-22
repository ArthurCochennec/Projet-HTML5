const scoreDisplay = document.querySelector(".high-score");
const reset = document.querySelector(".reset");
const main_music = document.getElementById("Main_Music");
main_music.volume = 0.2;
const death_sound = document.getElementById("Death_Sound");

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

canvas.width = 1100;
canvas.height = 600;
canvas.x_paddle = canvas.width / 2 - 60 / 2;
canvas.y_paddle = canvas.height / 2 - 20 / 2;

let time = 0;

let rightPressed = false;
let leftPressed = false;
let upPressed = false;
let downPressed = false;

document.addEventListener("keydown", keyDownHandler);
document.addEventListener("keyup", keyUpHandler);

function keyDownHandler(e) {
  if (e.key == "Right" || e.key == "ArrowRight") {
    rightPressed = true;
  } else if (e.key == "Left" || e.key == "ArrowLeft") {
    leftPressed = true;
  }
  else if (e.key == "ArrowUp") {
    upPressed = true;
  }
  else if (e.key == "ArrowDown") {
    downPressed = true;
  }
}

var highScore =  parseInt(localStorage.getItem("highScore"));


scoreDisplay.innerHTML = `High Score: ${highScore}`;

reset.addEventListener("click", () => {
  localStorage.setItem("highScore", "0");
  score = 0;

});


function keyUpHandler(e) {
  if (e.key == "Right" || e.key == "ArrowRight") {
    rightPressed = false;
  } else if (e.key == "Left" || e.key == "ArrowLeft") {
    leftPressed = false;
  }
  else if (e.key == "ArrowUp") {
    upPressed = false;
  }
  else if (e.key == "Left" || e.key == "ArrowDown") {
    downPressed = false;
  }
}

let score = 0;

function drawScore() {
  ctx.font = "16px Arial";
  ctx.fillStyle = "#230c33";
  ctx.fillText("Score: " + score + " " , 8, 20);
}

let speed = 2;


let paddle = {
  height: 20,
  width: 60,
  x: canvas.x_paddle,
  y: canvas.y_paddle,
  x2: 0,
  y2: 0,

  draw: function() {
    this.x2 = this.x + 60 / 2 - this.height / 2;
    this.y2 = this.y + 20 / 2 - this.width / 2;
    ctx.beginPath();
    ctx.rect(this.x , this.y, this.width, this.height);
    ctx.rect(this.x2 , this.y2 , this.height, this.width);
    ctx.fillStyle = "#230c33";
    ctx.fill();
    ctx.closePath();
  }
};

function play() {
  time += 1;
  essai()
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawBalls();
  paddle.draw();
  movePaddle();
  // levelUp();
  drawScore();

  let lose = false;

  for (const ball of balls)
  {
  
    if (ball.status == 1)
    {
      ball.x += ball.dx;
      ball.y += ball.dy;

      if (ball.x + ball.radius > canvas.width || ball.x - ball.radius < 0) {
        score ++;
        ball.dx *= -1;
        ball.dy += Math.ceil(Math.random() -0.5) / 2;
      }

      if (ball.y + ball.radius > canvas.height || ball.y - ball.radius < 0) {
        score ++;
        ball.dy *= -1;
        ball.dx += Math.ceil(Math.random() -0.5) / 2;
      }
    
  
      if (
        
        ((ball.y + ball.radius > paddle.y && ball.y + ball.radius < paddle.y + paddle.height) &&
        (ball.x + ball.radius > paddle.x && ball.x + ball.radius < paddle.x + paddle.width))
        ||
        ((ball.y + ball.radius > paddle.y2 && ball.y + ball.radius < paddle.y2 + paddle.width) &&
        (ball.x + ball.radius > paddle.x2 && ball.x + ball.radius < paddle.x2 + paddle.height))
        ||



        ((ball.y - ball.radius > paddle.y2 && ball.y - ball.radius < paddle.y2 + paddle.width) &&
        (ball.x - ball.radius > paddle.x2 && ball.x - ball.radius < paddle.x2 + paddle.height))
        ||
        ((ball.y - ball.radius > paddle.y2 && ball.y - ball.radius < paddle.y2 + paddle.width) &&
        (ball.x - ball.radius > paddle.x2 && ball.x - ball.radius < paddle.x2 + paddle.height))
        ||


        ((ball.y - ball.radius > paddle.y2 && ball.y - ball.radius < paddle.y2 + paddle.width) &&
        (ball.x + ball.radius > paddle.x2 && ball.x + ball.radius < paddle.x2 + paddle.height))
        ||
        ((ball.y - ball.radius > paddle.y2 && ball.y - ball.radius < paddle.y2 + paddle.width) &&
        (ball.x + ball.radius > paddle.x2 && ball.x + ball.radius < paddle.x2 + paddle.height))
        ||



        ((ball.y + ball.radius > paddle.y2 && ball.y + ball.radius < paddle.y2 + paddle.width) &&
        (ball.x - ball.radius > paddle.x2 && ball.x - ball.radius < paddle.x2 + paddle.height))
        ||
        ((ball.y + ball.radius > paddle.y2 && ball.y + ball.radius < paddle.y2 + paddle.width) &&
        (ball.x - ball.radius > paddle.x2 && ball.x - ball.radius < paddle.x2 + paddle.height))
        
        ){
        score_def = score
        if (score_def > parseInt(localStorage.getItem("highScore"))) {
          localStorage.setItem("highScore", score_def.toString());
          highScore =  parseInt(localStorage.getItem("highScore"));
          scoreDisplay.innerHTML = `High Score: ${highScore}`;
        }
        
        lose = true;
        score = 0;
        ball.dx = speed;
        ball.dy = -speed + 1;
        death_sound.play();
        main_music.currentTime=0;
        // location.reload();
      }

  }
    if (lose)
    {
      paddle.x = canvas.x_paddle;
      paddle.y = canvas.y_paddle;
      score = 0;
      lose = false;
      index_balls = 0;
      generateBalls();
    }

  }

  requestAnimationFrame(play);
}

let gameLevelUp = true;
let speed_paddle = 5;

function movePaddle() {
  if (rightPressed) {
    paddle.x += speed_paddle;
    if (paddle.x + paddle.width > canvas.width) {
      paddle.x = canvas.width - paddle.width;
    }
  } else if (leftPressed) {
    paddle.x -= speed_paddle;
    if (paddle.x < 0) {
      paddle.x = 0;
    }
  }
  else if (downPressed) {
    paddle.y += speed_paddle;
    if (paddle.y> canvas.height - paddle.height / 2 - paddle.width / 2) {
      paddle.y = canvas.height - paddle.height / 2 - paddle.width / 2;
    }
  }
  else if (upPressed) {
    paddle.y -= speed_paddle;
    if (paddle.y < paddle.width / 2 - paddle.height/ 2) {
      paddle.y = paddle.width / 2 - paddle.height/ 2;
    }
  }
}

var index_balls = 0;
var balls = [];
var ballsnumber = 25;

function generateBalls() {
  for (let c = 0; c < ballsnumber; c++) {
      balls[c] = {
        x: 20,
        y: 50 + Math.ceil(Math.random() * (canvas.height-100)),
        dx: speed,
        dy: 0,
        radius: 3 + Math.ceil(Math.random() * 14),
        status: 0
      };
  }
}

function drawBalls() {
  for (var c = 0; c < ballsnumber; c++) {
      if (balls[c].status === 1) {
        ctx.beginPath();
        ctx.fillStyle = "#230c33";
        ctx.arc(balls[c].x, balls[c].y, balls[c].radius, 0, Math.PI * 2, true);
        ctx.fill();
        ctx.closePath(); 
      }
  }
}

function essai() {
  if (time > 150)
  { 
    time = 0;
    if(index_balls < ballsnumber)
    {
      balls[index_balls].status = 1;
      index_balls ++;
    }
  }

}

generateBalls();
play();