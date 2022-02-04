Autor: Piotr Potomski
## Projekt aplikacji otwierajacej pliki ELF bez wywołań systemowych 

Skrypt generuje interpretowalny kod dla dostarczonego ELF z możliwością wykonania go. 


### Użycie
1. Uruchomienie okienowej aplikacji App_Gui 
```console
    $ ./App_gui
```
Należy wybrać plik (np. example_file_1, który jest skompilowanym plikiem example_file_1.c), a następnie kliknąć przycisk "Run". Aplikacja wygeneruje skrypt wyjściowy o nazwie "output_nazwapliku.py".

2. Uruchomienie skryptu "Open_File.py".

Wyżej wymieniony skrypt jest nieokienkową wersją aplikacji "App_Gui". Aby uruchomić poprawnie skrypt w parametrach
należy podać nazwę pliku, lub ścieżkę do pliku jeśli plik nie znajduje się w folderze z projektem:
```console
    -path example_file_1
```
Tak uruchomiony skrypt nie zapisuje pliku outputowego, a jedynie wyświetla go w konsoli.


3. Uruchomienie aplkacji z termianala:
```console
    $ python -m Open_File ./example_file_1 > output_filename.py
```
