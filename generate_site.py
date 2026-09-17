# -*- coding: utf-8 -*-
"""Собрать HTML-обучение: сжатые скрины + index.html."""
from __future__ import annotations

import html
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "_screens"
OUT = ROOT / "screens"
ASSETS = ROOT / "assets"
LOGO_SRC = Path(r"C:\Users\User\Desktop\КУРСОРИО\slovar-mihalych\assets\logo.png")
FAV_SRC = Path(r"C:\Users\User\Desktop\КУРСОРИО\slovar-mihalych\assets\favicon.svg")

PREFIXES = ("naming", "single", "mass")

NAMING_HINTS = {
    1: "Тип — что это за товар. Марка — как на упаковке. Модель — заводской индекс. Характеристики — только то, без чего позицию не отличить.",
    2: "Пример: было «КЗВ-180 (180 мм) Кожух защитный вытяжной „ДИОЛД“». Надо: «Кожух защитный вытяжной ДИОЛД КЗВ-180, 180 мм».",
}
SINGLE_HINTS = {
    1: "До входа в 1С соберите: артикул, наименование по формуле, штрихкод, основного поставщика.",
    2: "Путь: 1С → НСИ → «Номенклатура».",
    3: "Зайдите в нужную группу. Новую группу создавайте только если её ещё нет, затем «Создать».",
    4: "Сначала «Показать все». Дальше: штрихкод → рабочее наименование → наименование для печати → артикул → вид «Товар» → основной менеджер (у руководителя) → единица «штуки» → марка/бренд.",
    5: "Вкладка «min – max: помощник закупок». В колонке «Основной поставщик» выберите контрагента, у которого покупаем товар.",
}
MASS_HINTS = {
    1: "Нужен список: счёт, спецификация или таблица. Обязательно три колонки: артикул, наименование, штрихкод.",
    2: "1С → «НСИ и администрирование» → «Номенклатура».",
    3: "Справа иерархия групп. Выберите группу, куда пойдут новые товары, либо готовьтесь создать новую.",
    4: "Если группы нет: в дереве справа ПКМ по разделу → «Создать группу». Лишние папки не плодим.",
    5: "Имя группы — название поставщика, бренда или категории товара.",
    6: "Модуль уже установлен в 1С:Торговля у сотрудников отдела закупа — откройте его из базы, скачивать ничего не нужно.",
    7: "В модуле: «Каталог» — файл со списком; «Группа номенклатуры» — куда создавать; вид — «Товар»; НДС — «20%»; путь к логу не заполняем.",
    8: "Основные параметры: файл со штрихкодами, созданная группа, вид «Товар», НДС всегда 20%, путь к логу пустой.",
    9: "Вкладка «Параметры чтения»: сопоставьте колонки Excel (артикул, наименование, штрихкод) и укажите, с какой по какую строку идут товары. Шапка в диапазон не входит.",
    10: "Вкладка «Статические параметры»: единица измерения — «штуки».",
    11: "Кнопка «Загрузить». Файл Excel со списком должен быть закрыт, иначе модуль не запустится.",
    12: "Смотрите «Всего создано» и вкладку «Не созданные». Если такой артикул уже есть, новую карточку модуль не создаст.",
    13: "Модуль больше не нужен — закройте. Откройте группу номенклатуры, куда легли товары.",
    14: "Клик по любой строке, Ctrl+A, «Изменить выделенное». Найдите «Помощник закупок. Основной поставщик», поставьте галочку и выберите контрагента.",
    15: "Снова Ctrl+A → «Изменить выделенное» → строка «марка/бренд», галочка, выбрать бренд. Если бренда нет — «Создать».",
}

HINTS = {"naming": NAMING_HINTS, "single": SINGLE_HINTS, "mass": MASS_HINTS}

TITLES = {
    "naming": {
        1: "Что должно включать наименование",
        2: "Пример правильного наименования",
    },
    "single": {
        1: "Какие данные нужны",
        2: "Открыть справочник номенклатуры",
        3: "Создать группу (если нужно) и карточку",
        4: "Заполнить карточку товара",
        5: "Основной поставщик на вкладке min–max",
    },
    "mass": {
        1: "Наличие списка товаров",
        2: "Раздел «Номенклатура»",
        3: "Выбрать место для новых товаров",
        4: "Создать группу — только если нужно",
        5: "Задать наименование группы",
        6: "Открыть модуль массовой заливки в 1С",
        7: "Настроить колонки в модуле",
        8: "Загрузка номенклатуры и штрихкода",
        9: "Сопоставить графы с колонками списка",
        10: "Единица измерения — штуки",
        11: "Кнопка «Загрузить»",
        12: "Проверить результаты модуля",
        13: "Закрыть модуль и открыть группу",
        14: "Основной поставщик всем выделенным",
        15: "Проставить марку / бренд",
    },
}


