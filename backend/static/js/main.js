


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

async function downloadFile(params) {
  try {
    const response = await fetch('/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // 'Authorization': 'Bearer token' // если нужно
      },
      body: JSON.stringify(params)
    });

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    // Получаем имя файла из заголовка Content-Disposition
    const contentDisposition = response.headers.get('Content-Disposition');
    let filename = 'file';
    if (contentDisposition) {
      const match = contentDisposition.match(/filename\*?=(?:UTF-8'')?["']?([^;"']+)/i);
      if (match) filename = decodeURIComponent(match[1]);
    }

    // Получаем файл как Blob
    const blob = await response.blob();

    // Создаём ссылку и инициируем скачивание
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();

    // Убираем за собой
    link.remove();
    window.URL.revokeObjectURL(downloadUrl);

    return blob;
  } catch (error) {
    console.error('Ошибка скачивания файла:', error);
    throw error;
  }
}

    // Function send params to function download____________
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

  downloadFile(params)

}


let buttonGetFile = document.querySelector('.get-data__file');
let buttonGetHystory = document.querySelector('.get-data__history');

buttonGetFile.addEventListener('click', getFileData);

//___________________________________________________________________






























