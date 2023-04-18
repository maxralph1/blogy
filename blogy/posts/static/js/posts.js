const btnClose = document.getElementById('btn-close')

btnClose.addEventListener('click', (e) => {
    preventDefault(e);
    btnClose.classList.add('d-none')
})

console.log('hello')