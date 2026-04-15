function showSection(id){

document.querySelectorAll("section").forEach(s => {

s.classList.add("hidden")

})

document.getElementById(id).classList.remove("hidden")

}



const input = document.getElementById("terminal-input")
const output = document.getElementById("terminal-output")


input.addEventListener("keydown",function(e){

if(e.key === "Enter"){

const cmd = input.value

output.innerHTML += "<p>> " + cmd + "</p>"

if(cmd === "help"){

output.innerHTML += "<p>comandos: help tools projetos contato</p>"

}

if(cmd === "tools"){

showSection("tools")

}

if(cmd === "projetos"){

showSection("projects")

}

if(cmd === "contato"){

showSection("contact")

}

input.value = ""

}

})



const canvas = document.getElementById("matrix")
const ctx = canvas.getContext("2d")

canvas.height = window.innerHeight
canvas.width = window.innerWidth

const letters = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ"
const matrix = letters.split("")

const fontSize = 14
const columns = canvas.width / fontSize

const drops = []

for(let x = 0; x < columns; x++)
drops[x] = 1

function draw(){

ctx.fillStyle = "rgba(0,0,0,0.05)"
ctx.fillRect(0,0,canvas.width,canvas.height)

ctx.fillStyle = "#ffffff"
ctx.font = fontSize + "px monospace"

for(let i = 0; i < drops.length; i++){

const text = matrix[Math.floor(Math.random()*matrix.length)]

ctx.fillText(text, i*fontSize, drops[i]*fontSize)

if(drops[i]*fontSize > canvas.height && Math.random()>0.975)
drops[i] = 0

drops[i]++

}

}

setInterval(draw,35)