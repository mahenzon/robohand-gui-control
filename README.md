# RoboHand Control PySide6 GUI

## Установка зависимостей

Для установки Python пакета `gpiod` необходимо установить сборщик:
```shell
sudo apt install libffi-dev
```

А также (вероятно) использовать Python не свежее 3.10

### Установка для сервера (устройство, которое будет управлять роботом)

```shell
poetry install --only server
```
### Установка для пульта (интерфейс для управления)

```shell
poetry install --only gui
```

### Установить все зависимости:

```shell
poetry install
```

Если не нужно управление через gpio (например, запуск кода не на одноплатнике),
устанавливайте зависимости без пакетов для работы через gpio (пакет gpiod не встанет на обычные компы).
```shell
poetry install --without servokit
```
# robohand-gui-control
