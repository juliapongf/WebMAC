if (!localStorage.getItem('cor')) {
    localStorage.setItem('cor', 'rgb(234, 0, 179)');
}


function mudar_cor() {
    if (!localStorage.getItem('cor')) {
        localStorage.setItem('cor', 'rgb(234, 0, 179)');
    }
    let cor = localStorage.getItem('cor');
    document.querySelectorAll('.mutavel').forEach(item => {
        item.style.backgroundColor = cor;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    mudar_cor();
    document.querySelectorAll('.button-settings').forEach(botao => {
        botao.onclick = () => {
            localStorage.setItem('cor', botao.dataset.cor);
            document.querySelectorAll('.mutavel').forEach(item => {
                item.style.backgroundColor = botao.dataset.cor;
            });
        };
    });
});

document.addEventListener('htmx:afterSwap', () => {
    mudar_cor();
})
