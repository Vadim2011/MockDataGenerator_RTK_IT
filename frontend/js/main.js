


// Переключение кнопок меню вкл./выкл. ____________________________

let buttonsMenu = document.querySelectorAll('[data-switch]');

buttonsMenu.forEach(i => {
  i.addEventListener('click', function() {
    const currentStatus = i.getAttribute('data-switch');
    const exampleItem = document.querySelector(`#${i.className}`);

    if (currentStatus === 'off') {
      i.setAttribute('data-switch', 'on');
      exampleItem.style.display = 'block';
    } else {
      i.setAttribute('data-switch', 'off');
      exampleItem.style.display = 'none';
    }
  })
});
//___________________________________________________________________


































