/**
 * main.js - JavaScript для интернет-магазина SeeYouInside
 * Дипломный проект Некит Карины Руслановны
 */

// Ждем загрузки DOM
document.addEventListener('DOMContentLoaded', function () {

    // ============================================================
    // ФУНКЦИЯ ПОЛУЧЕНИЯ CSRF ТОКЕНА
    // ============================================================
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    // ============================================================
    // ДОБАВЛЕНИЕ ТОВАРА В КОРЗИНУ (AJAX)
    // ============================================================
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');

    addToCartForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = new FormData(this);
            const url = this.action;
            const button = this.querySelector('button[type="submit"]');
            const originalText = button.innerHTML;

            // Показываем загрузку
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Добавление...';

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Показываем уведомление
                        showToast(data.message, 'success');

                        // Обновляем счетчик корзины
                        updateCartCount(data.cart_count);

                        // Возвращаем кнопку
                        button.disabled = false;
                        button.innerHTML = '<i class="fas fa-check"></i> Добавлено';

                        setTimeout(() => {
                            button.innerHTML = originalText;
                        }, 2000);
                    } else {
                        showToast(data.error || 'Ошибка при добавлении', 'error');
                        button.disabled = false;
                        button.innerHTML = originalText;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showToast('Произошла ошибка', 'error');
                    button.disabled = false;
                    button.innerHTML = originalText;
                });
        });
    });

    // ============================================================
    // ОБНОВЛЕНИЕ КОЛИЧЕСТВА В КОРЗИНЕ (AJAX)
    // ============================================================
    const quantityInputs = document.querySelectorAll('.cart-quantity-input');

    quantityInputs.forEach(input => {
        input.addEventListener('change', function () {
            const itemId = this.dataset.itemId;
            const quantity = this.value;

            updateCartItem(itemId, 'set', quantity);
        });
    });

    const quantityButtons = document.querySelectorAll('.quantity-btn');

    quantityButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const itemId = this.dataset.itemId;
            const action = this.dataset.action;

            updateCartItem(itemId, action);
        });
    });

    function updateCartItem(itemId, action, quantity = null) {
        const formData = new FormData();
        formData.append('action', action);
        if (quantity) {
            formData.append('quantity', quantity);
        }

        fetch(`/cart/update/${itemId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Обновляем отображение
                    if (data.item_quantity === 0) {
                        // Товар удален - перезагружаем страницу
                        location.reload();
                    } else {
                        // Обновляем количество
                        const quantityElement = document.querySelector(`#quantity-${itemId}`);
                        if (quantityElement) {
                            quantityElement.textContent = data.item_quantity;
                        }

                        // Обновляем сумму позиции
                        const itemTotalElement = document.querySelector(`#item-total-${itemId}`);
                        if (itemTotalElement) {
                            itemTotalElement.textContent = data.item_total + ' ₽';
                        }

                        // Обновляем общую сумму
                        const cartTotalElement = document.querySelector('#cart-total');
                        if (cartTotalElement) {
                            cartTotalElement.textContent = data.cart_total + ' ₽';
                        }

                        // Обновляем счетчик
                        updateCartCount(data.cart_count);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Ошибка при обновлении корзины', 'error');
            });
    }

    // ============================================================
    // УДАЛЕНИЕ ИЗ КОРЗИНЫ
    // ============================================================
    const removeButtons = document.querySelectorAll('.remove-from-cart');

    removeButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();

            if (confirm('Удалить товар из корзины?')) {
                const url = this.href;

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken
                    }
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            location.reload();
                        }
                    });
            }
        });
    });

    // ============================================================
    // ОБНОВЛЕНИЕ СЧЕТЧИКА КОРЗИНЫ
    // ============================================================
    function updateCartCount(count) {
        const badge = document.getElementById('cart-count-badge');
        if (badge) {
            badge.textContent = count;
            if (count > 0) {
                badge.style.display = 'inline-block';
            } else {
                badge.style.display = 'none';
            }
        }
    }

    // ============================================================
    // УВЕДОМЛЕНИЯ (TOAST)
    // ============================================================
    function showToast(message, type = 'info') {
        // Создаем контейнер для уведомлений, если его нет
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container position-fixed top-0 end-0 p-3';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
        }

        // Создаем уведомление
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');

        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${type === 'success' ? '<i class="fas fa-check-circle me-2"></i>' : ''}
                    ${type === 'error' ? '<i class="fas fa-exclamation-circle me-2"></i>' : ''}
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        container.appendChild(toast);

        // Инициализируем Bootstrap Toast
        const bsToast = new bootstrap.Toast(toast, {
            animation: true,
            autohide: true,
            delay: 3000
        });

        bsToast.show();

        // Удаляем после скрытия
        toast.addEventListener('hidden.bs.toast', function () {
            toast.remove();
        });
    }

    // ============================================================
    // БЫСТРЫЙ ПРОСМОТР ТОВАРА
    // ============================================================
    const quickViewButtons = document.querySelectorAll('.quick-view-btn');

    quickViewButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();

            const productId = this.dataset.productId;
            const modal = new bootstrap.Modal(document.getElementById('quickViewModal'));

            fetch(`/quick-view/${productId}/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.querySelector('#quickViewModal .modal-body').innerHTML = data.html;
                        modal.show();
                    }
                });
        });
    });

    // ============================================================
    // ФИЛЬТРАЦИЯ В КАТАЛОГЕ
    // ============================================================
    const filterForm = document.getElementById('filter-form');

    if (filterForm) {
        const filterInputs = filterForm.querySelectorAll('input, select');

        filterInputs.forEach(input => {
            input.addEventListener('change', function () {
                filterForm.submit();
            });
        });
    }

    // ============================================================
    // ВАЛИДАЦИЯ ФОРМ
    // ============================================================
    const checkoutForm = document.getElementById('checkout-form');

    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function (e) {
            const phone = document.getElementById('phone');
            const email = document.getElementById('email');

            let isValid = true;

            // Проверка телефона
            if (phone && !phone.value.match(/^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/)) {
                showToast('Введите корректный номер телефона', 'error');
                isValid = false;
            }

            // Проверка email
            if (email && !email.value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
                showToast('Введите корректный email', 'error');
                isValid = false;
            }

            if (!isValid) {
                e.preventDefault();
            }
        });
    }

    // ============================================================
    // ГАЛЕРЕЯ ИЗОБРАЖЕНИЙ ТОВАРА
    // ============================================================
    const thumbnails = document.querySelectorAll('.product-thumbnail');
    const mainImage = document.getElementById('main-product-image');

    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', function () {
            const imageUrl = this.dataset.imageUrl;
            if (mainImage && imageUrl) {
                mainImage.src = imageUrl;

                // Обновляем активный класс
                thumbnails.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });

    // ============================================================
    // ПОИСКОВЫЕ ПОДСКАЗКИ
    // ============================================================
    const searchInput = document.querySelector('input[name="q"]');

    if (searchInput) {
        let timeout = null;

        searchInput.addEventListener('input', function () {
            clearTimeout(timeout);

            const query = this.value.trim();

            if (query.length >= 2) {
                timeout = setTimeout(() => {
                    fetch(`/api/search-suggestions/?q=${encodeURIComponent(query)}`)
                        .then(response => response.json())
                        .then(data => {
                            // Здесь можно реализовать отображение подсказок
                            console.log('Suggestions:', data.suggestions);
                        });
                }, 300);
            }
        });
    }

    // ============================================================
    // ИНИЦИАЛИЗАЦИЯ
    // ============================================================
    console.log('SeeYouInside - интернет-магазин запущен');

    // Получаем актуальное количество товаров в корзине
    fetch('/api/header-info/')
        .then(response => response.json())
        .then(data => {
            updateCartCount(data.cart_count);
        })
        .catch(error => {
            console.error('Error fetching cart info:', error);
        });
});