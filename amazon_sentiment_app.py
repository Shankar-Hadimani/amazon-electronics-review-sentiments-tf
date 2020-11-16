import tensorflow_datasets as tfds
import tensorflow as tf 
from flask import Flask, json, jsonify, make_response, request
from healthcheck import HealthCheck, EnvironmentDump
import logging
import waitress


app = Flask(__name__)
padding_size = 1000
model = tf.keras.models.load_model('model\sentiment_analysis.hdf5')
text_encoder = tfds.features.text.TokenTextEncoder.load_from_file('dataset\sa_encoder.vocab')

# set up logger information
logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
logging.basicConfig(format = logFormatStr, filename = "log\global_sa_amazon_tf.log", level=logging.DEBUG)
formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')
fileHandler = logging.FileHandler("log\summary_sa_amazon_tf.log")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)
app.logger.addHandler(fileHandler)
app.logger.addHandler(streamHandler)
app.logger.info("Logging is set up.")

#add initial info
logging.info('...sentiment anlaytics tensor flow Model and Vocabulary tokens have been loaded successfully.....')


# health status function 
def app_available():
    return True, "Application is OK"

# add environment dump
def application_data():
    import datetime
    time_val = datetime.datetime.now().isoformat()
    service_used = tf.__version__

    return jsonify({"App owner": "sa_amazon_tf_support","DateTime": time_val,"service" : "tensor flow",    "version": service_used})

health = HealthCheck(app, '/healthcheck')
# envdump = EnvironmentDump('/environment')

# add check and environment section
health.add_check(app_available)
# envdump.add_section("application", application_data)


# add func to pad the size of the vector by adding zeros at the end
def pad_to_size(vec, size):
    zeros = [0] * (size - len(vec))
    vec.extend(zeros)
    return vec


# predict the sentioment values
def predict_val(pred_text, pad_size):
    encode_text = text_encoder.encode(pred_text)
    pad_pred_text = pad_to_size(encode_text, pad_size)
    cast_pad_text = tf.cast(pad_pred_text, tf.int64)
    predict_value = model.predict(tf.expand_dims(cast_pad_text, 0))

    return (predict_value.tolist())


# # route app to expose the helath and environment dumps
# app.add_url_rule('/healthcheck', 'healthcheck', health())
# app.add_url_rule('/environment', 'environment', envdump())


@app.route('/seclassifier',methods=['POST'] )
def predict_sentiment():
    text = request.get_json()['text']
    print(text)
    predicted_value = predict_val(text, padding_size)
    sentiment = 'positive' if float(''.join(map(str, predicted_value[0]))) > 0 else 'negative'
    app.logger.info("prediction:" + str(predicted_value[0])+ "  sentiment: "+ sentiment)

    return jsonify({
        'predictions ': predicted_value,
        'sentiment': sentiment
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)

