function gettext(mes){

    if (LANG=='en')
        switch (mes){
            case 'Удалить':
                return 'Delete';
            case 'Пожалуйста выберите размер':
                return 'Please, choose size'
            case 'Ключевое слово':
                return 'Keyword'
            case 'Вы можете добавить только фотографии':
                return 'You can add only pictures'
            case 'Максимальный размер файла 2MB':
                return 'Maximum file size 2MB'
            case 'Загрузка завершена!':
                return 'Loading complete'
            case 'Укажите цвет':
                return 'Please choose color'
            case 'Укажите размер':
                return 'Please choose size'
            case 'Укажите тип':
                return 'Please choose type'
            case 'Трекинг код отослан':
                return 'Tracking code submited'
            case 'Ошибка':
                return 'Error'
            case 'Цена':
                return 'Price'
            case 'Доверенный продавец':
                return 'Trustable seller'
            case 'На ваш email была отправлена ссылка для изменения пароля':
                return 'On your email was sent link for password changing'
        }
    return mes;

}
