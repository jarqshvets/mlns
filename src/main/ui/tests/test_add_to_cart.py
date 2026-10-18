from playwright.sync_api import expect


def test_add_to_cart(auth_page):

    # Добавляем товар в корзину
    product_card = auth_page.locator(".inventory_item", has_text="Sauce Labs Bike Light")
    add_button = product_card.locator("button")  # кнопка Add to cart внутри карточки

    # Кликаем
    add_button.click()

    # Проверяем, что кнопка изменилась на Remove
    expect(add_button).to_have_text("Remove")

    # Проверяем счётчик корзины
    expect(auth_page.locator(".shopping_cart_badge")).to_have_text("1")

def test_add_to_cart_2(auth_page):

    # Добавляем товар в корзину
    product_card = auth_page.locator(".inventory_item", has_text="Sauce Labs Onesie")
    add_button = product_card.locator("button")  # кнопка Add to cart внутри карточки

    # Кликаем
    add_button.click()

    # Проверяем, что кнопка изменилась на Remove
    expect(add_button).to_have_text("Remove")

    # Проверяем счётчик корзины
    expect(auth_page.locator(".shopping_cart_badge")).to_have_text("1")