def e(text: str) -> str:
    return html.escape(text, quote=True)


def compress() -> dict[str, list[str]]:
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("quad_*.jpg"):
        old.unlink()
    mapping: dict[str, list[str]] = {p: [] for p in PREFIXES}
    for png in sorted(SRC.glob("*.png")):
        prefix = png.name.split("_")[0]
        if prefix not in mapping:
            continue
        n = len(mapping[prefix]) + 1
        dest = OUT / f"{prefix}_{n:02d}.jpg"
        im = Image.open(png).convert("RGB")
        im.thumbnail((1280, 900))
        im.save(dest, "JPEG", quality=72, optimize=True)
        mapping[prefix].append(dest.name)
        print("jpg", dest.name, dest.stat().st_size)
    # Если исходных PNG нет — оставить уже собранные jpg по префиксам
    for prefix in PREFIXES:
        if mapping[prefix]:
            continue
        mapping[prefix] = [p.name for p in sorted(OUT.glob(f"{prefix}_*.jpg"))]
    return mapping


def steps_html(prefix: str, files: list[str], open_first: int = 0) -> str:
    chunks = []
    titles = TITLES[prefix]
    hints = HINTS[prefix]
    for i, name in enumerate(files, 1):
        opened = " open" if i <= open_first else ""
        title = titles.get(i, f"Шаг {i}")
        hint = hints.get(i, "")
        chunks.append(
            f'''<details class="step"{opened}>
  <summary><span class="sn">{i}.</span> {e(title)}</summary>
  <div class="step-body">
    <p>{hint}</p>
    <img class="shot" src="screens/{e(name)}" alt="{e(title)}" loading="lazy" />
  </div>
</details>'''
        )
    return "\n".join(chunks)


