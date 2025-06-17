class GPIO:
    BCM = 11
    BOARD = 10
    OUT = 0
    IN = 1
    HIGH = 1
    LOW = 0
    
    @staticmethod
    def setmode(mode):
        print(f"GPIO.setmode({mode})")
    
    @staticmethod
    def setup(pin, mode):
        print(f"GPIO.setup({pin}, {mode})")
    
    @staticmethod
    def output(pin, state):
        print(f"GPIO.output({pin}, {state})")
    
    @staticmethod
    def cleanup():
        print("GPIO.cleanup()")
    
    @staticmethod
    def setwarnings(flag):
        print(f"GPIO.setwarnings({flag})") 