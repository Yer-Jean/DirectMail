document.addEventListener('DOMContentLoaded', function () {
    // Получите поле 'periodic'
    const periodicField = document.getElementById('id_periodic');
    // Получите поля, которые нужно скрыть/показать
    const endDayField = document.getElementById('endDayField');
    const dayOfWeekField = document.getElementById('dayOfWeekField');
    const dayOfMonthField = document.getElementById('dayOfMonthField');

    // Обработчик события изменения значения поля 'periodic'
    periodicField.addEventListener('change', function () {
        // Скрываем все поля
        hideFieldAndLabel(endDayField);
        hideFieldAndLabel(dayOfWeekField);
        hideFieldAndLabel(dayOfMonthField);
        // endDayField.classList.add('hidden-field');
        // dayOfWeekField.classList.add('hidden-field');
        // dayOfMonthField.classList.add('hidden-field');

        // В зависимости от выбранного значения 'periodic', покажите соответствующее поле
        if (periodicField.value === 'd') {
            showFieldAndLabel(endDayField);
        } else if (periodicField.value === 'w') {
            showFieldAndLabel(endDayField);
            showFieldAndLabel(dayOfWeekField);
        } else if (periodicField.value === 'm') {
            showFieldAndLabel(endDayField);
            showFieldAndLabel(dayOfMonthField);
        }
        // if (periodicField.value === 'd') {
        //     endDayField.classList.remove('hidden-field');
        // } else if (periodicField.value === 'm') {
        //     dayOfMonthField.classList.remove('hidden-field');
        // } else if (periodicField.value === 'w') {
        //     dayOfWeekField.classList.remove('hidden-field');
        // }
    });

    // Инициализация, чтобы правильно показать/скрыть поля при загрузке страницы
    periodicField.dispatchEvent(new Event('change'));

    // Функция для скрытия поля и его описания
    function hideFieldAndLabel(fieldContainer) {
        fieldContainer.classList.add('hidden-field');
    }

    // Функция для отображения поля и его описания
    function showFieldAndLabel(fieldContainer) {
        fieldContainer.classList.remove('hidden-field');
    }
});
