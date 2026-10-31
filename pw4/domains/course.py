class Course:
    def __init__(self, cid, name, credits):
        self.cid = cid
        self.name = name
        self.credits = credits

    def __str__(self):
        return f"{self.cid:<10} {self.name:<24} {self.credits} credits"
