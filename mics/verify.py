from prisma_ import prisma



class Utils:
    def __init__(self) -> None:
     self.prisma = prisma      
    
    
    async def verify_user_and_check_expires(self, token):
        pass
        
util = Utils()
