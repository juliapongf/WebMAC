/**************************************************************************************************
 * 
 * Script para mudar a cor de todos os elementos mutávels do site com a cor escolhida pelo usuário
 * 
 * ************************************************************************************************/


// Buscando caso haja uma cor já escolhida, e colocando como padrão rosa caso não tenha nenhuma escolhida
if (!localStorage.getItem('cor')) {
    localStorage.setItem('cor', 'rgb(234, 0, 179)');
}

// Função que muda a cor de todos os elementos mutáveis
function mudar_cor() {
    if (!localStorage.getItem('cor')) {
        localStorage.setItem('cor', 'rgb(234, 0, 179)');
    }
    let cor = localStorage.getItem('cor');
    document.querySelectorAll('.mutavel').forEach(item => {
        item.style.backgroundColor = cor;
    });
}

// Mudando a cor de todos os elementos mutáveis ao carregar a página
document.addEventListener('DOMContentLoaded', () => {
    mudar_cor();
    document.querySelectorAll('.button-settings').forEach(botao => {
        botao.onclick = () => {
            localStorage.setItem('cor', botao.dataset.cor);
            mudar_cor();
        };
    });
});

// Mudando a cor de todos os elementos mutáveis após fazer um swap HTMX
document.addEventListener('htmx:afterSwap', () => {
    mudar_cor();
})


