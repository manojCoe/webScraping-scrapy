# webScraping-scrapy

Blue-tomatoe website:
[URL](https://www.blue-tomato.com/de-DE/products/categories/Snowboard+Shop-00000000/ "blue tomotoes")

Run Command(cmd): _scrapy crawl blue -o brad1.json_

**Note:**
	1. 
The following code is mandatory in youe settings.py file
```python
	ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}
	IMAGES_STORE = 'img_folder' #create a new img_folder before
```
	2. Modify your pipelines.py file like below
```python 
	from scrapy.pipelines.images import ImagesPipeline

	class customImagePipeline(ImagesPipeline):
		def file_path(self, request, response=None, info=None):
			return request.url.split('/')[-1]
```