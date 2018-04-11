# Утилиты сбора данных с 2ch.hk
## Установка
```bash
git clone https://github.com/saber-nyan/harkach2data.git && cd harkach2data
virtualenv3 ./venv
source ./venv/bin/activate
pip install ./
```
## Использование
### harkach_dataset
Сохраняет все посты из всех тредов на указанных досках в `pickle`-файл.<br/>
Внутри файла лежит массив строк, каждый элемент — текст поста.
```bash
python -m harkach_dataset [необходимые доски через пробел]
```
Пример:
```bash
$ python -m harkach_dataset b s
*some debug output...*
$ du -h ./posts.pkl
1,9M    ./posts.pkl
```
### harkach_normalize
Удаляет из постов весь HTML, заменяет HTML-escape на оригинальные символы,
исключает некоторы посты, не несущие смысловой нагрузки.

Сохраняет результаты в `output_data.txt`, где каждый пост отделен от других
пустой строкой.
```bash
python -m harkach_normalize [путь до pickle-файла]
```
Пример:
```bash
$ python -c 'print("\n".join(__import__("pickle").load(open("./posts.pkl", "rb"))))' | grep "Троль или рил долбаеб?"  # Что было
<a href="/b/res/174176908.html#174176908" class="post-reply-link" data-thread="174176908" data-num="174176908">>>174176908 (OP)</a><br>Троль или рил долбаеб?
$ python -m harkach_normalize ./posts.pkl 
2018-04-11 16:06:24,317 (__main__.py:25 MainThread) DEBUG - root: args: ['/home/saber-nyan/Documents/Development/Workspace/Python/harkach2data/harkach_normalize/__main__.py', './posts.pkl']
2018-04-11 16:06:24,322 (__main__.py:28 MainThread) INFO - root: posts count: 7443
2018-04-11 16:06:24,322 (__main__.py:29 MainThread) INFO - root: started!
2018-04-11 16:06:24,357 (__main__.py:46 MainThread) INFO - root: done!
$ grep "Троль или рил долбаеб?" ./output_data.txt  # Что получили
Троль или рил долбаеб? 
```
