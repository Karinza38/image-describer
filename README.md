Overview
A framework for continuous and self-training(without training dataset) of custom image classifier so that it can describe the image appearing on digital documents such as ebooks, comics etc.

# How to run
- Deploy the framework
  - Setup an [Azure Machine Learning workspace](https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-manage-workspace)
  - Run this [notebook](image_describer_training_pipeline.ipynb). Before running,
      - Configure [Azure Machine Learning Development Environment](https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-configure-environment).
      - Install the required dependencies
      - Download the `config.json` of your `AML Workspace`to the root. It is needed for the authorization of your AML workspace. 
      - If you want, you can change the step scripts with your training and scrapping logic. Learn about [Azure Machine Learning Pipelines](https://github.com/Azure/MachineLearningNotebooks/tree/master/how-to-use-azureml/machine-learning-pipelines)
      - The current logic uses [Custom Vision API](https://azure.microsoft.com/en-us/services/cognitive-services/custom-vision-service/) image classifier, which is trained by the image-describer framework, and [Bing Image Search](https://azure.microsoft.com/en-us/services/cognitive-services/bing-image-search-api/), for web scrapping.
      - If you want to use the same logic, replace the required subscription keys and endpoints in the scripts of [train](./train_step) and [scrapper](./image_scrapper_step) step.
      
 - Train using the framework
    - You can use the framework to train your classifier using REST endpoint, through Azure Portal or by creating a schedule for self training, as shown in the later sections of this [notebook](image_describer_training_pipeline.ipynb).
    
 - Use\Test your image classifier 
    - Run [comic_reader.py](comic_reader.py). Before running,
      - If you are using the current logic, Put your subscription keys and endnpoints in [keys.json](keys.json).
    - A `.wmv` file will be generated in the root folder
    - Play the voice transcript generated by the [comic_reader.py](comic_reader.py)
