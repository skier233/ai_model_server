import time
from ai_processing import preprocess_image_cpu
from lib.async_lib.async_processing import ItemFuture
from lib.model.model import Model


class ImagePreprocessorModel(Model):
    def __init__(self, configValues):
        super().__init__(configValues)  # Assuming Python 3 syntax for brevity
        self.use_gpu = configValues.get("use_gpu", False)
        self.image_size = configValues.get("image_size", 512)
    
    async def worker_function(self, data):
        if self.use_gpu:
            pass #TODO AT SOME POINT IN THE FUTURE MAYBE
        else:
            await self.preprocess_cpu(data)


    async def preprocess_cpu(self, data):
        for item in data:
            try:
                itemFuture = item.item_future
                input_data = itemFuture[item.input_names[0]]
                preprocessed_frame = preprocess_image_cpu(input_data, self.image_size)
                await itemFuture.set_data(item.output_names[0], preprocessed_frame)
            except FileNotFoundError as fnf_error:
                print(f"File not found error: {fnf_error}")
                itemFuture.set_exception(fnf_error)
            except IOError as io_error:
                print(f"IO error (image might be corrupted): {io_error}")
                itemFuture.set_exception(io_error)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                itemFuture.set_exception(e)

    async def preprocess_gpu(self, data):
        pass #TODO AT SOME POINT IN THE FUTURE MAYBE