// efeito do titulo (todas as paginas)
const titulos = ["You", "are", "not", "alone."];
let i = 0;

setInterval(() => {
  document.title = titulos[i];
  i = (i + 1) % titulos.length;
}, 300);

// SISTEMA DE RESPOSTA (só roda se tiver pergunta)
const pergunta = document.querySelector("h1");

if (pergunta && pergunta.innerText.includes("5+3-2")) {
  
  // cria input escondido
  const input = document.createElement("input");
  input.type = "text";
  input.placeholder = "...";
  
  input.style.background = "black";
  input.style.color = "white";
  input.style.border = "1px solid white";
  input.style.marginTop = "20px";
  input.style.textAlign = "center";

  document.body.appendChild(input);

  input.focus();

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      
      const resposta = input.value.trim();

      if (resposta === "6") {
        window.location.href = "6/";
}
      } else {
        input.value = "";
        input.placeholder = "errado...";
      }

    }
  });
}
