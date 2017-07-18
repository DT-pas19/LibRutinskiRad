from docx import Document, text

if __name__ == "__main__":
    document = Document('data/162117_б-МЕТЛипу11_2017_7.docx')
    first_page_text = []
    for p in document.paragraphs[:50]:
        first_page_text.append(p.text)

    # чтение первой страницы, определение, есть ли титульник
    print()

    'Выполнил'

    list(filter(lambda x: len(x) > 0, first_page_text))  # 17-20 первых


    # перемещение неиспользуемых файлов, преобразование имен файлов, формирование таблиц

