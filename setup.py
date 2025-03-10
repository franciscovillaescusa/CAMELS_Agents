from setuptools import setup, find_packages

setup(name='CAMELS Agents',
      version='0.1.0',
      packages=find_packages(),
      install_requires=['streamlit',
                        'tiktoken',
                        'langchain',
                        'langchain-chroma',
                        'langchain-groq',
                        'langchain-google-vertexai',
                        'langchain-google-genai',
                        'pydantic',
                        'dotenv',
                        'requests',
                        'typing-extensions'],
    entry_points={'console_scripts': ['your_app=app:main']},
    include_package_data=True,
    zip_safe=False)