def write_html(mapping: dict[str, list[str]]) -> None:
    naming = steps_html("naming", mapping["naming"], 2)
    single = steps_html("single", mapping["single"], 1)
    mass = steps_html("mass", mapping["mass"], 0)
    page = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Создание карточек номенклатуры — отдел закупа</title>
  <meta name="description" content="Внутренний регламент отдела закупа: наименование, заливка в 1С поштучно и массово." />
  <meta name="robots" content="noindex,nofollow" />
  <meta name="theme-color" content="#4208A8" />
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="glow" aria-hidden="true"></div>
  <header class="top">
    <div class="wrap top-inner">
      <a class="brand" href="/internal/zakup">
        <img src="assets/logo.png" alt="У Михалыча" />
        <span class="brand-tag">Отдел закупа · регламенты</span>
      </a>
      <span class="chip">Обучение</span>
    </div>
  </header>

  <main class="wrap">
    <section class="hero">
      <p class="kicker">Внутренние регламенты · отдел закупа</p>
      <h1>Создание карточек номенклатуры</h1>
      <p class="lead">Выберите тему — раскроется обучение со скриншотами из 1С. Заводим товар в справочник номенклатуры: поштучно или массово.</p>
    </section>

    <nav class="toc" aria-label="Темы обучения">
      <a href="#choose" data-open="choose"><b>01</b><span>Какой путь выбрать</span></a>
      <a href="#naming" data-open="naming"><b>02</b><span>Правильное наименование</span></a>
      <a href="#single" data-open="single"><b>03</b><span>Заливка поштучно в 1С</span></a>
      <a href="#mass" data-open="mass"><b>04</b><span>Массовое заведение в 1С</span></a>
      <a href="#check" data-open="check"><b>05</b><span>Чек-лист готовности</span></a>
    </nav>

    <details class="topic" id="choose">
      <summary>
        <span class="num">01</span>
        <span class="sum-text">Какой путь выбрать<small>Одна позиция или линейка</small></span>
        <span class="chev">▾</span>
      </summary>
      <div class="topic-body">
        <p>Номенклатура живёт в 1С. Сначала проверьте, нет ли товара в базе, затем заводите поштучно или массовым модулем.</p>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Ситуация</th><th>Что открыть</th></tr></thead>
            <tbody>
              <tr><td>Одна позиция или несколько штук</td><td><a href="#single" data-open="single">Тема 03 — поштучно в 1С</a></td></tr>
              <tr><td>Линейка, десятки позиций, есть Excel</td><td><a href="#mass" data-open="mass">Тема 04 — массовая заливка</a></td></tr>
            </tbody>
          </table>
        </div>
        <div class="warn">
          <b>Перед любой заливкой</b>
          Проверьте, нет ли товара в базе (штрихкод, артикул, наименование). Дубль хуже, чем задержка. Наименование сразу пишите по формуле из темы 02. Группу номенклатуры создавайте, только если её реально нет.
        </div>
      </div>
    </details>

    <details class="topic" id="naming">
      <summary>
        <span class="num">02</span>
        <span class="sum-text">Правильное наименование<small>Формула имени товара в 1С</small></span>
        <span class="chev">▾</span>
      </summary>
      <div class="topic-body">
        <p>Наименование — то, по чему коллеги ищут товар в 1С и печатают документы. Одинаково в «Рабочем наименовании» и в «Наименовании для печати».</p>
        <div class="formula">Тип товара + марка / бренд + модель + 1–3 основные характеристики</div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Часть</th><th>Пример</th></tr></thead>
            <tbody>
              <tr><td>Как было</td><td>КЗВ-180 (180 мм) Кожух защитный вытяжной «ДИОЛД»</td></tr>
              <tr><td>Как надо</td><td>Кожух защитный вытяжной ДИОЛД КЗВ-180, 180 мм</td></tr>
              <tr><td>Тип</td><td>Кожух защитный вытяжной</td></tr>
              <tr><td>Марка / бренд</td><td>ДИОЛД</td></tr>
              <tr><td>Модель</td><td>КЗВ-180</td></tr>
              <tr><td>Характеристика</td><td>180 мм</td></tr>
            </tbody>
          </table>
        </div>
        {naming}
      </div>
    </details>

    <details class="topic" id="single">
      <summary>
        <span class="num">03</span>
        <span class="sum-text">Заливка поштучно в 1С<small>Одна карточка руками</small></span>
        <span class="chev">▾</span>
      </summary>
      <div class="topic-body">
        <p>Этот путь — когда позиций мало и каждую карточку заполняете руками. Раскройте шаг — внутри скриншот из 1С.</p>
        <div class="note">
          <b>На руках до входа в 1С</b>
          Артикул · наименование по формуле · штрихкод · основной поставщик.
        </div>
        {single}
        <div class="warn">
          <b>Не закрывайте карточку без поставщика</b>
          Вкладка «min – max: помощник закупок». Без поставщика позиция потом теряется в закупке.
        </div>
      </div>
    </details>

    <details class="topic" id="mass">
      <summary>
        <span class="num">04</span>
        <span class="sum-text">Массовое заведение в 1С<small>Линейка через модуль в базе</small></span>
        <span class="chev">▾</span>
      </summary>
      <div class="topic-body">
        <p>Когда есть готовый список и нужно завести линейку целиком. Раскрывайте шаги по порядку.</p>
        <div class="note">
          <b>Модуль уже в 1С:Торговля</b>
          У сотрудников отдела закупа модуль массовой заливки установлен в базе — открывайте его из 1С, отдельно скачивать не нужно.
        </div>
        {mass}
        <div class="warn">
          <b>Три вещи, без которых модуль ломается</b>
          Файл Excel со списком должен быть закрыт. НДС в модуле всегда 20%, путь к логу пустой. Если артикул уже есть в 1С — карточка не создастся, смотрите вкладку «Не созданные».
        </div>
        <div class="warn">
          <b>После заливки</b>
          Ctrl+A → «Изменить выделенное»: сначала основной поставщик, затем марка/бренд. Нет бренда в списке — «Создать». Проверьте 2–3 карточки: наименование, штрихкод, единица, группа.
        </div>
      </div>
    </details>

    <details class="topic" id="check">
      <summary>
        <span class="num">05</span>
        <span class="sum-text">Чек-лист готовности<small>Карточку можно считать готовой, если всё закрыто</small></span>
        <span class="chev">▾</span>
      </summary>
      <div class="topic-body">
        <div class="table-wrap">
          <table>
            <thead><tr><th>Контур</th><th>Проверить</th></tr></thead>
            <tbody>
              <tr><td>1С, наименование</td><td>Тип + бренд + модель + 1–3 характеристики. Рабочее и для печати совпадают.</td></tr>
              <tr><td>1С, идентификация</td><td>Штрихкод и артикул внесены, единица хранения указана.</td></tr>
              <tr><td>1С, закупка</td><td>Вид номенклатуры = товар, бренд выбран, основной поставщик на вкладке min–max.</td></tr>
              <tr><td>1С, массовая заливка</td><td>Excel закрыт, НДС 20%, вкладка «Не созданные» пустая. Ctrl+A: поставщик, затем бренд.</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </details>
  </main>
  <footer class="wrap foot">Сеть магазинов «У Михалыча» · внутренний регламент отдела закупа · Академия УМ</footer>
  <script src="app.js"></script>
</body>
</html>
'''
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    print("wrote index.html")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    if LOGO_SRC.exists():
        shutil.copy2(LOGO_SRC, ASSETS / "logo.png")
    if FAV_SRC.exists():
        shutil.copy2(FAV_SRC, ASSETS / "favicon.svg")
    mapping = compress()
    for k, v in mapping.items():
        print(k, len(v))
    write_html(mapping)


if __name__ == "__main__":
    main()
