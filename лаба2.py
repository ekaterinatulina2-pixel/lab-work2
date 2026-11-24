from pathlib import Path
from datetime import datetime
from PIL import Image, ImageFilter, UnidentifiedImageError
import stat


# Пути к папкам лабораторной работы
base = Path.home() / "Desktop" / "Lab2_Media"
inp = base / "data" / "input"
out = base / "data" / "output"
logs = base / "logs"
hist = logs / "history.txt"


# Запись информации в журнал
def log(name, filt, status):
    logs.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    s = f"[{now}] Файл: {name} | Фильтр: {filt} | Статус: {status}\n"

    with open(hist, "a", encoding="UTF-8") as f:
        f.write(s)


# Проверка атрибута «Только чтение» в Windows
def only_read(path):
    attr = path.stat().st_file_attributes
    read_only = getattr(stat, "FILE_ATTRIBUTE_READONLY", 1)
    return bool(attr & read_only)


# Фильтр Гаусса
def gauss(img):
    return img.filter(ImageFilter.GaussianBlur(radius=2))


# Гамма-коррекция
def gamma(img, g=0.8):
    # Преобразуем яркость каждого цветового канала по формуле
    # I_out = 255 * (I_in / 255) ** g
    table = [
        round(255 * ((i / 255) ** g))
        for i in range(256)
    ]
    return img.point(table * len(img.getbands()))


# Основная обработка изображения
def obrabotka(img):
    img = gauss(img)
    img = gamma(img, 0.8)
    return img


# Основная часть программы
def main():
    print("Обработка изображений")
    name = input("Введите имя файла: ").strip()

    # Не разрешаем вводить путь к другому файлу
    if not name or Path(name).name != name:
        print("Ошибка: введите только имя файла.")
        return

    path = inp / name

    # Проверяем, существует ли файл
    if not path.is_file():
        print("Ошибка: Файл не найден")
        log(name, "Фильтр Гаусса, гамма-коррекция", "Файл не найден")
        return

    # В Windows «Только чтение» не запрещает чтение.
    # Поэтому проверяем атрибут отдельно, чтобы выполнить условие задания.
    try:
        if only_read(path):
            print(
                f"Ошибка: Нет прав на чтение файла {name}. "
                "Обратитесь к администратору"
            )
            log(name, "Фильтр Гаусса, гамма-коррекция", "Ошибка доступа")
            return

        # Открываем изображение
        with Image.open(path) as source:
            source.load()
            img = source.convert("RGB")

        # Применяем два алгоритма
        result = obrabotka(img)

        # Создаём папку для результата, если её нет
        out.mkdir(parents=True, exist_ok=True)

        # Сохраняем результат
        result.save(out / "result.jpg", format="JPEG", quality=95)

        print("Файл успешно найден.")
        print("Применён фильтр Гаусса.")
        print("Выполнена гамма-коррекция.")
        print("Результат сохранён:", out / "result.jpg")

        log(name, "Фильтр Гаусса, гамма-коррекция", "Успешно")
        print("Информация добавлена в журнал.")

    except PermissionError:
        print(
            f"Ошибка: Нет прав на чтение файла {name}. "
            "Обратитесь к администратору"
        )
        log(name, "Фильтр Гаусса, гамма-коррекция", "Ошибка доступа")

    except UnidentifiedImageError:
        print("Ошибка: файл не является корректным изображением.")
        log(name, "Фильтр Гаусса, гамма-коррекция", "Ошибка формата")

    except OSError as e:
        print("Ошибка при работе с файлом:", e)
        log(name, "Фильтр Гаусса, гамма-коррекция", "Ошибка обработки")


if __name__ == "__main__":
    main()
