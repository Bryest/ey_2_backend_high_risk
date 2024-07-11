
# Web Scraping exercise 1 
## [Offshore Leaks Database](https://offshoreleaks.icij.org/)
### To Run the project
1. Create the virtual environment <br>
`python -m venv venv`

2. To activate venv (Windows) <br>
`venv\Scripts\activate`

3. Install the dependecies for the project <br>
`pip install -r requirements.txt`

4. To run the project <br>
`flask --app app.py run`

5. Running in port <br>
`http://127.0.0.1:5000`

6. Endpoint and Example <br>
 *  Endpoint <br>
`http://127.0.0.1:5000/search?entity_name={entity_name}`

 * Example <br>
`http://127.0.0.1:5000/search?entity_name=New Entity Limited`