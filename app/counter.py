import time

def countdown(seconds: int) -> None:
    while seconds > 0:
        print(f'Обратный отсчёт: {seconds}')
        time.sleep(1)
        seconds -= 1

    print('Время вышло!')

def main() -> None:
    countdown(600)

if __name__ == "__main__":
    main()
