import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


def test_purchase():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        try:
            logging.info("Открытие браузера и переход на сайт")
            page = browser.new_page()
            page.goto("https://www.saucedemo.com")

            logging.info("Процесс авторизации")
            page.fill('input[name="user-name"]', 'standard_user')
            page.fill('input[name="password"]', 'secret_sauce')
            page.click('input[type="submit"]')
            page.wait_for_selector('div.inventory_list')
            logging.info("Авторизация успешна")

            logging.info("Выбор товара и добавление в корзину")
            backpack_text = 'Sauce Labs Backpack'
            page.click(f'text={backpack_text}')
            page.click('text=ADD TO CART')

            logging.info("Переход в корзину")
            page.click('a.shopping_cart_link')
            assert page.is_visible('div.inventory_item_name >> text='
                                   f'{backpack_text}'), (
                f"Товар '{backpack_text}' не был добавлен в корзину")
            logging.info("Товар успешно добавлен в корзину")

            logging.info("Оформление покупки")
            page.click('#checkout')
            page.fill('input[name="firstName"]', 'foo')
            page.fill('input[name="lastName"]', 'bar')
            page.fill('input[name="postalCode"]', '12345')
            page.click('#continue')
            page.click('#finish')

            logging.info("Проверка успешного завершения покупки")
            assert page.is_visible('h2[data-test="complete-header"]'), (
                "Заголовок 'Thank you for your order!' не найден")
            actual_header = page.inner_text('h2[data-test="complete-header"]')
            assert actual_header == "Thank you for your order!", (
                f"Текст заголовка не совпадает. Ожидалось: 'Thank you for your"
                f" order!', Получено: '{actual_header}'")
            logging.info("Заголовок 'Thank you for your order!' успешно"
                         " проверен")

            logging.info("Проверка текста с информацией о доставке")
            assert page.is_visible('div[data-test="complete-text"]')
            actual_text = page.inner_text('div[data-test="complete-text"]')
            expected_text = (
                "Your order has been dispatched, and will arrive just as fast"
                " as the pony can get there!")
            assert actual_text == expected_text, (
                f"Текст о доставке не совпадает. Ожидалось: '{expected_text}'"
                f", Получено: '{actual_text}'")
            logging.info("Текст с информацией о доставке успешно проверен")

        except Exception as e:
            logging.error(f"Ошибка во время выполнения теста: {e}")
            raise
        finally:
            logging.info("Закрытие браузера")
            browser.close()


class TestPurchase:
    def __init__(self):
        self.browser = None
        self.page = None

    def setup(self):
        """Настройка тестовой среды"""
        logging.info("Запуск браузера")
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        logging.info("Браузер и страница запущены")

    def teardown(self):
        """Очистка после теста"""
        if self.browser:
            logging.info("Закрытие браузера")
            self.browser.close()

    def test_purchase(self):
        """Основной тест"""
        self.setup()

        try:
            logging.info("Переход на сайт")
            self.page.goto("https://www.saucedemo.com")

            logging.info("Авторизация")
            self.page.fill('input[name="user-name"]', 'standard_user')
            self.page.fill('input[name="password"]', 'secret_sauce')
            self.page.click('input[type="submit"]')
            self.page.wait_for_selector('div.inventory_list')
            logging.info("Авторизация успешна")

            logging.info("Выбор товара и добавление в корзину")
            backpack_text = 'Sauce Labs Backpack'
            self.page.click(f'text={backpack_text}')
            self.page.click('text=ADD TO CART')

            logging.info("Переход в корзину")
            self.page.click('a.shopping_cart_link')

            assert self.page.is_visible(f'div.inventory_item_name >> '
                                        f'text={backpack_text}')
            logging.info("Товар успешно добавлен в корзину")

            logging.info("Оформление покупки")
            self.page.click('#checkout')
            self.page.fill('input[name="firstName"]', 'foo')
            self.page.fill('input[name="lastName"]', 'bar')
            self.page.fill('input[name="postalCode"]', '12345')
            self.page.click('#continue')
            self.page.click('#finish')

            logging.info("Проверка успешного завершения покупки")
            assert self.page.is_visible('h2[data-test="complete-header"]')
            actual_header = self.page.inner_text('h2[data-test="complete-'
                                                 'header"]')
            assert actual_header == "Thank you for your order!", (
                f"Текст заголовка не совпадает. Ожидалось: 'Thank you for your"
                f" order!', Получено: '{actual_header}'")
            logging.info("Заголовок 'Thank you for your order!' успешно "
                         "проверен")

            logging.info("Проверка текста с информацией о доставке")
            assert self.page.is_visible('div[data-test="complete-text"]')
            actual_text = self.page.inner_text(
                'div[data-test="complete-text"]'
            )
            expected_text = (
                "Your order has been dispatched, and will arrive just as fast"
                " as the pony can get there!")
            assert actual_text == expected_text, (
                f"Текст о доставке не совпадает. Ожидалось: '{expected_text}'"
                f", Получено: '{actual_text}'")
            logging.info("Текст с информацией о доставке успешно проверен")

        except Exception as e:
            logging.error(f"Ошибка во время выполнения теста: {e}")
            raise
        finally:
            self.teardown()


if __name__ == "__main__":
    # test = TestPurchase()
    # test.test_purchase()
    test_purchase()
