### Общее описание:

Фидж - голосовой ассистент. Есть база ссылок на статьи, которые человек прочитал и считает интересными. Фидж необходим, чтобы эффективно ссылаться на источники во время беседы/презентации. На основании голосового диалога производится поиск по базе и предлагается наиболее релевантный вариант.

На данном этапе Фидж работает с заранее прописанными текстовыми запросами, которые хранятся в queries.json или с текстовыми запросами поступающими от пользователя через приложение.
Для поиска используются модели тематического поиска: lda, lsi и word2vec.
Для работы моделей производится преобразование статей и запросов в нужный вид.

Пользователь выбирает модель, название модели передается для поиска. Если модель ещё не была обучена и, соответственно, сохранена, происходит обучение модели и ее сохранение на диск. В ином случае, происходит считывание модели и запросов, обработка запросов и получение результата работы моделей для каждого запроса.

### Реализованный функционал:

Считывание ссылок для загрузки статей из файла urls.json.
***
Скачивание html страниц по ссылкам.
***
Выделение текста со страниц.
***
Чистка текста от пунктуации, табуляции, стопслов, приведение текста к нижнему регистру, лемматизация.
***
Сохранение текстов статей в виде списка нормализованных слов.
***
Для английских статей производится перевод текста. Определение языка статьи реализовано двумя способами:
1) Язык заранее указан в файле urls.json;
2) Использованы библиотеки для определения языка.
***
В случае добавления новых ссылок в urls.json производится дозакачка по новым ссылкам, которая подразумевает этапы:
- фильтрация новых ссылок;
- скачивание статей по новым ссылкам; 
- предобработка текста;
- добавление новых статей к старым;
- сохранение.
***
В случае неудачной загрузки статьи по ссылке (не получена страница/не удалось выделить текст) ссылка игнорируется и при последующем запуске программы будет попытка повторной загрузки.
Причина неудачной загрузки выводится в консоль.
***
Сохранение обработанных статей в структуру PhyArticle и на диск в articles.json, содержащие поля:
- url - ссылка по которой загружена статья;
- title - название статьи;
- text - текст статьи;
- language - язык статьи;
- normalized_words - список нормализованных слов.
***
Составление корпуса и словаря для моделей из normalized_words (методами gensim).
***
Запросы хранятся в queries.json с полями:

- id - идентификационный номер запроса;
- url - ссылка статьи по которой сформирован запрос;
- title - название статьи;
- text - текст запроса (подразумевается копипаст);
- summary - текст запроса (подразумевается краткая выжимка/пересказ человека).

Тексты запросов также подвергаются предобработке, как и тексты статей.
***
Поиск статьи по запросу (необходимо передать корпус и подготовленный запрос; также в качестве аргумента можно указать число наиболее релевантных статей для вывода.)
***

Запись результатов поиска в answers.json с информацией:

- answer_time - время поиска статьи;
- model_name - название модели;
- answer_articles - информация по найденной статье;
- query - текст запроса.

В свою очередь answer_articles содержит:

- id - идентификационный номер статьи;
- title - заголовок статьи;
- url - ссылка на статью;
- text - первые строки статьи;
- similarity - мера сходства с запросом.

***
Также реализован фунционал работы:   
- со статьями представленными в формате pdf (в репозитории имеется скрипт, который парсит pdf файлы и представляет их в необходимом виде - нашему сервису).    
- с книгами издательства МИФ. Написан скраппер, который собирает описание книг с официального сайта издательства и представляет данные в необходимом для Phyge виде.  
  - tema - хештеги книги
  - title - название
  - source - ссылка
  - description - краткое описание
  - stikers - текст на стикерах
  - about_book - о книге
  - excerption - цитаты из книги
  - type = 'book'- тип данных  
Можно доскраппить данные:   
  - help_book - кому может помочь эта книга
  - for_who - для кого книга
  - about_author - об авторе

***
Обработанные статьи/книги добавляются в mongoBD
