


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


// Получение данных от сервера ______________________________________
    // Function fetch method POST____________
async function sendData(params) {
  try {
    const response = await fetch('/', {
      method: 'POST', // Указываем метод
      headers: {
        'Content-Type': 'application/json;charset=utf-8' // Заголовки
      },
      body: JSON.stringify(params)
    });

    if (!response.ok) {
      throw new Error(`Ошибка HTTP: ${response.status}`);
    }

    const result = await response.json(); // Читаем ответ сервера в формате JSON
    console.log('Ответ сервера:', 'result');
  } catch (error) {
    console.error('Ошибка при отправке:', error);
  }
}

function getFileData() {
  
  const params = {
    ligin: document.querySelector('.login-input').value,
    surname: document.querySelector('.surname').dataset.switch,
    first_name: document.querySelector('.first-name').dataset.switch,
    patronymic: document.querySelector('.patronymic').dataset.switch,
    email: {
      email: document.querySelector('.email').dataset.switch,
      email_method: document.querySelector('input[name="email"]:checked').value,
    },
    phone: {
      phone: document.querySelector('.phone').dataset.switch,
      phone_method: document.querySelector('input[name="phone"]:checked').value,
    }, 
    address: {
      address:document.querySelector('.address').dataset.switch,
      address_city: document.querySelector('input[name="city"]').checked,
      address_street:  document.querySelector('input[name="street"]').checked,
      address_house:  document.querySelector('input[name="house"]').checked,
      address_apartment: document.querySelector('input[name="apartment"]').checked,
    },  
    count_item: document.querySelector('input[name="count-row"]').value,
    format_data: document.querySelector('input[name="format"]:checked').value,
  }

  // sendData(params)


  console.log(params);

}


let buttonGetFile = document.querySelector('.get-data__file');
let buttonGetHystory = document.querySelector('.get-data__history');

buttonGetFile.addEventListener('click', getFileData);

// fetch('путь/к/файлу.json')
//   .then(response => {
//     // Проверяем статус ответа (успех или ошибка)
//     if (!response.ok) {
//       throw new Error(`HTTP error! Status: ${response.status}`);
//     }
//     // Распарсиваем тело ответа как JSON
//     return response.json();
//   })
//   .then(data => {
//     console.log(data); // Готово! Данные в формате JavaScript
//   })
//   .catch(error => {
//     console.error('Ошибка:', error); // Обработка ошибок
//   });




//<input type="text" name="login" id="login" value="test_user"></input>

// Сервер
//  Content-Type: text/csv; charset=utf-8
// Content-Disposition: attachment; filename="data.csv"

/* 
"count-item"
'login-inpu'

"surname" data-switch="on"
"first-name" data-switch="on"
"patronymic" data-switch="on"
"email" data-switch="on"
"phone" data-switch="on"
"address" data-switch="on"
*/

/*
type="radio" name="email" value="email-gen" checked
type="radio" name="email" value="email-db"
type="radio" name="email" value="email-name"

type="radio" name="phone" value="phone-gen" checked
type="radio" name="phone" value="phone-db"

type="checkbox" name="city" value="city" checked
type="checkbox" name="street" value="street" checked
type="checkbox" name="home" value="home" checked
type="checkbox" name="aparment" value="aparment" checked
*/

/*
type="radio" name="format" value="csv" checked>
type="radio" name="format" value="json">
*/

//___________________________________________________________________






























