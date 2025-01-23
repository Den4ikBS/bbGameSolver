# bbGameSolver

Установка пакета из ОС Linux:

```bash
git clone https://github.com/Den4ikBS/bbGameSolver
cd bbGameSolver

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Запуск программы осуществляется при помощи сценария `launch.sh` :
```bash
bash ./launch.sh
```

Краткое описание основных модулей и функций проекта
- config              -- файл с глобальными параметрами проекта
- gui                 -- модуль, реализующий приложение с графическим интерфейсом
    - gui.gui_tools   -- модуль, реализующий составные виджеты
        - 
    - gui.gui_widgets -- модуль с фабриками встроенных виджетов
- calc                -- расчётный модуль с решателями игр
    - calc.DGame      -- решатель дискретной антагонистической игры


Подробное описание методов и функций содержится в док-строках в исходном коде