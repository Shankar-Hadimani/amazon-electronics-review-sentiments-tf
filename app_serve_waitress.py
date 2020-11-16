from waitress import serve
import amazon_sentiment_app

### waitress to scale the flask app
### waitress for windows OS
serve(amazon_sentiment_app, port=8000, threads=6)
