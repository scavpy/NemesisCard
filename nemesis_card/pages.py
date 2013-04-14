from nemesis_card.bottle import get, post, template

@get("/")
def home_page():
    return """
<!doctype html>
<html>
<body>
 <h1>Nemesis Card</h1>
</body>
</html>
"""

