
# DataVista

DataVista is an advanced Database Management System (DBMS) designed to simplify database interactions for users of all levels of expertise. The platform provides a secure login interface where users enter their credentials, database name, and select the database type—SQL or MongoDB—ensuring seamless connectivity to different data sources.

After successful login, users are redirected to the homepage, where they can describe their intended database operation in natural language. DataVista generates the corresponding database query, along with the expected output and a step-by-step explanation. Users can choose to execute the AI-generated query or run their own custom query, making DataVista both intuitive and flexible for efficient database management.



## Run Locally

Clone the project

```bash
  git clone https://github.com/pioneerHitesh/DataVista.git
```

Go to the project directory

```bash
  cd DataVista
```

(Recommended) Create a virtual environment

```bash
  python -m venv env
```

Activate it

```bash
  .\env\Scripts\activate
```





Install dependencies

```bash
  pip install -r requirements.txt
```

Configure API Keys

- Open config.py and add your API keys:

```python 
GOOGLE_API_KEY = "<Your Gemini API Key here>"
```

Start the server

```bash
  python app.py
```


## Demo


[![DataVista Demo](https://img.youtube.com/vi/PZnrRCrlIGc/0.jpg)](https://youtu.be/PZnrRCrlIGc)

Click the image to watch the demo on YouTube.

## Contributing

Pull requests are welcome.
Please ensure your changes do not include secrets or local configuration files.


## License

[MIT](https://choosealicense.com/licenses/mit/)

