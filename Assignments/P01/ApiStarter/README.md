## Fast Api - Backend for Country Game

## Resources

### Fast Api Tutorial and Docs

-   Remember that they run the api differently using `uvicorn` from the command line and we
    use `python filename.py` which invokes `uvicorn` from the `__main__` block inside the file.
-   https://fastapi.tiangolo.com/tutorial/

### Realpython tutorial

-   Realpython is usually very good.
-   https://realpython.com/fastapi-python-web-apis/

### Requirements

-   You can install the `requirements.txt` by running: `python -m pip install -r requirements.txt`
-   Remember that I decided to use Pythons `Vertualenv` instead of conda. So I think this command should work for anyone using `conda` as thier environment: `conda install --file requirements.txt`
-

## Api Methods

-   GET `/country_names/`
    -   returns a list of country names
-   GET `/country/{country_name}`
    -   returns a polygon (and more) for a chosen country
-   GET `/countryCenter/{country_name}`
    -   returns a point based on the centroid of a polygon
-   GET `/country_lookup/{key}`
    -   returns all countries as matched by a substring
-   GET `/line_between/`
    -   returns a feature (linestring) that connects to centroids of two countries.
-   GET `/property/{country}`
    -   returns a property from a country (pass in a key, get the value)
-   GET `/bbox/{country}`
    -   returns a bounding box of a countries polygon
-   GET `/bboxCenter/{country}`
    -   returns the center of a bounding box (slightly different than the centroid)
-   GET `/centroidRelations/`
    -   returns the distance and bearing between two centroids from two countries.
-   GET `/borderRelations/`
    -   returns the distance between two polygons after finding the minimum distance between all points in both polygons. If any points are "shared" (distance = 0), than those are returned instead.
-   GET `/lengthLine/{country}`
    -   returns a line feature between the furthest two points in a single polygon.
-   GET `/cardinal/{degrees}`
    -   returns a cardinal direction (N, E, S, W, + more) given a decimal degree.
