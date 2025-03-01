
class next_page:
    def __init__(self, page):
        self.page = page
    
    def main(self):
        if self.page in []:
            self.page += 1
        return "page", self.page