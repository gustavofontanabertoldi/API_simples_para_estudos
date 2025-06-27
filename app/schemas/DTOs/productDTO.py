from pydantic import BaseModel, Field

class ProductDTO(BaseModel):   
    name : str = Field(...,min_length=1, max_length=100, description='name from the product')
    description : str = Field(None , min_length=0, max_length=500, description='description of the product')

    class Config:
        from_attributes = True



'''
Builder não será utilizado, pois não faz sentido para essa aplicação, favor ignorar abaixo.
'''

# class ProductDTOBuilder:
#     def __init__(self):
#         self._name: str | None = None
#         self._description: str | None = None

#     def com_name(self, name):
#         self.com_name = name
#         return self
    
#     def com_description(self, description):
#         self.com_description = description
#         return self
    
#     def build(self) -> ProductDTO:
#         return ProductDTO(
#             name=self._name,
#             description=self._description
#         )

# def product_dto_diretor(name: str, description: str) -> ProductDTO:
#     return ProductDTOBuilder().com_name(name).com_description(description).build()