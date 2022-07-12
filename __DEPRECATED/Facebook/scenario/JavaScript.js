// https://itchief.ru/javascript/get-elements
// выбор элементов внутри документа с последующим их сохранением в переменную elements
function find_elements_by_css_selector(selector) {
    var elements = document.querySelectorAll(selector);
    return (elements);
}

find_elements_by_css_selector(selector);
