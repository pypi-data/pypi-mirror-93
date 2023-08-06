from bergen.types.manager import  ModelManager
from bergen.types.model import ArnheimAsyncModelManager

class RepresentationManager(ModelManager):

    def from_xarray(self, array, compute=True, **kwargs):
        instance = self.create(**kwargs)
        instance.save_array(array, compute=compute)
        print(instance)
        instance = self.update(id=instance.id, **kwargs)
        return instance


class AsyncRepresentationManager(ArnheimAsyncModelManager["Representation"]):

    async def from_xarray(self, array, compute=True, **kwargs):
        instance = await self.create(**kwargs)
        instance.save_array(array, compute=compute)
        print(instance)
        instance = await self.update(id=instance.id, **kwargs)
        return instance