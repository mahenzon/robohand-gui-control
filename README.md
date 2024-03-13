# RoboHand Control PySide6 GUI

## Установка зависимостей

Установить все зависимости:

```shell
poetry install
```

Если не нужно управление через gpio (например, запуск кода не на одноплатнике),
устанавливайте зависимости без пакетов для работы через gpio (пакет gpiod не встанет на обычные компы).
```shell
poetry install --without servokit
```
# robohand-gui-control
