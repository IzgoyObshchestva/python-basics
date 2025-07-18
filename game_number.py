import random

class Game:
    def __init__(self):
        self.game = 1
        self.number_random = self.get_random_number()

    def start(self):
        print(f"Угадай число от 1 до 100. У тебя 5 попыток.")
        while self.game <= 5:
            number_user = int(input(f"Поптытка {self.game}: "))
            res = self.check_guess(self.number_random, number_user)
            if res[0]:
                print(res[1])
                break
            else:
                print(res[1])
                self.game+=1
        else:
            print(f"Ты проиграл. Было число: {self.number_random}")

    @staticmethod
    def check_guess(number_random, number):
        if number == number_random:
            return (True, "Ты угадал!")
        elif number < number_random:
            return (False, "Слишком маленькое")
        elif number > number_random:
            return (False, "Слишком большое")

    @staticmethod
    def get_random_number():
        return random.randint(1, 100)
    
q = Game()


if __name__ == '__main__':
    q.start()