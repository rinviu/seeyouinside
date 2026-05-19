/**
 * main.js - JavaScript для интернет-магазина SeeYouInside
 * Дипломный проект Некит Карины Руслановны
 */

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
                    if (data.item_quantity === 0) {
                        location.reload();
                    } else {
                        const quantityElement = document.querySelector(`#quantity-${itemId}`);
                        if (quantityElement) {
                            quantityElement.textContent = data.item_quantity;
                        }

                        const itemTotalElement = document.querySelector(`#item-total-${itemId}`);
                        if (itemTotalElement) {
                            itemTotalElement.textContent = data.item_total + ' ₽';
                        }

                        const cartTotalElement = document.querySelector('#cart-total');
                        if (cartTotalElement) {
                            cartTotalElement.textContent = data.cart_total + ' ₽';
                        }

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
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container position-fixed top-0 end-0 p-3';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : 'success'} border-0`;
        toast.setAttribute('role', 'alert');

        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        container.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast, { animation: true, autohide: true, delay: 3000 });
        bsToast.show();
        toast.addEventListener('hidden.bs.toast', () => toast.remove());
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

            if (phone && !phone.value.match(/^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/)) {
                showToast('Введите корректный номер телефона', 'error');
                isValid = false;
            }

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
                            console.log('Suggestions:', data.suggestions);
                        });
                }, 300);
            }
        });
    }

    // ============================================================
    // ОБНОВЛЕНИЕ ИНФОРМАЦИИ О КОРЗИНЕ
    // ============================================================
    function updateCartInfo() {
        fetch('/api/header-info/')
            .then(response => response.json())
            .then(data => {
                const cartCount = document.getElementById('cart-count-badge');
                if (cartCount) cartCount.textContent = data.cart_count || 0;
                const wishlistCount = document.getElementById('wishlist-count-badge');
                if (wishlistCount) wishlistCount.textContent = data.wishlist_count || 0;
            })
            .catch(error => console.error('Error fetching cart info:', error));
    }

    // ============================================================
    // ИНИЦИАЛИЗАЦИЯ
    // ============================================================
    console.log('SeeYouInside - интернет-магазин запущен');
    updateCartInfo();
});